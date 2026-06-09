import streamlit as st
from ui_components import render_hero, render_steps, section_header
from state import go_to
from constants import TARIF_PLN

def render() -> None:
    render_hero()
    render_steps(1)
    section_header("🏠", "Household Information",
                   "Tell us a little about your home — this only takes 30 seconds!")

    _, col_m, _ = st.columns([1, 3, 1])
    with col_m:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        # ── Jumlah penghuni ──────────────────────────────────
        st.markdown("**👥 How many people live in your home?**")
        n = st.number_input(
            "Residents", min_value=1, max_value=15,
            # Gunakan .get() untuk mencegah error jika key belum terinisialisasi
            value=st.session_state.get("n_penghuni", 3), 
            label_visibility="collapsed", key="inp_penghuni",
        )
        st.caption("Count everyone living in the house, including children!")

        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

        # ── Pilih cara input ─────────────────────────────────
        st.markdown("**⚡ How would you like to enter your usage?**")
        mode = st.radio(
            "input_mode",
            ["I know my kWh", "I know my bill (Rp)"],
            horizontal=True, label_visibility="collapsed", key="inp_mode",
        )

        if mode == "I know my kWh":
            kwh = st.number_input(
                "kWh", min_value=10, max_value=5000,
                value=st.session_state.get("kwh_bulan", 250),
                label_visibility="collapsed", key="inp_kwh",
            )
            st.markdown(
                '<div class="info-pill">💡 Check your electricity bill or PLN Mobile app</div>'
                '<div style="font-size:.8rem;color:#6B8F78;margin-top:8px;font-weight:500">'
                'Examples: 150 kWh (small) · 250 kWh (medium) · 450 kWh (large)</div>',
                unsafe_allow_html=True,
            )
        else:
            rupiah = st.number_input(
                "Rupiah", min_value=10000, max_value=10_000_000, step=10000,
                value=int(st.session_state.get("kwh_bulan", 250) * TARIF_PLN),
                label_visibility="collapsed", key="inp_rupiah",
            )
            kwh = round(rupiah / TARIF_PLN)
            st.markdown(
                f'<div class="info-pill">💡 Estimated ≈ <b>{kwh} kWh</b> '
                f'(at Rp{TARIF_PLN:,.0f}/kWh)</div>'
                '<div style="font-size:.8rem;color:#6B8F78;margin-top:8px;font-weight:500">'
                'Note: an estimate — real bills include admin fees & tax, so it may differ slightly.</div>',
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

         # ── Note: Step 2 opsional ────────────────────────────
        st.markdown(
            '<div class="info-pill" style="margin-top:14px">'
            'ℹ️ <b>Next step (appliances) is optional.</b> '
            'You can skip it — your status (efficient/normal/high) is still calculated. '
            'Adding appliances just makes the recommendations more accurate.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        if st.button("➡️ Continue to Appliances", type="primary", key="btn_s1"):
            st.session_state.n_penghuni = n
            st.session_state.kwh_bulan  = int(kwh)
            go_to(2)