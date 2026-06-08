# ============================================================
#  model.py
#  Load .pkl models + feature engineering according to the dataset
# ============================================================

import os
import pandas as pd
import streamlit as st

from constants import APPLIANCES, WATT, FITUR_ML


# ── .pkl file names ───────────────────────────────────────────
#  Change here if the file names differ
SCALER_PATH = "scaler_energi.pkl"
MODEL_PATH  = "model_tree_energi.pkl"


@st.cache_resource
def load_model() -> tuple:
    """
    Load scaler and model from .pkl files.
    Returns (scaler, model) if files are found,
    or (None, None) if they are not yet available.

    Integration guide:
        Place scaler_energi.pkl and model_tree_energi.pkl
        in the same folder as app.py, then restart Streamlit.
        The model will be automatically detected.
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
    Build a 1-row feature DataFrame according to the dataset schema:

        total_kwh_tahun  = kwh_bulan × 12
        kwh_<appliance>  = Watt × hours/day × 365 / 1000   (annual)
        prop_<appliance> = kwh_<appliance> / Σ kwh_all_appliances
        kwh_per_orang    = total_kwh_tahun / household_size

    Column order follows FITUR_ML (or feature_names_in_ from scaler).

    Parameters
    ----------
    kwh_bulan   : electricity consumption this month (kWh)
    n_penghuni  : number of family members
    usage_hours : dict {appliance_id: hours_of_use_per_day}
    avg_temp    : average ambient temperature (°C), default 27.0
    """
    kwh_tahun = kwh_bulan * 12

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
        cols = list(scaler.feature_names_in_)
    else:
        # Fallback: order from FITUR_ML (only columns present in df)
        cols = [c for c in FITUR_ML if c in df.columns]

    return df[cols]


def run_predict(X_df: pd.DataFrame) -> str | None:
    """
    Execute pipeline: scaler.transform → model.predict.

    Returns
    -------
    Prediction label string ('hemat' | 'normal' | 'boros')
    or None if the model is not available.

    Note:
        X_df.values is used (2D array) to avoid
        column name mismatch if the model was trained without feature_names_in_.
    """
    scaler, model = load_model()
    if scaler is None or model is None:
        return None

    X_scaled = scaler.transform(X_df.values)
    return model.predict(X_scaled)[0]