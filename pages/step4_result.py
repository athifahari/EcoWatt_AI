# ============================================================
#  pages/step4_result.py
#  Step 4 — Analysis Results
#  Rekomendasi: Association Rules (mlxtend)
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json

from constants import APPLIANCES, TARIF_PLN, AVG_KWH_ORANG_INDO, FAKTOR_CO2
from ui_components import render_steps
from state import reset_state

# ── Status config ─────────────────────────────────────────────
_STATUS_CFG: dict = {
    "hemat":  {
        "cls": "hemat",  "emoji": "🏆",
        "badge": "✅ Energy Efficient",
        "msg": "Your home is <b>energy efficient</b> compared to the average! Keep up the good work 🌿",
    },
    "normal": {
        "cls": "normal", "emoji": "⚡",
        "badge": "🟡 Normal Consumption",
        "msg": "Your electricity usage is <b>quite normal</b>. There are a few small things you could improve!",
    },
    "boros":  {
        "cls": "boros",  "emoji": "🚨",
        "badge": "🔴 High Consumption",
        "msg": "Your electricity usage is <b>quite high</b>. Check out the recommendations below! 💪",
    },
    None: {
        "cls": "normal", "emoji": "❓",
        "badge": "— Prediction Unavailable",
        "msg": "The AI model is not yet integrated. You can still view your consumption data below.",
    },
}

_PIE_COLORS = [
    "#7AE582", "#89CFF0", "#FFE066", "#FF8FA3", "#A9E34B",
    "#FFA94D", "#CC5DE8", "#20C997", "#FF6B6B", "#74C0FC",
]

# ── Median proporsi dari dataset (untuk association rules) ────
_PROP_MEDIANS: dict[str, float] = {
    "Air_Conditioning": 0.2336,
    "Computer":         0.0722,
    "Dishwasher":       0.0723,
    "Fridge":           0.0196,
    "Heater":           0.2311,
    "Lights":           0.0735,
    "Microwave":        0.0721,
    "Oven":             0.0733,
    "TV":               0.0703,
    "Washing_Machine":  0.0724,
}

# ── Semua association rules hasil mining (label → arah_alat) ─
# Format: {label: [(arah_alat, confidence, lift), ...]}
# arah_alat = "high_AC" berarti rumah berlabel ini cenderung pakai AC TINGGI
_ALL_RULES: dict[str, list[tuple]] = {
    "hemat": [
        ("high_Computer",        0.569, 1.138),
        ("high_TV",              0.545, 1.090),
        ("high_Washing_Machine", 0.533, 1.066),
        ("low_Air_Conditioning", 0.533, 1.066),
        ("low_Dishwasher",       0.515, 1.030),
        ("high_Heater",          0.515, 1.030),
        ("high_Lights",          0.515, 1.030),
        ("high_Microwave",       0.509, 1.018),
        ("low_Oven",             0.503, 1.006),
        ("high_Fridge",          0.503, 1.006),
    ],
    "normal": [
        ("high_Microwave",       0.554, 1.108),
        ("low_Heater",           0.554, 1.108),
        ("high_Oven",            0.542, 1.084),
        ("high_Fridge",          0.536, 1.072),
        ("high_Dishwasher",      0.512, 1.024),
        ("low_Computer",         0.512, 1.024),
        ("low_Air_Conditioning", 0.512, 1.024),
        ("low_TV",               0.506, 1.012),
        ("high_Lights",          0.506, 1.012),
        ("high_Washing_Machine", 0.500, 1.000),
    ],
    "boros": [
        ("low_Microwave",        0.563, 1.126),
        ("low_Computer",         0.557, 1.114),
        ("high_Air_Conditioning",0.545, 1.090),
        ("low_Fridge",           0.539, 1.078),
        ("high_Heater",          0.539, 1.078),
        ("low_TV",               0.539, 1.078),
        ("low_Oven",             0.539, 1.078),
        ("low_Washing_Machine",  0.533, 1.066),
        ("low_Lights",           0.509, 1.018),
        ("high_Dishwasher",      0.503, 1.006),
    ],
}

def _get_relevant_rules(label: str, props: dict, max_rules: int = 3) -> list[tuple]:
    """
    Filter rules berdasarkan alat yang BENAR-BENAR dipakai user,
    lalu sort berdasarkan seberapa cocok profil user dengan pola rule.

    Prioritas:
    1. Alat yang dipakai user (prop > 0) DAN arahnya MATCH dengan rule
    2. Alat yang dipakai user DAN arahnya TIDAK match (informatif untuk edukasi)
    3. Alat yang tidak dipakai user (skip)
    """
    all_rules = _ALL_RULES.get(label, [])
    used_appliances = {k for k, v in props.items() if v > 0}

    matched, unmatched = [], []
    for arah_alat, conf, lift in all_rules:
        arah, alat = arah_alat.split("_", 1)
        if alat not in used_appliances:
            continue  # skip alat yang tidak dipakai user
        user_prop  = props.get(alat, 0)
        median     = _PROP_MEDIANS.get(alat, 0)
        user_arah  = "high" if user_prop > median else "low"
        is_match   = (user_arah == arah)
        entry      = (alat, arah, conf, lift, is_match)
        (matched if is_match else unmatched).append(entry)

    # Gabung: match dulu, lalu unmatch, ambil max_rules
    combined = matched + unmatched
    return combined[:max_rules]

