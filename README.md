# EcoWatt AI
> **"Cek apakah rumahmu hemat listrik atau diam-diam boros!"**

Aplikasi berbasis web (Streamlit) yang dirancang untuk membantu masyarakat umum menganalisis tingkat efisiensi konsumsi listrik rumah tangga secara instan menggunakan kecerdasan buatan (*Machine Learning*).

Proyek ini dikembangkan untuk memenuhi tugas mata kuliah **Artificial Intelligence** di **Universitas Padjadjaran**.

---

## Tim Pengembang (Kelompok)
Susunan anggota kelompok pengembang EcoWatt AI:
1. **[Athifah Ari Ghumaisha]** — NPM: `[140810240004]`
2. **[Vivian Azarine Widyatna]** — NPM: `[140810240014]`
3. **[Azhaar Fathin Tsuraya]** — NPM: `[140810240036]`

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
| kWh tahunan | `kwh_bulan × 12` → sama dengan basis dataset |
| Estimasi kWh alat | `Watt × jam/hari × 365 / 1000` per alat |
| Proporsi | `kWh_alat / total_kWh_semua_alat` → `prop_*` |
| kwh_per_orang | `kwh_tahun / n_penghuni` (TAHUNAN, bukan bulanan!) |
| Normalisasi | `StandardScaler.transform()` — **wajib sebelum predict** |
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
│
├── app.py                    # File kode utama aplikasi Streamlit
├── requirements.txt          # Daftar library dependency Python
├── scaler_energi.pkl         # Serialisasi StandardScaler (dari Notebook)
├── model_tree_energi.pkl     # Serialisasi Decision Tree (dari Notebook)
├── kmeans_energi.pkl         # Serialisasi KMeans (dari Notebook)
└── README.md                 # Dokumentasi proyek aplikasi
```

