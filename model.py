# ============================================================
#  model.py
#  Load .pkl models + feature engineering according to the dataset
# ============================================================

import os
import pandas as pd
import streamlit as st

from constants import APPLIANCES, WATT, FITUR_ML, SKALA_MODEL


# ── .pkl file names ───────────────────────────────────────────
SCALER_PATH = "scaler_energi.pkl"
MODEL_PATH  = "model_tree_energi.pkl"


@st.cache_resource
def load_model() -> tuple:
    """
    Load scaler and model from .pkl files.
    Returns (scaler, model) if files are found,
    or (None, None) if they are not yet available.
    """
    if os.path.exists(SCALER_PATH) and os.path.exists(MODEL_PATH):
        import joblib
        scaler = joblib.load(SCALER_PATH)
        model  = joblib.load(MODEL_PATH)
        return scaler, model
    return None, None


def is_model_ready() -> bool:
    """Returns True if both .pkl files are available."""
    scaler, model = load_model()
    return scaler is not None and model is not None


def build_features(
    kwh_bulan:   int,
    n_penghuni:  int,
    usage_hours: dict,
    avg_temp:    float = 27.0,
) -> pd.DataFrame:
    """
    Build a 1-row feature DataFrame according to the dataset schema.

        kwh_bulan_model  = kwh_bulan ÷ SKALA_MODEL  (sesuaikan ke skala dataset training)
        total_kwh_tahun  = kwh_bulan_model × 12     (dipakai untuk fitur model)
        kwh_<appliance>  = Watt × hours/day × 365 / 1000   (annual, skala asli — untuk tampilan/rekomendasi)
        prop_<appliance> = kwh_<appliance> / Σ kwh_all_appliances  (rasio, tidak terpengaruh skala)
        kwh_per_orang    = total_kwh_tahun / household_size  (fitur model, skala dataset)
    """
    # Rescale input user (skala realistis Indonesia) ke skala dataset training
    kwh_bulan_model = kwh_bulan / SKALA_MODEL
    kwh_tahun = kwh_bulan_model * 12

    # Annual kWh per appliance
    kwh_alat: dict[str, float] = {
        ap["id"]: (WATT[ap["id"]] * usage_hours.get(ap["id"], 0) * 365) / 1000
        for ap in APPLIANCES
    }
    total_kwh_alat = sum(kwh_alat.values())

    # Proportion per appliance (0.0 if no usage)
    prop_alat: dict[str, float] = {
        k: (v / total_kwh_alat if total_kwh_alat > 0 else 0.0)
        for k, v in kwh_alat.items()
    }

    row: dict[str, float] = {
        "total_kwh_tahun": float(kwh_tahun),
        "household_size":  float(n_penghuni),
        "avg_temp":        float(avg_temp),
        "kwh_per_orang":   float(kwh_tahun / n_penghuni),
        **{f"kwh_{k}":  float(v) for k, v in kwh_alat.items()},
        **{f"prop_{k}": float(v) for k, v in prop_alat.items()},
    }

    df = pd.DataFrame([row])

    # Prioritize column order from scaler (most accurate)
    scaler, _ = load_model()
    if scaler is not None and hasattr(scaler, "feature_names_in_"):
        scaler_cols = list(scaler.feature_names_in_)
        # FIX: scaler mungkin dilatih tanpa kwh_per_orang.
        # Pastikan kolom ini tetap ada di df yang dikembalikan
        # agar vonis_realistis() bisa membacanya.
        cols = scaler_cols
        if "kwh_per_orang" not in cols:
            cols = cols + ["kwh_per_orang"]
    else:
        # Fallback: gunakan FITUR_ML, filter hanya yang ada di df
        cols = [c for c in FITUR_ML if c in df.columns]

    # Isi kolom yang tidak ada di df dengan 0 (bukan error)
    for c in cols:
        if c not in df.columns:
            df[c] = 0.0

    return df[cols]


# ============================================================
#  THRESHOLD BERBASIS DATASET (tertile / pembagian 3 kelompok)
#
#  Dihitung dari distribusi kolom `kwh_per_orang` (skala TAHUNAN,
#  sama seperti di dataset_energi.csv) menggunakan persentil 33%
#  dan 67%, sehingga jumlah baris hemat/normal/boros relatif seimbang.
#
#  Kategori (kwh_per_orang per TAHUN):
#    HEMAT  : < 77   (≈ persentil bawah 33%)
#    NORMAL : 77 – 146
#    BOROS  : > 146  (≈ persentil atas 33%)
#
#  Jika dataset diganti, hitung ulang dengan:
#    df['kwh_per_orang'].quantile(1/3) dan quantile(2/3)
# ============================================================
HEMAT_MAX = 77    # kwh_per_orang/tahun < 77   → hemat
BOROS_MIN = 146   # kwh_per_orang/tahun > 146  → boros


def vonis_realistis(kwh_per_orang_tahun: float) -> str:
    """Status berbasis distribusi dataset (tertile), skala TAHUNAN."""
    if kwh_per_orang_tahun < HEMAT_MAX:
        return "hemat"
    if kwh_per_orang_tahun > BOROS_MIN:
        return "boros"
    return "normal"


def run_predict(X_df: pd.DataFrame) -> str:
    """
    Vonis status (hemat/normal/boros) untuk input user.

    Prioritas:
      1. Jika model_tree_energi.pkl tersedia, gunakan
         model_tree.predict() langsung pada fitur SKALA ASLI
         (fitur_ml = 11 kolom: kwh_per_orang + 10 prop_<alat>).

         PENTING: scaler_energi.pkl TIDAK dipakai di sini.
         Berdasarkan notebook training, StandardScaler hanya
         dipakai untuk input KMeans (clustering label), sedangkan
         DecisionTreeClassifier di-fit langsung pada
         df_rumah[fitur_ml] (skala asli/tidak di-scale). Decision
         tree juga tidak butuh feature scaling secara prinsip.
         Memanggil scaler.transform() di sini membuat semua
         threshold tree (misal kwh_per_orang <= 172.79) menjadi
         tidak pernah tercapai -> prediksi selalu jatuh ke kelas
         yang sama.

      2. Jika model tidak tersedia / error, fallback ke threshold
         berbasis tertile dataset (vonis_realistis).

    Proporsi peralatan (prop_*) tetap tersimpan di session_state
    untuk rekomendasi di halaman hasil.
    """
    _, model = load_model()

    if model is not None and hasattr(model, "feature_names_in_"):
        model_cols = list(model.feature_names_in_)
        for c in model_cols:
            if c not in X_df.columns:
                X_df[c] = 0.0

        X_model = X_df[model_cols]

        try:
            pred = model.predict(X_model)
            return str(pred[0])
        except Exception:
            # Jika terjadi error tak terduga saat predict, fallback ke rule-based
            pass

    # Fallback rule-based (threshold tertile dataset)
    if "kwh_per_orang" not in X_df.columns:
        if "total_kwh_tahun" in X_df.columns and "household_size" in X_df.columns:
            kwh_per_orang = (
                float(X_df["total_kwh_tahun"].iloc[0])
                / float(X_df["household_size"].iloc[0])
            )
            return vonis_realistis(kwh_per_orang)
        return "normal"  # default jika data tidak cukup

    return vonis_realistis(float(X_df["kwh_per_orang"].iloc[0]))