_ALAT_LABEL: dict[str, str] = {
    ap["id"]: f"{ap['emoji']} {ap['label']}" for ap in APPLIANCES
}

# ── Main render ───────────────────────────────────────────────
def render() -> None:
    render_steps(4)
    r = st.session_state.result

    st.markdown(
        '<div style="max-width:740px;margin:0 auto;padding:8px 20px 0;text-align:center">'
        '<div style="font-size:1.7rem;font-weight:900;color:#1A2420;margin-bottom:4px">'
        '📊 EcoWatt AI Analysis Results</div>'
        '<p style="color:#6B8F78;font-weight:500;font-size:.95rem">'
        'Here is your household electricity consumption profile.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    label = r["label"]
    _, col_m, _ = st.columns([1, 4, 1])
    with col_m:
        _render_status_card(label)
        _render_metrics(r)
        _render_pie_chart(r)
        _render_association_insights(r)
        _render_fallback_recommendations(r)
        _render_insights(r)
        _render_reset_button()


# ── Sub-renders ───────────────────────────────────────────────
def _render_status_card(label) -> None:
    cfg = _STATUS_CFG.get(label, _STATUS_CFG[None])
    st.markdown(
        f'<div class="status-card {cfg["cls"]}">'
        f'<div class="status-emoji">{cfg["emoji"]}</div>'
        f'<div class="status-label badge-{cfg["cls"]}">{cfg["badge"]}</div>'
        f'<h2>Home Efficiency Status</h2>'
        f'<p>{cfg["msg"]}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_metrics(r: dict) -> None:
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("⚡ kWh / month",   f"{r['kwh_bulan']:,}")
    with m2: st.metric("👤 kWh / person",  f"{r['kwh_per_orang_bulan']:.1f}")
    with m3: st.metric("💰 Estimated Bill",f"Rp {r['kwh_bulan'] * TARIF_PLN:,.0f}")
    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)


def _render_pie_chart(r: dict) -> None:
    pie_labels, pie_vals = [], []
    for ap in APPLIANCES:
        v = r["est_bulan"][ap["id"]]
        if v > 0:
            pie_labels.append(f"{ap['emoji']} {ap['label']}")
            pie_vals.append(v)

    if not pie_vals:
        st.info("No appliances selected — chart not available.")
        return

    st.markdown(
        '<div style="font-size:1.1rem;font-weight:800;color:#1A2420;margin-bottom:4px">'
        '🥧 Energy Consumption Proportion</div>'
        '<p style="font-size:.87rem;color:#6B8F78;font-weight:500;margin-bottom:12px">'
        'Estimated contribution of each appliance to total electricity usage.</p>',
        unsafe_allow_html=True,
    )
    fig = go.Figure(go.Pie(
        labels=pie_labels, values=pie_vals, hole=0.44,
        marker=dict(colors=_PIE_COLORS, line=dict(color="white", width=2.5)),
        textinfo="label+percent",
        hovertemplate="%{label}<br><b>%{value:.1f} kWh/month</b><extra></extra>",
    ))
    fig.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", size=13),
        annotations=[dict(text="⚡", x=0.5, y=0.5, font_size=22, showarrow=False)],
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Association Rules Section ─────────────────────────────────
def _render_association_insights(r: dict) -> None:
    label      = r["label"]
    user_props = r.get("props", {})

    # Filter rules dinamis berdasarkan alat yang dipakai user
    relevant = _get_relevant_rules(label, user_props, max_rules=3)
    if not relevant:
        return

    st.markdown(
        '<div style="font-size:1.1rem;font-weight:800;color:#1A2420;margin:8px 0 4px">'
        '🔍 Pattern Analysis (Association Rules)</div>'
        '<p style="font-size:.87rem;color:#6B8F78;font-weight:500;margin-bottom:14px">'
        'Patterns discovered from mining the energy dataset — '
        'how your appliance profile matches homes with similar energy status.</p>',
        unsafe_allow_html=True,
    )

    label_emoji = {"hemat": "✅", "normal": "⚡", "boros": "🔴"}.get(label, "❓")

    for alat, arah, conf, lift, is_match in relevant:
        alat_label  = _ALAT_LABEL.get(alat, alat)
        median_pct  = _PROP_MEDIANS.get(alat, 0) * 100
        user_pct    = user_props.get(alat, 0) * 100
        match_icon  = "✅" if is_match else "⚠️"
        match_text  = "matches pattern" if is_match else "differs from pattern"
        bar_color   = "#7AE582" if is_match else "#FF8FA3"

        st.markdown(
            f'<div class="reco-card" style="margin-bottom:10px">'
            f'<div style="width:100%">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">'
            f'<span style="font-weight:700;font-size:.95rem"> {alat_label}</span>'
            f'<span style="font-size:.78rem;background:#f0f8f4;padding:2px 8px;border-radius:99px;color:#2EA89E;font-weight:600">'
            f'conf {conf:.0%} · lift {lift:.2f}</span>'
            f'</div>'
            f'<div style="font-size:.82rem;color:#6B8F78;margin-bottom:8px">'
            f'Your <b>{alat_label}</b> usage is '
            f'{"above" if arah == "high" else "below"} the dataset average '
            f'(dataset median: {median_pct:.1f}%)'
            f'</div>'
            f'<div style="display:flex;align-items:center;gap:8px;font-size:.82rem">'
            f'<div style="flex:1;background:#eee;border-radius:4px;height:6px">'
            f'<div style="width:{min(user_pct*2.5,100):.0f}%;background:{bar_color};height:6px;border-radius:4px"></div>'
            f'</div>'
            f'<span>Your usage: <b>{user_pct:.1f}%</b></span>'
            f'<span>{match_icon} {match_text}</span>'
            f'</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

def _render_fallback_recommendations(r: dict) -> None:
    st.markdown(
        '<div style="font-size:1.1rem;font-weight:800;color:#1A2420;margin:16px 0 4px">'
        '🌿 Energy Saving Recommendations</div>'
        '<p style="font-size:.87rem;color:#6B8F78;font-weight:500;margin-bottom:14px">'
        'Personalized tips based on your largest consumption contributors.</p>',
        unsafe_allow_html=True,
    )
    sorted_ap = sorted(
        [(ap, r["props"].get(ap["id"], 0)) for ap in APPLIANCES],
        key=lambda x: x[1], reverse=True,
    )
    count = 0
    fallback_tips = {
        "Air_Conditioning": ("❄️", "Optimize AC temperature", "Set to 24–26°C and use sleep mode at night to save up to 20% AC energy."),
        "Heater":           ("🔥", "Save on water heating",   "Consider heating water only when needed or switch to solar water heater."),
        "Fridge":           ("🧊", "Fridge efficiency",        "Set temperature to 3–5°C and avoid putting hot food directly inside."),
        "Computer":         ("💻", "Computer power",           "Enable auto-sleep after 10–15 minutes of inactivity."),
        "TV":               ("📺", "TV standby",               "Turn TV completely off — standby mode still consumes electricity."),
        "Washing_Machine":  ("🧺", "Washing machine",          "Wash with cold water — saves up to 90% energy per cycle."),
        "Lights":           ("💡", "Lighting",                 "Switch to LEDs and use natural daylight when possible."),
        "Dishwasher":       ("🍽️", "Dishwasher",              "Run only when full and use energy-saving mode."),
        "Oven":             ("🍞", "Oven usage",               "Cook multiple items at once and use residual heat."),
        "Microwave":        ("🍲", "Microwave",                "Prefer microwave over stove for heating small portions."),
    }
    for ap, prop in sorted_ap:
        if prop > 0 and ap["id"] in fallback_tips and count < 3:
            icon, title, tip = fallback_tips[ap["id"]]
            st.markdown(
                f'<div class="reco-card">'
                f'<div class="reco-icon">{icon}</div>'
                f'<div><div class="reco-title">{title}</div>'
                f'<div class="reco-text">{tip}</div></div></div>',
                unsafe_allow_html=True,
            )
            count += 1

# ── Insights ──────────────────────────────────────────────────
def _render_insights(r: dict) -> None:
    st.markdown(
        '<div style="font-size:1.1rem;font-weight:800;color:#1A2420;margin:16px 0 10px">'
        '💡 Interesting Insights</div>',
        unsafe_allow_html=True,
    )
    kpo_b = r["kwh_per_orang_bulan"]
    label = r["label"]
    if label == "hemat":
        msg = (f'🌱 Consumption per person (<b>{kpo_b:.1f} kWh/month</b>) is below the '
               f'average (~{AVG_KWH_ORANG_INDO:.0f}). Excellent — keep it up!')
    elif label == "boros":
        msg = (f'🔴 Consumption per person (<b>{kpo_b:.1f} kWh/month</b>) is well above the '
               f'average (~{AVG_KWH_ORANG_INDO:.0f}). Big saving potential!')
    else:
        msg = (f'⚡ Consumption per person (<b>{kpo_b:.1f} kWh/month</b>) is around the '
               f'average (~{AVG_KWH_ORANG_INDO:.0f}). A few tweaks can still help.')
    st.markdown(f'<div class="insight">{msg}</div>', unsafe_allow_html=True)

    co2 = r["kwh_bulan"] * FAKTOR_CO2
    st.markdown(
        f'<div class="insight">🌍 This month ~<b>{co2:.0f} kg CO₂</b> was generated. '
        f'It would take ~{co2/1.75:.0f} trees a month to absorb it! 🌳</div>',
        unsafe_allow_html=True,
    )


def _render_reset_button() -> None:
    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    if st.button("🔄 Analyze Again", type="secondary", key="btn_reset"):
        reset_state()
        st.rerun()