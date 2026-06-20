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
   ```


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


## Dataset & Analisis Bias

### Sumber & Sifat Data
- **Sumber:** Kaggle — *Smart Home Energy Consumption* (`mexwell/smart-home-energy-consumption`).
- **Ukuran:** 500 rumah, 100.000 baris, periode 1 tahun (2023).
- **Granularitas:** tiap baris = catatan satu peralatan pada satu waktu (kWh).
- **Sifat:** dataset **sintetis** — bukan data tagihan PLN asli. Digunakan untuk membuktikan metodologi, bukan sebagai sumber nilai absolut.

### Pra-pemrosesan (Agregasi)
- Diagregasi ke **1 baris per rumah** (total kWh setahun di-`sum`).
- `Household Size` diambil dengan **modus** per rumah (nilainya tidak konsisten antar baris pada data asli).
- Fitur clustering: `kwh_per_orang` + proporsi peralatan (`prop_*`).
- Label `hemat / normal / boros` dihasilkan via **clustering (K-Means)**, lalu dipakai melatih **Decision Tree** untuk melayani input pengguna baru.

### Laporan Analisis Bias (Bias Analysis Report)
| Bias / Keterbatasan | Penjelasan | Mitigasi |
|---|---|---|
| **Skala data tak realistis** | Konsumsi dataset (~25 kWh/bln) jauh di bawah rumah Indonesia nyata (~200 kWh/bln) karena data hanya sampel. | Klasifikasi berbasis **posisi relatif** & fitur ternormalisasi; ambang untuk data nyata dikalibrasi ke **norma PLN/BPS**. |
| **Household Size tidak konsisten** | Jumlah penghuni berubah antar baris pada seluruh rumah (ciri data sintetis). | Diambil **modus** per rumah. |
| **Bias ukuran rumah** | kWh total mentah membuat rumah besar tampak boros. | Normalisasi **per penghuni** (`kwh_per_orang`). |
| **Nilai Rupiah ilustratif** | Estimasi memakai tarif acuan (R-1/1.300 VA), bukan tagihan asli. | Disebut terbuka sebagai estimasi; tidak dipakai untuk klasifikasi. |
| **Asumsi daya (watt)** | Estimasi kWh per alat memakai watt asumsi dari `constants.py`. | Tabel watt didokumentasikan & dapat disesuaikan. |

> **Catatan etis:** hasil bersifat *decision-support*, bukan kesimpulan mutlak. Untuk penerapan nyata, model perlu dikalibrasi dengan data konsumsi rumah tangga Indonesia.

## Struktur Proyek

```
ecowatt_ai/
├── app.py                  ← entry point web app
├── constants.py            ← WATT, APPLIANCES, FITUR_ML, RECO_DB, tarif
├── model.py                ← load_model(), build_features(), run_predict()
├── state.py                ← init_state(), reset_state(), go_to()
├── ui_components.py        ← CSS global, hero, step nav, footer
├── pages/
│   ├── step1_info.py       ← form jumlah penghuni & kWh
│   ├── step2_appliances.py ← checkbox + slider pemakaian jam per alat
│   ├── step3_confirm.py    ← konfirmasi + loading + trigger prediksi
│   └── step4_result.py     ← status card, pie chart, rekomendasi
├── scaler_energi.pkl       
├── model_tree_energi.pkl   
├── data/
│   ├── AI_Energi.ipynb     ← file colab untuk data mining & training awal
│   └── dataset_energi.csv  ← dataset yang digunakan model
```

