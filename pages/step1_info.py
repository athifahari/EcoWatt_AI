import streamlit as st
from ui_components import render_hero, render_steps, section_header
from state import go_to

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

        # ── Konsumsi kWh ─────────────────────────────────────
        st.markdown("**⚡ Electricity consumption last month (kWh)**")
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

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

        # ── Tombol lanjut ────────────────────────────────────
        if st.button("➡️ Continue to Appliances", type="primary", key="btn_s1"):
            st.session_state.n_penghuni = n
            st.session_state.kwh_bulan  = kwh
            go_to(2)