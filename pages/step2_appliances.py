# ============================================================
#  pages/step2_appliances.py
#  Step 2 — Electronic Appliances (checkbox + daily usage slider)
# ============================================================

import streamlit as st
from constants import APPLIANCES, WATT
from ui_components import render_steps, section_header
from state import go_to


def render() -> None:
    render_steps(2)
    section_header("🔌", "Electronic Appliances",
                   "Check the appliances you own, then slide to set daily usage hours.")

    _, col_note, _ = st.columns([1, 4, 1])
    with col_note:
        st.info(
            "💡 **Note:** Power consumption (Watt) uses standard average values. "
            "Actual consumption may vary depending on brand and appliance specifications."
        )

    _, col_m, _ = st.columns([1, 4, 1])
    with col_m:
        for ap in APPLIANCES:
            aid   = ap["id"]
            is_on = st.session_state.checked.get(aid, False)

            card_cls = "ap-card active" if is_on else "ap-card"
            st.markdown(f'<div class="{card_cls}">', unsafe_allow_html=True)

            chk = st.checkbox(
                f"{ap['emoji']} **{ap['label']}** · `{ap['watt_desc']}`",
                value=is_on, key=f"chk_{aid}",
            )
            st.session_state.checked[aid] = chk

            if chk:
                cur_h = st.session_state.usage_hours.get(aid, 4)
                h = st.slider(
                    "⏱ Usage hours per day",
                    min_value=0, max_value=24,
                    value=cur_h, key=f"sl_{aid}", format="%d hrs",
                )
                st.session_state.usage_hours[aid] = h
                est_kwh_bulan = (WATT[aid] * h * 30) / 1000
                st.markdown(
                    f'<div style="font-size:.8rem;color:#4EC95A;font-weight:700;margin-top:4px">'
                    f'≈ {est_kwh_bulan:.1f} kWh/month</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.session_state.usage_hours[aid] = 0

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

        cb, cn = st.columns(2)
        with cb:
            if st.button("⬅️ Back", type="secondary", key="btn_s2b"):
                go_to(1)
        with cn:
            if st.button("➡️ Confirm Data", type="primary", key="btn_s2"):
                go_to(3)