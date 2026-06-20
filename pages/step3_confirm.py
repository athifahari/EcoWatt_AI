# ============================================================
#  pages/step3_confirm.py
#  Step 3 — Confirm data + run analysis
# ============================================================

import time
import streamlit as st

from constants import APPLIANCES, WATT, TARIF_PLN
from model import build_features, run_predict
from ui_components import render_steps, section_header
from state import go_to


def render() -> None:
    render_steps(3)
    section_header("🤖", "Confirm Data",
                   "Ensure the data below is correct before proceeding with analysis.")

    _, col_m, _ = st.columns([1, 4, 1])
    with col_m:
        _render_summary_card()
        _render_appliance_card()

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        cb, cn = st.columns(2)
        with cb:
            if st.button("⬅️ Edit Appliances", type="secondary", key="btn_s3b"):
                go_to(2)
        with cn:
            if st.button("🔍 Analyze My Home", type="primary", key="btn_s3"):
                _run_analysis()


# ── Helpers ───────────────────────────────────────────────────

def _render_summary_card() -> None:
    est_tag = st.session_state.kwh_bulan * TARIF_PLN
    st.markdown(
        '<div class="card"><strong>🏠 Household Information</strong>'
        f'<div class="confirm-row"><span class="key">👥 Residents</span>'
        f'<span class="val">{st.session_state.n_penghuni} people</span></div>'
        f'<div class="confirm-row"><span class="key">⚡ This Month\'s Usage</span>'
        f'<span class="val">{st.session_state.kwh_bulan} kWh</span></div>'
        f'<div class="confirm-row"><span class="key">💰 Estimated Bill</span>'
        f'<span class="val">Rp {est_tag:,.0f}</span></div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_appliance_card() -> None:
    aktif = [
        (ap, st.session_state.usage_hours.get(ap["id"], 0))
        for ap in APPLIANCES
        if st.session_state.checked.get(ap["id"], False)
    ]
    if aktif:
        rows = "".join(
            f'<div class="confirm-row">'
            f'<span class="key">{ap["emoji"]} {ap["label"]}</span>'
            f'<span class="val">{jam} hrs/day · ≈{(WATT[ap["id"]] * jam * 30) / 1000:.1f} kWh/mo</span>'
            f'</div>'
            for ap, jam in aktif
        )
        st.markdown(
            f'<div class="card"><strong>🔌 Selected Appliances</strong>{rows}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("⚠️ No appliances selected.")


def _run_analysis() -> None:
    """Loading animation → build features → predict → save results."""
    ph = st.empty()
    msgs = [
        "🤖 EcoWatt AI is analyzing your home...",
        "📊 Calculating energy consumption proportions...",
        "🌿 Preparing personalized recommendations...",
    ]
    for i, msg in enumerate(msgs):
        with ph.container():
            st.markdown(
                f'<div style="display:flex;flex-direction:column;align-items:center;'
                f'justify-content:center;text-align:center;margin:30px auto;max-width:500px">'
                f'<div style="font-size:4rem;margin-bottom:10px;'
                f'animation:float 1.5s ease-in-out infinite">🤖</div>'
                f'<div style="font-size:1.2rem;font-weight:700;color:#2EA89E;'
                f'margin-bottom:20px;line-height:1.5">{msg}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            _, col_bar, _ = st.columns([1, 6, 1])
            with col_bar:
                st.progress((i + 1) / len(msgs))
        time.sleep(0.9)
    ph.empty()

    # Build features & predict
    X_df  = build_features(
        st.session_state.kwh_bulan,
        st.session_state.n_penghuni,
        st.session_state.usage_hours,
    )
    label = run_predict(X_df)

    # Compute supporting data for the results page
    kwh_tahun   = st.session_state.kwh_bulan * 12
    est_tahunan = {
        ap["id"]: (WATT[ap["id"]] * st.session_state.usage_hours.get(ap["id"], 0) * 365) / 1000
        for ap in APPLIANCES
    }
    total_est = sum(est_tahunan.values())
    props     = {k: v / total_est if total_est > 0 else 0.0 for k, v in est_tahunan.items()}

    st.session_state.result = {
        "label":               label,
        "kwh_bulan":           st.session_state.kwh_bulan,
        "kwh_tahun":           kwh_tahun,
        "n_penghuni":          st.session_state.n_penghuni,
        "kwh_per_orang_bulan": kwh_tahun / st.session_state.n_penghuni / 12,
        "est_bulan":           {k: v / 12 for k, v in est_tahunan.items()},
        "props":               props,
    }
    go_to(4)