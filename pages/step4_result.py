# ============================================================
#  pages/step4_result.py
#  Step 4 — Analysis Results (status, charts, recommendations, insights)
# ============================================================

import streamlit as st
import plotly.graph_objects as go

from constants import (
    APPLIANCES, RECO_DB, TARIF_PLN,
    AVG_KWH_ORANG_INDO, FAKTOR_CO2,
)
from ui_components import render_steps
from state import reset_state

# Configuration for display based on model prediction label
_STATUS_CFG: dict[str, dict] = {
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
        _render_metrics(r)
        _render_pie_chart(r)
        _render_recommendations(r)
        _render_insights(r)
        _render_reset_button()


# ── Sub-renders ───────────────────────────────────────────────

def _render_metrics(r: dict) -> None:
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("⚡ kWh / month",      f"{r['kwh_bulan']:,}")
    with m2: st.metric("👤 kWh / person",     f"{r['kwh_per_orang_bulan']:.1f}")
    with m3: st.metric("💰 Estimated Bill", f"Rp {r['kwh_bulan'] * TARIF_PLN:,.0f}")
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


def _render_recommendations(r: dict) -> None:
    st.markdown(
        '<div style="font-size:1.1rem;font-weight:800;color:#1A2420;margin:8px 0 4px">'
        '🤖 Energy Saving Recommendations</div>'
        '<p style="font-size:.87rem;color:#6B8F78;font-weight:500;margin-bottom:14px">'
        'Personalized tips based on the largest consumption contributors in your home.</p>',
        unsafe_allow_html=True,
    )

    sorted_ap = sorted(
        [(ap, r["props"].get(ap["id"], 0)) for ap in APPLIANCES],
        key=lambda x: x[1], reverse=True,
    )
    count = 0
    for ap, prop in sorted_ap:
        if prop > 0 and ap["id"] in RECO_DB and count < 4:
            icon, title, tip = RECO_DB[ap["id"]]
            rp = r["est_bulan"][ap["id"]] * TARIF_PLN
            st.markdown(
                f'<div class="reco-card">'
                f'<div class="reco-icon">{icon}</div>'
                f'<div>'
                f'<div class="reco-title">{title}</div>'
                f'<div class="reco-pct">{prop*100:.1f}% consumption · ≈ Rp{rp:,.0f}/month</div>'
                f'<div class="reco-text">{tip}</div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
            count += 1

    if count == 0:
        st.info("Check appliances in Step 2 to receive personalized recommendations.")


def _render_insights(r: dict) -> None:
    st.markdown(
        '<div style="font-size:1.1rem;font-weight:800;color:#1A2420;margin:16px 0 10px">'
        '💡 Interesting Insights</div>',
        unsafe_allow_html=True,
    )
    kpo_b = r["kwh_per_orang_bulan"]
    if kpo_b < AVG_KWH_ORANG_INDO:
        st.markdown(
            f'<div class="insight">🌱 Consumption per person (<b>{kpo_b:.1f} kWh/month</b>) '
            f'is lower than average rata-rata Indonesia (~{AVG_KWH_ORANG_INDO:.0f} kWh/person). Great!</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="insight">⚡ Consumption per person is '
            f'<b>{kpo_b - AVG_KWH_ORANG_INDO:.1f} kWh/month</b> higher than the average rata-rata Indonesia. '
            f'There is still room to save!</div>',
            unsafe_allow_html=True,
        )
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