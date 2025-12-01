# **Seller Churn Analysis**

## **1. Deskripsi Proyek**

Proyek ini bertujuan untuk menganalisis faktor-faktor yang mempengaruhi **churn seller** pada platform marketplace Olist. Seller churn merujuk pada kondisi ketika seller berhenti berjualan atau menjadi tidak aktif dalam periode tertentu. Analisis dilakukan menggunakan data historis transaksi, performa seller, serta metrik aktivitas lainnya.

Proyek mencakup eksplorasi data, pembuatan fitur, pemodelan machine learning, serta rekomendasi strategis berdasarkan temuan model.

---

## **2. Latar Belakang**

Marketplace seperti Olist sangat mengandalkan keberlanjutan seller untuk menjaga ekosistem yang sehat. Ketika seller churn, terjadi dampak negatif seperti:

* Penurunan pilihan produk untuk pelanggan
* Berkurangnya volume transaksi
* Meningkatnya biaya akuisisi seller baru

Dengan memahami faktor penyebab churn, tim dapat melakukan intervensi preventif sebelum seller benar-benar meninggalkan platform.

---

## **3. Stakeholder**

Pihak yang berkepentingan dalam proyek ini:

* **Seller Support Team**
  Membantu menjaga hubungan seller dan mendukung kebutuhan mereka.

* **Business Intelligence Team**
  Menganalisis performa bisnis dan memberikan insight strategis.

* **Marketplace Product Team**
  Mengembangkan fitur dan pengalaman seller di platform.

---

## **4. Tujuan Proyek**

Proyek ini memiliki beberapa tujuan utama:

* Mengidentifikasi faktor signifikan yang berpengaruh pada risiko churn seller.
* Membangun model prediksi churn dengan performa yang optimal.
* Memberikan rekomendasi actionable berdasarkan hasil analisis dan model.
* Menyediakan insight yang dapat digunakan untuk strategi retensi seller.

---

## **5. Dataset**

Dataset yang digunakan mencakup:

* Informasi seller
* Riwayat transaksi
* Kategori produk
* Performansi pengiriman
* Rating dan ulasan pelanggan

Notebook melakukan pembersihan data, penggabungan tabel, serta feature engineering untuk menyiapkan data sebelum modeling.

---

## **6. Metodologi**

Tahapan utama dalam analisis:

1. **Exploratory Data Analysis (EDA)**
   Mengidentifikasi pola, distribusi data, dan outlier.

2. **Data Preprocessing**

   * Handling missing values
   * Encoding
   * Scaling
   * Feature selection

3. **Modeling**
   Model machine learning yang digunakan antara lain:

   * Logistic Regression
   * Random Forest
   * XGBoost

4. **Evaluasi Model**
   Menggunakan metrik:

   * Accuracy
   * Precision, Recall, F1-score
   * ROC-AUC

5. **Interpretasi Fitur**
   Melihat fitur mana yang paling berkontribusi dalam meningkatkan risiko churn.

---

## **7. Hasil Utama**

* Model terbaik menunjukkan performa prediksi yang baik untuk mendeteksi seller dengan risiko churn tinggi.
* Beberapa faktor penting yang ditemukan berpengaruh:

  * Penurunan jumlah pesanan dalam beberapa periode terakhir
  * Rating buruk atau meningkatnya komplain
  * Penurunan variasi produk yang dijual
  * Kenaikan waktu pengiriman

---

## **8. Rekomendasi Bisnis**

Berdasarkan insight model, beberapa rekomendasi yang disarankan:

* Membuat *early warning system* untuk mendeteksi seller berisiko tinggi.
* Menyediakan dukungan khusus untuk seller yang mengalami tren negatif dalam performa.
* Memberi insentif atau program retensi untuk seller yang mendekati ambang churn.
* Memberikan edukasi dan pelatihan untuk meningkatkan kualitas layanan seller.

---

## **9. Struktur Repository**

Struktur umum repositori:

```
.
├── README.md
├── Finpro_5_0.ipynb
├── data/
│   ├── raw/
│   └── processed/
└── models/
```

---

## **10. Cara Menjalankan Notebook**

1. Pastikan Python 3.x terinstal
2. Install library yang diperlukan:

   ```
   pip install -r requirements.txt
   ```
3. Jalankan notebook:

   ```
   jupyter notebook Finpro_5_0.ipynb
   ```

---

## **11. Kontributor**

* Adinda Prilly Cindana
* Dian Margaretha Nainggolan


