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
HEMAT_MAX = 40 * 12   # = 480  → < 480/tahun (≈ <40/bln) → hemat - data pln
BOROS_MIN = 60 * 12   # = 720  → > 720/tahun (≈ >60/bln) → boros - data pln

def vonis_realistis(kwh_per_orang_tahun: float) -> str:
    """Status berbasis distribusi dataset (tertile), skala TAHUNAN."""
    if kwh_per_orang_tahun < HEMAT_MAX:
        return "hemat"
    if kwh_per_orang_tahun > BOROS_MIN:
        return "boros"
    return "normal"

def run_predict(X_df: pd.DataFrame) -> str:
    """
    Vonis status memakai ambang realistis (norma PLN), berbasis kwh_per_orang.
    Decision Tree & K-Means tetap dilatih di notebook sebagai fondasi metodologi
    (pelabelan + analisis pola), tetapi TIDAK dipakai untuk vonis akhir karena
    skala dataset (sintetis, kecil) tidak mewakili konsumsi Indonesia.
    """
    if "kwh_per_orang" in X_df.columns:
        return vonis_realistis(float(X_df["kwh_per_orang"].iloc[0]))
    if "total_kwh_tahun" in X_df.columns and "household_size" in X_df.columns:
        kpo = float(X_df["total_kwh_tahun"].iloc[0]) / float(X_df["household_size"].iloc[0])
        return vonis_realistis(kpo)
    return "normal"