import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="🌱 EcoWatt AI", page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
:root{--mint:#7AE582;--mint-dk:#4EC95A;--mint-lt:#D4F7D7;--sky:#89CFF0;--sky-lt:#DCF0FB;--yellow:#FFE066;--bg:#F5FBF6;--card:#FFFFFF;--text:#1A2420;--muted:#6B8F78;--border:rgba(122,229,130,0.25);--shadow-sm:0 2px 12px rgba(74,180,82,0.10);--shadow-md:0 8px 32px rgba(74,180,82,0.15);--r:20px}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,.stApp{background:var(--bg);font-family:'Plus Jakarta Sans',sans-serif!important;color:var(--text)}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{visibility:hidden!important;display:none!important}
.block-container{padding:0!important;max-width:100%!important}
section[data-testid="stSidebar"]{display:none!important}
div[data-testid="stNumberInput"] input{border-radius:12px!important;border:2px solid var(--border)!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:1rem!important;font-weight:600!important;padding:10px 14px!important;background:white!important;transition:border-color .2s!important}
div[data-testid="stNumberInput"] input:focus{border-color:var(--mint-dk)!important;box-shadow:0 0 0 3px rgba(122,229,130,0.2)!important}
div[data-testid="stCheckbox"] label{font-family:'Plus Jakarta Sans',sans-serif!important;font-weight:700!important;font-size:.97rem!important;color:var(--text)!important}
div[data-testid="stSlider"]{padding:4px 0!important}
div[data-testid="stButton"]>button[kind="primary"]{background:linear-gradient(135deg,var(--mint),var(--mint-dk))!important;color:#1A2420!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-weight:800!important;font-size:1rem!important;padding:13px 36px!important;border-radius:50px!important;border:none!important;box-shadow:0 4px 20px rgba(122,229,130,.45)!important;transition:all .25s!important;width:100%!important}
div[data-testid="stButton"]>button[kind="primary"]:hover{box-shadow:0 8px 30px rgba(122,229,130,.6)!important;transform:translateY(-2px)!important}
div[data-testid="stButton"]>button[kind="secondary"]{background:white!important;color:var(--mint-dk)!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-weight:700!important;padding:10px 28px!important;border-radius:50px!important;border:2px solid var(--mint)!important;transition:all .2s!important;width:100%!important}
div[data-testid="stButton"]>button[kind="secondary"]:hover{background:var(--mint-lt)!important}
div[data-testid="stProgress"]>div{background:var(--mint-lt)!important;border-radius:50px!important;height:8px!important}
div[data-testid="stProgress"]>div>div{background:linear-gradient(90deg,var(--mint),var(--sky))!important;border-radius:50px!important}
div[data-testid="stMetric"]{background:white!important;border-radius:16px!important;padding:20px!important;border:1.5px solid var(--border)!important;box-shadow:var(--shadow-sm)!important}
div[data-testid="stMetricValue"]{font-family:'Plus Jakarta Sans',sans-serif!important;font-weight:900!important;font-size:1.8rem!important;color:var(--mint-dk)!important}
div[data-testid="stMetricLabel"]{font-family:'Plus Jakarta Sans',sans-serif!important;font-weight:600!important;color:var(--muted)!important}
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
.insight{background:linear-gradient(135deg,#F2FCF2,#E8F8EA);border:1.5px solid var(--mint);border-radius:16px;padding:16px 20px;margin-bottom:10px;font-size:.93rem;font-weight:600;color:var(--text);display:flex;gap:10px;align-items:center}
.pipeline-note{background:linear-gradient(135deg,#F3F0FF,#EDE8FF);border:1.5px solid #B197FC;border-radius:14px;padding:12px 18px;font-size:.83rem;color:#5534CC;font-weight:600;margin-bottom:20px}
.no-model-warn{background:linear-gradient(135deg,#FFF9E6,#FFF5C2);border:2px solid #FFD43B;border-radius:16px;padding:16px 20px;font-size:.9rem;color:#7A5A00;font-weight:600;margin-bottom:20px;text-align:center}
.footer{background:linear-gradient(135deg,#1A2420,#0F3328);color:#8EC9A0;text-align:center;padding:44px 20px;margin-top:60px}
.footer .ft-logo{font-size:1.5rem;font-weight:900;color:var(--mint);margin-bottom:4px}
.footer .ft-sub{font-size:.88rem;opacity:.75;margin-bottom:20px}
.footer a.gh{display:inline-flex;align-items:center;gap:8px;background:var(--mint);color:#1A2420;font-weight:800;font-size:.9rem;padding:10px 28px;border-radius:50px;text-decoration:none}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
</style>
""", unsafe_allow_html=True)

WATT = {"Air_Conditioning":900,"Fridge":150,"TV":100,"Computer":150,"Lights":60,"Heater":2000,"Dishwasher":1200,"Oven":2000,"Microwave":1000,"Washing_Machine":500}
APPLIANCES = [
    {"id":"Air_Conditioning","label":"Air Conditioner (AC)","emoji":"❄️","watt_desc":"900 W"},
    {"id":"Fridge","label":"Kulkas","emoji":"🧊","watt_desc":"150 W"},
    {"id":"TV","label":"Televisi","emoji":"📺","watt_desc":"100 W"},
    {"id":"Computer","label":"Komputer / Laptop","emoji":"💻","watt_desc":"150 W"},
    {"id":"Lights","label":"Lampu","emoji":"💡","watt_desc":"60 W"},
    {"id":"Heater","label":"Pemanas Air","emoji":"🔥","watt_desc":"2.000 W"},
    {"id":"Dishwasher","label":"Dishwasher","emoji":"🍽️","watt_desc":"1.200 W"},
    {"id":"Oven","label":"Oven","emoji":"🍞","watt_desc":"2.000 W"},
    {"id":"Microwave","label":"Microwave","emoji":"🍲","watt_desc":"1.000 W"},
    {"id":"Washing_Machine","label":"Mesin Cuci","emoji":"🧺","watt_desc":"500 W"},
]
FITUR_ML= [
    "total_kwh_tahun",
    "household_size",
    "avg_temp",
    "kwh_Air_Conditioning", "kwh_Computer",  "kwh_Dishwasher",
    "kwh_Fridge",           "kwh_Heater",    "kwh_Lights",
    "kwh_Microwave",        "kwh_Oven",       "kwh_TV",
    "kwh_Washing_Machine",
    "prop_Air_Conditioning","prop_Computer",  "prop_Dishwasher",
    "prop_Fridge",          "prop_Heater",    "prop_Lights",
    "prop_Microwave",       "prop_Oven",       "prop_TV",
    "prop_Washing_Machine",
    "kwh_per_orang",
]
RECO_DB = {
    "Air_Conditioning":("❄️","Optimalkan suhu AC","Atur suhu di <b>24–26°C</b> — setiap 1°C lebih hangat hemat ~6% listrik."),
    "Heater":("🔥","Hemat di pemanas air","Pertimbangkan <b>pemanas air tenaga surya</b> atau mandi tanpa pemanas di siang hari."),
    "Oven":("🍞","Masak cerdas dengan oven","<b>Masak beberapa bahan sekaligus</b> dan manfaatkan sisa panas oven setelah dimatikan."),
    "Dishwasher":("🍽️","Optimalkan dishwasher","Gunakan hanya saat <b>penuh</b> dan pilih mode hemat energi."),
    "Washing_Machine":("🧺","Cuci lebih cerdas","Cuci dengan <b>air dingin</b> — bisa hemat hingga 90% energi per siklus."),
    "Fridge":("🧊","Jaga efisiensi kulkas","Atur suhu di <b>3–5°C</b>. Tutup pintu rapat dan jangan masukkan makanan panas."),
    "Computer":("💻","Hemat daya komputer","Aktifkan <b>sleep otomatis</b> setelah 10–15 menit idle."),
    "TV":("📺","Tonton TV lebih hemat","Matikan TV <b>sepenuhnya</b> (bukan standby). Mode standby tetap menyedot listrik!"),
    "Lights":("💡","Maksimalkan cahaya alami","Ganti ke <b>LED</b> dan manfaatkan sinar matahari."),
    "Microwave":("🍲","Microwave > kompor","Microwave lebih <b>hemat energi</b> dari kompor untuk memanaskan porsi kecil."),
}

def init_state():
    defaults = {"step":1,"n_penghuni":3,"kwh_bulan":250,
                "usage_hours":{ap["id"]:0 for ap in APPLIANCES},
                "checked":{ap["id"]:False for ap in APPLIANCES},"result":None}
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v
init_state()

@st.cache_resource
def load_model():
    import os
    if os.path.exists("scaler_energi.pkl") and os.path.exists("model_tree_energi.pkl"):
        import joblib
        return joblib.load("scaler_energi.pkl"), joblib.load("model_tree_energi.pkl")
    return None, None

def run_predict(X_df):
    scaler, model = load_model()
    if scaler is None or model is None: 
        return None
        
    # Ambil nilai mentahnya saja (.values) sebagai array 2D 
    # untuk menghindari error perbedaan nama/urutan kolom dengan model pkl
    X_array = X_df.values 
    
    # Lakukan transformasi dan prediksi menggunakan array mentah
    scaled_data = scaler.transform(X_array)
    return model.predict(scaled_data)[0]

# Pastikan fungsi build_features diubah menjadi seperti ini:
def build_features(kwh_bulan, n_penghuni, usage_hours):
    kwh_tahun = kwh_bulan * 12
    
    # Buat seluruh kemungkinan fitur terlebih dahulu
    features = {
        "total_kwh_tahun": float(kwh_tahun),
        "household_size": float(n_penghuni),
        "avg_temp": 27.0, 
        "kwh_per_orang": float(kwh_tahun / n_penghuni)
    }
    
    est_kwh_alat_tahunan = {}
    for ap in APPLIANCES:
        aid = ap["id"]
        kwh_alat = (WATT[aid] * usage_hours.get(aid, 0) * 365) / 1000
        est_kwh_alat_tahunan[aid] = kwh_alat
        features[f"kwh_{aid}"] = float(kwh_alat)
        
    total_est_tahunan = sum(est_kwh_alat_tahunan.values())
    for ap in APPLIANCES:
        aid = ap["id"]
        if total_est_tahunan > 0:
            features[f"prop_{aid}"] = float(est_kwh_alat_tahunan[aid] / total_est_tahunan)
        else:
            features[f"prop_{aid}"] = 0.0

    df_pred = pd.DataFrame([features])
    
    # KUNCI UTAMA: Ambil daftar nama fitur asli dari scaler bawaan .pkl
    scaler, _ = load_model()
    if scaler is not None and hasattr(scaler, "feature_names_in_"):
        fitur_asli_model = scaler.feature_names_in_
        # Filter df_pred hanya menggunakan 11 fitur yang dikenali model pkl
        return df_pred[fitur_asli_model]
    else:
        # Fallback jika model belum di-load (menggunakan FITUR_ML bawaan)
        return df_pred[[f for f in FITUR_ML if f in df_pred.columns]]

# ── KEY FIX: build full HTML string first, then ONE st.markdown call ──
def render_steps(current):
    steps = [("🏠","Informasi"),("🔌","Peralatan"),("✅","Konfirmasi"),("📊","Hasil")]
    parts = ['<div class="step-nav">']
    for i, (icon, label) in enumerate(steps, 1):
        if i < current:   cc, cl = "done", ""
        elif i == current: cc, cl = "active", "active"
        else:              cc, cl = "todo", ""
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

def render_hero():
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
        '✨ Cek apakah rumahmu hemat listrik atau diam-diam boros!</div>'
        '<div style="font-size:clamp(2rem,5vw,3.2rem);font-weight:900;'
        'background:linear-gradient(135deg,#2EA89E,#1C7ED6);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px">🌱 EcoWatt AI</div>'
        '<p style="font-size:clamp(.9rem,2vw,1.1rem);color:#5C8A7A;max-width:560px;'
        'margin:0 auto;line-height:1.7;font-weight:500">'
        'Temukan profil konsumsi listrik rumahmu menggunakan kecerdasan buatan '
        'dan dapatkan rekomendasi hemat energi yang dipersonalisasi.</p>'
        '</div></div>',
        unsafe_allow_html=True
    )

def step1():
    render_hero()
    render_steps(1)
    st.markdown(
        '<div class="section-wrap"><div class="section-head">'
        '<div class="icon">🏠</div><h2>Informasi Rumah Tangga</h2>'
        '<p>Ceritakan sedikit tentang rumahmu — ini hanya butuh 30 detik!</p>'
        '</div></div>', unsafe_allow_html=True)
    _, col_m, _ = st.columns([1,3,1])
    with col_m:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**👥 Berapa orang yang tinggal di rumah?**")
        n = st.number_input("Penghuni", min_value=1, max_value=15,
                            value=st.session_state.n_penghuni,
                            label_visibility="collapsed", key="inp_penghuni")
        st.caption("Hitung semua yang tinggal di rumah, termasuk anak kecil ya!")
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown("**⚡ Konsumsi listrik bulan lalu (kWh)**")
        kwh = st.number_input("kWh", min_value=10, max_value=5000,
                              value=st.session_state.kwh_bulan,
                              label_visibility="collapsed", key="inp_kwh")
        st.markdown(
            '<div class="info-pill">💡 Cek di tagihan PLN atau aplikasi PLN Mobile</div>'
            '<div style="font-size:.8rem;color:#6B8F78;margin-top:8px;font-weight:500">'
            'Contoh: 150 kWh (kecil) · 250 kWh (sedang) · 450 kWh (besar)</div>',
            unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        if st.button("➡️ Lanjutkan ke Peralatan", type="primary", key="btn_s1"):
            st.session_state.n_penghuni = n
            st.session_state.kwh_bulan = kwh
            st.session_state.step = 2
            st.rerun()

def step2():
    render_steps(2)
    st.markdown(
        '<div class="section-wrap"><div class="section-head">'
        '<div class="icon">🔌</div><h2>Peralatan Elektronik</h2>'
        '<p>Centang alat yang kamu punya, lalu geser jam pemakaian per hari.</p>'
        '</div></div>', unsafe_allow_html=True)
    
    # --- CATATAN TEMPLATE WATT ---
    _, col_note, _ = st.columns([1,4,1])
    with col_note:
        st.info("💡 **Catatan:** Konsumsi daya (Watt) di bawah ini menggunakan nilai template rata-rata standar. "
                "Konsumsi riil di rumah Anda mungkin berbeda tergantung merek dan spesifikasi alat.")
    # ---------------------------------------------
    _, col_m, _ = st.columns([1,4,1])
    with col_m:
        for ap in APPLIANCES:
            aid = ap["id"]
            is_on = st.session_state.checked.get(aid, False)
            card_cls = "ap-card active" if is_on else "ap-card"
            st.markdown(f'<div class="{card_cls}">', unsafe_allow_html=True)
            chk = st.checkbox(f"{ap['emoji']} **{ap['label']}**  ·  `{ap['watt_desc']}`",
                              value=is_on, key=f"chk_{aid}")
            st.session_state.checked[aid] = chk
            if chk:
                cur_h = st.session_state.usage_hours.get(aid, 4)
                h = st.slider("⏱ Jam penggunaan per hari", min_value=0, max_value=24,
                              value=cur_h, key=f"sl_{aid}", format="%d jam")
                st.session_state.usage_hours[aid] = h
                est_kwh_bulan = (WATT[aid] * h * 30) / 1000
                st.markdown(
                    f'<div style="font-size:.8rem;color:#4EC95A;font-weight:700;margin-top:4px">'
                    f'≈ {est_kwh_bulan:.1f} kWh/bulan</div>', unsafe_allow_html=True)
            else:
                st.session_state.usage_hours[aid] = 0
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        cb, cn = st.columns(2)
        with cb:
            if st.button("⬅️ Kembali", type="secondary", key="btn_s2b"):
                st.session_state.step = 1; st.rerun()
        with cn:
            if st.button("➡️ Konfirmasi Data", type="primary", key="btn_s2"):
                st.session_state.step = 3; st.rerun()

def step3():
    render_steps(3)
    st.markdown(
        '<div class="section-wrap"><div class="section-head">'
        '<div class="icon">🤖</div><h2>Konfirmasi Data</h2>'
        '<p>Pastikan data di bawah sudah benar sebelum dianalisis.</p>'
        '</div></div>', unsafe_allow_html=True)
    _, col_m, _ = st.columns([1,4,1])
    with col_m:
        est_tag = st.session_state.kwh_bulan * 1444.70
        st.markdown(
            '<div class="card"><strong>🏠 Informasi Rumah</strong>'
            f'<div class="confirm-row"><span class="key">👥 Jumlah Penghuni</span><span class="val">{st.session_state.n_penghuni} orang</span></div>'
            f'<div class="confirm-row"><span class="key">⚡ Konsumsi Bulan Lalu</span><span class="val">{st.session_state.kwh_bulan} kWh</span></div>'
            f'<div class="confirm-row"><span class="key">💰 Estimasi Tagihan</span><span class="val">Rp {est_tag:,.0f}</span></div>'
            '</div>', unsafe_allow_html=True)
        aktif = [(ap, st.session_state.usage_hours.get(ap["id"], 0))
                 for ap in APPLIANCES if st.session_state.checked.get(ap["id"], False)]
        if aktif:
            rows = "".join(
                f'<div class="confirm-row"><span class="key">{ap["emoji"]} {ap["label"]}</span>'
                f'<span class="val">{jam} jam/hari · ≈{(WATT[ap["id"]]*jam*30)/1000:.1f} kWh/bln</span></div>'
                for ap, jam in aktif)
            st.markdown(f'<div class="card"><strong>🔌 Peralatan yang Dipilih</strong>{rows}</div>',
                        unsafe_allow_html=True)
        else:
            st.info("⚠️ Belum ada peralatan yang dipilih.")
        scaler, model = load_model()
        if scaler is None:
            st.markdown(
                '<div class="no-model-warn">⚠️ <b>Model AI belum terhubung.</b><br>'
                'Letakkan <code>scaler_energi.pkl</code> dan <code>model_tree_energi.pkl</code> '
                'di folder yang sama dengan <code>app.py</code>, lalu restart.<br>'
                '<span style="font-size:.8rem;opacity:.8">File .pkl dari notebook AI_Energi_baru_fix.ipynb (Tahap 12).</span>'
                '</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        cb, cn = st.columns(2)
        with cb:
            if st.button("⬅️ Edit Peralatan", type="secondary", key="btn_s3b"):
                st.session_state.step = 2; st.rerun()
        with cn:
            if st.button("🔍 Analisis Rumah Saya", type="primary", key="btn_s3"):
                if scaler is None:
                    st.error("❌ Model belum tersedia.")
                else:
                    run_analysis()

def run_analysis():
    ph = st.empty()
    msgs = [
        "🤖 EcoWatt AI sedang menganalisis rumah Anda...",
        "📊 Menghitung proporsi konsumsi energi...",
        "🌿 Menyiapkan rekomendasi personal..."
    ]
    
    for i, msg in enumerate(msgs):
        with ph.container():
            # Pembungkus dengan CSS yang memaksa seluruh komponen di dalamnya rata tengah secara absolut
            st.markdown(
                f"""
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin: 30px auto; max-width: 500px;">
                    <div style="font-size: 4rem; margin-bottom: 10px; animation: float 1.5s ease-in-out infinite;">🤖</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #2EA89E; margin-bottom: 20px; line-height: 1.5;">{msg}</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Kita gunakan trik column kosong [lebar_kiri, lebar_tengah, lebar_kanan] 
            # untuk memaksa progress bar bawaan streamlit berada di tengah grid.
            col_kiri, col_tengah, col_kanan = st.columns([1, 6, 1])
            with col_tengah:
                st.progress((i + 1) / len(msgs))
                
            st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
            
        time.sleep(0.9)
    ph.empty()
    
    # Proses pembentukan fitur dan prediksi berjalan di bawah ini
    X_df = build_features(st.session_state.kwh_bulan, st.session_state.n_penghuni, st.session_state.usage_hours)
    label = run_predict(X_df)
    kwh_tahun = st.session_state.kwh_bulan * 12
    est = {ap["id"]: (WATT[ap["id"]] * st.session_state.usage_hours.get(ap["id"], 0) * 365) / 1000 for ap in APPLIANCES}
    total_est = sum(est.values())
    props = ({k: v/total_est for k,v in est.items()} if total_est > 0 else {ap["id"]: 0.0 for ap in APPLIANCES})
    st.session_state.result = {
        "label": label, "kwh_bulan": st.session_state.kwh_bulan, "kwh_tahun": kwh_tahun,
        "kwh_per_orang_bulan": (kwh_tahun / st.session_state.n_penghuni) / 12,
        "n_penghuni": st.session_state.n_penghuni,
        "est_bulan": {k: v/12 for k,v in est.items()}, "props": props,
    }
    st.session_state.step = 4
    st.rerun()

def step4():
    render_steps(4)
    r = st.session_state.result
    st.markdown(
        '<div style="max-width:740px;margin:0 auto;padding:8px 20px 0;text-align:center">'
        '<div style="font-size:1.7rem;font-weight:900;color:#1A2420;margin-bottom:4px">📊 Hasil Analisis EcoWatt AI</div>'
        '<p style="color:#6B8F78;font-weight:500;font-size:.95rem">Berikut profil konsumsi listrik rumahmu.</p>'
        '</div>', unsafe_allow_html=True)
    label = r["label"]
    _, col_m, _ = st.columns([1,4,1])
    with col_m:
        if label is None:
            bc,he,bt,hm = "normal","❓","— Prediksi Tidak Tersedia","Model AI belum diintegrasikan."
            st.markdown(
                '<div class="no-model-warn" style="margin-bottom:20px">⚠️ <b>Hasil prediksi tidak tersedia</b> — model AI belum terhubung.<br>'
                '<span style="font-size:.82rem">Upload <code>scaler_energi.pkl</code> + <code>model_tree_energi.pkl</code> ke folder <code>app.py</code> dan restart.</span></div>',
                unsafe_allow_html=True)
        elif label == "hemat": bc,he,bt,hm = "hemat","🏆","✅ Hemat Energi","Rumahmu termasuk <b>hemat listrik</b>! 🌿"
        elif label == "normal": bc,he,bt,hm = "normal","⚡","🟡 Konsumsi Normal","Pemakaian <b>cukup normal</b>. Ada hal kecil yang bisa ditingkatkan!"
        else: bc,he,bt,hm = "boros","🚨","🔴 Konsumsi Tinggi","Pemakaian <b>cukup tinggi</b>. Lihat rekomendasi di bawah! 💪"
        st.markdown(
            f'<div class="status-card {bc}">'
            f'<div class="status-emoji">{he}</div>'
            f'<div class="status-label badge-{bc}">{bt}</div>'
            f'<h2>Status Efisiensi Rumahmu</h2><p>{hm}</p></div>', unsafe_allow_html=True)
        pl = f"→ label: <b>{label}</b>" if label else "→ <i>model belum tersedia</i>"
        
        m1,m2,m3 = st.columns(3)
        with m1: st.metric("⚡ kWh / bulan", f"{r['kwh_bulan']:,}")
        with m2: st.metric("👤 kWh / orang", f"{r['kwh_per_orang_bulan']:.1f}")
        with m3: st.metric("💰 Estimasi Tagihan", f"Rp {r['kwh_bulan']*1444.70:,.0f}")
        st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)
        pie_labels, pie_vals = [], []
        for ap in APPLIANCES:
            v = r["est_bulan"][ap["id"]]
            if v > 0: pie_labels.append(f"{ap['emoji']} {ap['label']}"); pie_vals.append(v)
        if pie_vals:
            st.markdown(
                '<div style="font-size:1.1rem;font-weight:800;color:#1A2420;margin-bottom:4px">🥧 Proporsi Konsumsi Energi</div>'
                '<p style="font-size:.87rem;color:#6B8F78;font-weight:500;margin-bottom:12px">Estimasi kontribusi tiap peralatan.</p>',
                unsafe_allow_html=True)
            colors = ["#7AE582","#89CFF0","#FFE066","#FF8FA3","#A9E34B","#FFA94D","#CC5DE8","#20C997","#FF6B6B","#74C0FC"]
            fig = go.Figure(go.Pie(labels=pie_labels, values=pie_vals, hole=.44,
                marker=dict(colors=colors, line=dict(color="white", width=2.5)),
                textinfo="label+percent",
                hovertemplate="%{label}<br><b>%{value:.1f} kWh/bulan</b><extra></extra>"))
            fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10), height=360,
                paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Plus Jakarta Sans, sans-serif", size=13),
                annotations=[dict(text="⚡", x=.5, y=.5, font_size=22, showarrow=False)])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tidak ada peralatan yang dipilih — grafik tidak tersedia.")
        sorted_ap = sorted([(ap, r["props"].get(ap["id"], 0)) for ap in APPLIANCES], key=lambda x: x[1], reverse=True)
        st.markdown(
            '<div style="font-size:1.1rem;font-weight:800;color:#1A2420;margin:8px 0 4px">🤖 Rekomendasi Hemat Energi</div>'
            '<p style="font-size:.87rem;color:#6B8F78;font-weight:500;margin-bottom:14px">Tips personal berdasarkan proporsi terbesar.</p>',
            unsafe_allow_html=True)
        count = 0
        for ap, prop in sorted_ap:
            if prop > 0 and ap["id"] in RECO_DB and count < 4:
                icon, title, tip = RECO_DB[ap["id"]]
                rp = r["est_bulan"][ap["id"]] * 1444.70
                st.markdown(
                    f'<div class="reco-card"><div class="reco-icon">{icon}</div><div>'
                    f'<div class="reco-title">{title}</div>'
                    f'<div class="reco-pct">{prop*100:.1f}% konsumsi · ≈ Rp{rp:,.0f}/bulan</div>'
                    f'<div class="reco-text">{tip}</div></div></div>', unsafe_allow_html=True)
                count += 1
        if count == 0: st.info("Centang peralatan di Langkah 2 untuk mendapat rekomendasi personal.")
        st.markdown('<div style="font-size:1.1rem;font-weight:800;color:#1A2420;margin:16px 0 10px">💡 Insight Menarik</div>', unsafe_allow_html=True)
        kpo_b = r["kwh_per_orang_bulan"]
        if kpo_b < 100:
            st.markdown(f'<div class="insight">🌱 Konsumsi per orang (<b>{kpo_b:.1f} kWh/bulan</b>) lebih rendah dari rata-rata Indonesia (~100 kWh/orang). Keren!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="insight">⚡ Konsumsi per orang lebih tinggi <b>{kpo_b-100:.1f} kWh/bulan</b> dari rata-rata Indonesia. Masih ada potensi hemat!</div>', unsafe_allow_html=True)
        co2 = r["kwh_bulan"] * 0.87
        st.markdown(f'<div class="insight">🌍 Bulan ini ~<b>{co2:.0f} kg CO₂</b> dihasilkan. Butuh ~{co2/1.75:.0f} pohon untuk menyerapnya! 🌳</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        if st.button("🔄 Analisis Ulang", type="secondary", key="btn_reset"):
            st.session_state.step = 1; st.session_state.result = None
            st.session_state.checked = {ap["id"]: False for ap in APPLIANCES}
            st.session_state.usage_hours = {ap["id"]: 0 for ap in APPLIANCES}
            st.rerun()

step = st.session_state.step
if   step == 1: step1()
elif step == 2: step2()
elif step == 3: step3()
elif step == 4: step4()

st.markdown(
    '<div class="footer"><div class="ft-logo">🌱 EcoWatt AI</div>'
    '<div class="ft-sub">Proyek Mata Kuliah Artificial Intelligence<br><strong>Universitas Padjadjaran</strong></div>'
    '<a class="gh" href="https://github.com/" target="_blank">⭐ Lihat di GitHub</a>'
    '<div style="margin-top:18px;font-size:.78rem;opacity:.5">Made with ❤️ + 🤖 · © 2026 EcoWatt AI</div>'
    '</div>', unsafe_allow_html=True)