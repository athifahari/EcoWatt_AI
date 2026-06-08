import streamlit as st

from state import init_state

init_state()

from ui_components import inject_css, render_footer
import pages.step1_info       as step1
import pages.step2_appliances as step2
import pages.step3_confirm    as step3
import pages.step4_result     as step4

# ── Konfigurasi halaman ──────────────────────────────────────
st.set_page_config(
    page_title="🌱 EcoWatt AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Init & CSS ───────────────────────────────────────────────
inject_css()

# ── Router ───────────────────────────────────────────────────
_PAGES = {1: step1, 2: step2, 3: step3, 4: step4}
_PAGES[st.session_state.step].render()

# ── Footer ───────────────────────────────────────────────────
render_footer()
