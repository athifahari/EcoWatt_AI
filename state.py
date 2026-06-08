# ============================================================
#  state.py
#  Initialization and helpers for st.session_state
# ============================================================

import streamlit as st
from constants import APPLIANCES

def init_state() -> None:
    # Force delete all incorrect old variables (English versions)
    old_keys = ["n_residents", "monthly_kwh"]
    for key in old_keys:
        if key in st.session_state:
            del st.session_state[key]
        
    # Initialize new variables (Indonesian names preserved for logic)
    defaults = {
        "step": 1,
        "n_penghuni": 3,
        "kwh_bulan": 250,
        "usage_hours": {ap["id"]: 0 for ap in APPLIANCES},
        "checked": {ap["id"]: False for ap in APPLIANCES},
        "result": None,
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def go_to(page_num):
    st.session_state.step = page_num
    st.rerun()

def reset_state():
    # Clear all keys to perform a full reset
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()