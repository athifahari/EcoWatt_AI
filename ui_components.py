# ============================================================
#  ui_components.py
#  UI components used across multiple steps:
#  Global CSS, hero banner, step navigator
# ============================================================

import streamlit as st


# ── Global CSS ───────────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
:root{
  --mint:#7AE582;--mint-dk:#4EC95A;--mint-lt:#D4F7D7;
  --sky:#89CFF0;--sky-lt:#DCF0FB;--yellow:#FFE066;
  --bg:#F5FBF6;--card:#FFFFFF;--text:#1A2420;--muted:#6B8F78;
  --border:rgba(122,229,130,0.25);
  --shadow-sm:0 2px 12px rgba(74,180,82,0.10);
  --shadow-md:0 8px 32px rgba(74,180,82,0.15);
  --r:20px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,.stApp{background:var(--bg);font-family:'Plus Jakarta Sans',sans-serif!important;color:var(--text)}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{visibility:hidden!important;display:none!important}
.block-container{padding:0!important;max-width:100%!important}
section[data-testid="stSidebar"]{display:none!important}

div[data-testid="stNumberInput"] input{
  border-radius:12px!important;border:2px solid var(--border)!important;
  font-family:'Plus Jakarta Sans',sans-serif!important;font-size:1rem!important;
  font-weight:600!important;padding:10px 14px!important;background:white!important;
  transition:border-color .2s!important}
div[data-testid="stNumberInput"] input:focus{
  border-color:var(--mint-dk)!important;box-shadow:0 0 0 3px rgba(122,229,130,0.2)!important}
div[data-testid="stCheckbox"] label{
  font-family:'Plus Jakarta Sans',sans-serif!important;font-weight:700!important;
  font-size:.97rem!important;color:var(--text)!important}
div[data-testid="stSlider"]{padding:4px 0!important}

div[data-testid="stButton"]>button[kind="primary"]{
  background:linear-gradient(135deg,var(--mint),var(--mint-dk))!important;
  color:#1A2420!important;font-family:'Plus Jakarta Sans',sans-serif!important;
  font-weight:800!important;font-size:1rem!important;padding:13px 36px!important;
  border-radius:50px!important;border:none!important;
  box-shadow:0 4px 20px rgba(122,229,130,.45)!important;
  transition:all .25s!important;width:100%!important}
div[data-testid="stButton"]>button[kind="primary"]:hover{
  box-shadow:0 8px 30px rgba(122,229,130,.6)!important;transform:translateY(-2px)!important}
div[data-testid="stButton"]>button[kind="secondary"]{
  background:white!important;color:var(--mint-dk)!important;
  font-family:'Plus Jakarta Sans',sans-serif!important;font-weight:700!important;
  padding:10px 28px!important;border-radius:50px!important;
  border:2px solid var(--mint)!important;transition:all .2s!important;width:100%!important}
div[data-testid="stButton"]>button[kind="secondary"]:hover{background:var(--mint-lt)!important}

div[data-testid="stProgress"]>div{
  background:var(--mint-lt)!important;border-radius:50px!important;height:8px!important}
div[data-testid="stProgress"]>div>div{
  background:linear-gradient(90deg,var(--mint),var(--sky))!important;border-radius:50px!important}

div[data-testid="stMetric"]{
  background:white!important;border-radius:16px!important;padding:20px!important;
  border:1.5px solid var(--border)!important;box-shadow:var(--shadow-sm)!important}
div[data-testid="stMetricValue"]{
  font-family:'Plus Jakarta Sans',sans-serif!important;font-weight:900!important;
  font-size:1.8rem!important;color:var(--mint-dk)!important}
div[data-testid="stMetricLabel"]{
  font-family:'Plus Jakarta Sans',sans-serif!important;font-weight:600!important;color:var(--muted)!important}

.ap-card{background:white;border:2px solid var(--border);border-radius:18px;padding:18px 20px;margin-bottom:12px}
.ap-card.active{border-color:var(--mint);box-shadow:0 4px 20px rgba(122,229,130,.2);background:linear-gradient(135deg,#FAFFFE,#F2FCF2)}

.step-nav{display:flex;align-items:center;justify-content:center;gap:0;padding:24px 20px 0;max-width:700px;margin:0 auto}
.step-item{display:flex;flex-direction:column;align-items:center;gap:6px;flex:1}
.step-circle{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.95rem;border:2.5px solid transparent}
.step-circle.done{background:var(--mint);color:#1A2420;border-color:var(--mint-dk)}
.step-circle.active{background:white;color:var(--mint-dk);border-color:var(--mint-dk);box-shadow:0 0 0 4px rgba(122,229,130,.25)}
.step-circle.todo{background:#F0F0F0;color:#AAAAAA;border-color:#E0E0E0}
.step-label{font-size:.72rem;font-weight:700;text-align:center;color:var(--muted);letter-spacing:.03em;text-transform:uppercase}
.step-label.active{color:var(--mint-dk)}
.step-line{height:2.5px;flex:1;background:#E8EEE9;margin-bottom:22px;border-radius:2px}
.step-line.done{background:var(--mint)}

.section-wrap{max-width:740px;margin:0 auto;padding:28px 20px 40px}
.section-head{text-align:center;margin-bottom:28px}
.section-head .icon{font-size:2.8rem;margin-bottom:8px}
.section-head h2{font-size:1.6rem;font-weight:900;color:var(--text);margin-bottom:6px}
.section-head p{font-size:.95rem;color:var(--muted);font-weight:500}
.card{background:white;border-radius:var(--r);border:1.5px solid var(--border);box-shadow:var(--shadow-sm);padding:24px;margin-bottom:16px}
.info-pill{display:inline-flex;align-items:center;gap:6px;background:var(--sky-lt);color:#1A5C8A;font-size:.83rem;font-weight:600;padding:6px 14px;border-radius:50px;border:1px solid var(--sky);margin-top:10px}
.confirm-row{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #F0F5F0;font-size:.93rem}
.confirm-row:last-child{border-bottom:none}
.confirm-row .key{color:var(--muted);font-weight:600}
.confirm-row .val{font-weight:800;color:var(--text)}

.badge-hemat{background:#D4F7D7;color:#1B6B25}
.badge-normal{background:#FFF5C2;color:#7A5A00}
.badge-boros{background:#FFE0E6;color:#8B1A30}
.status-card{border-radius:24px;padding:36px 28px;text-align:center;margin-bottom:24px}
.status-card.hemat{background:linear-gradient(135deg,#E8FDE8,#C8F5CC);border:2px solid #7AE582}
.status-card.normal{background:linear-gradient(135deg,#FFFBEA,#FFF5C2);border:2px solid #FFE066}
.status-card.boros{background:linear-gradient(135deg,#FFF0F3,#FFE0E6);border:2px solid #FF8FA3}
.status-emoji{font-size:4rem;margin-bottom:12px}
.status-label{display:inline-flex;align-items:center;gap:8px;font-size:1.2rem;font-weight:900;padding:8px 24px;border-radius:50px;margin-bottom:12px}
.status-card h2{font-size:1.5rem;font-weight:900;color:var(--text);margin-bottom:8px}
.status-card p{color:var(--muted);font-size:.97rem;font-weight:500}

.reco-card{background:white;border:1.5px solid var(--border);border-radius:18px;padding:18px 20px;margin-bottom:12px;display:flex;gap:14px;align-items:flex-start;box-shadow:var(--shadow-sm)}
.reco-icon{font-size:2rem;flex-shrink:0}
.reco-title{font-weight:800;font-size:.97rem;color:var(--text);margin-bottom:4px}
.reco-pct{font-size:.8rem;font-weight:700;color:var(--mint-dk);background:var(--mint-lt);padding:2px 10px;border-radius:50px;display:inline-block;margin-bottom:6px}
.reco-text{font-size:.88rem;color:var(--muted);line-height:1.6;font-weight:500}

.insight{background:linear-gradient(135deg,#F2FCF2,#E8F8EA);border:1.5px solid #7AE582;border-radius:16px;padding:16px 20px;margin-bottom:10px;font-size:.93rem;font-weight:600;color:var(--text);display:flex;gap:10px;align-items:center}
.no-model-warn{background:linear-gradient(135deg,#FFF9E6,#FFF5C2);border:2px solid #FFD43B;border-radius:16px;padding:16px 20px;font-size:.9rem;color:#7A5A00;font-weight:600;margin-bottom:20px;text-align:center}
.model-ok{background:#E8FDE8;border:1.5px solid #7AE582;border-radius:12px;padding:10px 16px;font-size:.85rem;color:#1B6B25;font-weight:600;margin-bottom:12px}

.footer{background:linear-gradient(135deg,#1A2420,#0F3328);color:#8EC9A0;text-align:center;padding:44px 20px;margin-top:60px}
.footer .ft-logo{font-size:1.5rem;font-weight:900;color:var(--mint);margin-bottom:4px}
.footer .ft-sub{font-size:.88rem;opacity:.75;margin-bottom:20px}
.footer a.gh{display:inline-flex;align-items:center;gap:8px;background:var(--mint);color:#1A2420;font-weight:800;font-size:.9rem;padding:10px 28px;border-radius:50px;text-decoration:none}

@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
</style>
"""


def inject_css() -> None:
    """Inject global CSS into the page. Call once in app.py."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_hero() -> None:
    """Hero banner at the top of the page (step 1 only)."""
    st.markdown(
        '<div style="background:linear-gradient(135deg,#E8FDE8 0%,#D4F7D7 40%,#DCF0FB 100%);'
        'padding:56px 24px 40px;text-align:center;position:relative;overflow:hidden;'
        'border-bottom:2px solid rgba(122,229,130,.3)">'
        '<div style="position:absolute;top:-60px;right:-60px;width:260px;height:260px;'
        'background:radial-gradient(circle,rgba(137,207,240,.35),transparent 70%);border-radius:50%"></div>'
        '<div style="position:relative">'
        '<div style="font-size:3rem;margin-bottom:12px;animation:float 3s ease-in-out infinite">🌱⚡🏠🤖</div>'
        '<div style="display:inline-block;background:#FFE066;color:#7A5A00;font-weight:800;'
        'font-size:.85rem;padding:5px 18px;border-radius:50px;margin-bottom:14px">'
        '✨ Check if your home is energy efficient or secretly wasteful!</div>'
        '<div style="font-size:clamp(2rem,5vw,3.2rem);font-weight:900;'
        'background:linear-gradient(135deg,#2EA89E,#1C7ED6);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px">🌱 EcoWatt AI</div>'
        '<p style="font-size:clamp(.9rem,2vw,1.1rem);color:#5C8A7A;max-width:560px;'
        'margin:0 auto;line-height:1.7;font-weight:500">'
        'Discover your household electricity consumption profile using AI '
        'and get personalized energy-saving recommendations.</p>'
        '</div></div>',
        unsafe_allow_html=True,
    )


def render_steps(current: int) -> None:
    """
    Step navigator (1–4). Build entire HTML first, then one
    st.markdown() call — prevents raw HTML from leaking as text.
    """
    steps = [("🏠", "Info"), ("🔌", "Appliances"), ("✅", "Confirm"), ("📊", "Results")]
    parts = ['<div class="step-nav">']
    for i, (icon, label) in enumerate(steps, 1):
        if i < current:    cc, cl = "done",   ""
        elif i == current: cc, cl = "active", "active"
        else:              cc, cl = "todo",   ""
        inner = icon if i < current else str(i)
        parts.append(
            '<div class="step-item">'
            f'<div class="step-circle {cc}">{inner}</div>'
            f'<div class="step-label {cl}">{label}</div>'
            '</div>'
        )
        if i < len(steps):
            lc = "done" if i < current else ""
            parts.append(f'<div class="step-line {lc}"></div>')
    parts.append('</div><div style="height:8px"></div>')
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_footer() -> None:
    """Page footer."""
    st.markdown(
        '<div class="footer">'
        '<div class="ft-logo">🌱 EcoWatt AI</div>'
        '<div class="ft-sub">Artificial Intelligence Course Project<br>'
        '<strong>Universitas Padjadjaran</strong></div>'
        '<a class="gh" href="https://github.com/athifahari/EcoWatt_AI" target="_blank">⭐ View on GitHub</a>'
        '<div style="margin-top:18px;font-size:.78rem;opacity:.5">'
        'Made with ❤️ © 2026 EcoWatt AI</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def section_header(icon: str, title: str, subtitle: str) -> None:
    """Standard section header (large icon + title + sub)."""
    st.markdown(
        f'<div class="section-wrap"><div class="section-head">'
        f'<div class="icon">{icon}</div>'
        f'<h2>{title}</h2>'
        f'<p>{subtitle}</p>'
        f'</div></div>',
        unsafe_allow_html=True,
    )