# EcoWatt AI
> **"Cek apakah rumahmu hemat listrik atau diam-diam boros!"**

Aplikasi berbasis web (Streamlit) yang dirancang untuk membantu masyarakat umum menganalisis tingkat efisiensi konsumsi listrik rumah tangga secara instan menggunakan kecerdasan buatan (*Machine Learning*).

Proyek ini dikembangkan untuk memenuhi tugas mata kuliah **Artificial Intelligence** di **Universitas Padjadjaran**.

---

## Tim Pengembang (Kelompok)
Susunan anggota kelompok pengembang EcoWatt AI:
1. **Athifah Ari Ghumaisha** - NPM: `140810240004`
2. **Vivian Azarine Widyatna** - NPM: `140810240014`
3. **Azhaar Fathin Tsuraya** - NPM: `140810240036`

---

## Cara Menjalankan Aplikasi

1. **Clone atau Unduh Repositori Ini**
2. **Install Dependensi/Library yang Diperlukan:**
   ```bash
   pip install -r requirements.txt

## Pipeline Feature Engineering (sesuai notebook)

| Langkah | Keterangan |
|---|---|
| Input user | kWh/bulan + jam pemakaian per alat |
| kWh perbulan | `kwh_bulan` |
| Estimasi kWh alat | `Watt × jam/hari × 365 / 1000` per alat |
| Proporsi | `kWh_alat / total_kWh_semua_alat` → `prop_*` |
| kwh_per_orang | `kwh_tahun / n_penghuni` |
| Normalisasi | `StandardScaler.transform()` |
| Prediksi | `model_tree.predict(X_scaled)` |


### Label keluaran model:
| Label | Badge di Web |
|---|---|
| `'hemat'` | Hijau — Hemat Energi |
| `'normal'` | Kuning — Konsumsi Normal |
| `'boros'` | Merah — Konsumsi Tinggi |

---

## Struktur Proyek

```
ecowatt_ai/
├── app.py                  ← entry point, cukup 48 baris
├── constants.py            ← WATT, APPLIANCES, FITUR_ML, RECO_DB, tarif
├── model.py                ← load_model(), build_features(), run_predict()
├── state.py                ← init_state(), reset_state(), go_to()
├── ui_components.py        ← CSS global, hero, step nav, footer
├── pages/
│   ├── step1_info.py       ← form jumlah penghuni & kWh
│   ├── step2_appliances.py ← checkbox + slider per alat
│   ├── step3_confirm.py    ← konfirmasi + loading + trigger prediksi
│   └── step4_result.py     ← status card, pie chart, rekomendasi
├── scaler_energi.pkl       ← taruh di sini
└── model_tree_energi.pkl   ← taruh di sini
```

