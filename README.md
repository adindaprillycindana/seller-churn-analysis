# **Seller Churn Analysis**

## **1. Deskripsi Proyek**

Proyek ini bertujuan untuk menganalisis perilaku **churn seller** pada marketplace (penjual yang berhenti aktif). Analisis dilakukan menggunakan dataset historis yang mencakup transaksi, performa seller, dan variabel operasional lainnya. Output akhir berupa model prediksi churn serta aplikasi sederhana untuk melakukan prediksi berdasarkan input user.

Proyek ini terdiri dari notebook analisis, file model, aplikasi, dan query SQL yang digunakan pada tahap data preparation.

---

## **2. File & Struktur Repository**

Repositori memiliki struktur berikut:

```
.
├── SQL Queries/
│   └── (kumpulan query SQL untuk ekstraksi & transformasi data)
│
├── README.md                 → Dokumentasi proyek (file ini)
├── Seller_Churn_Analisis.ipynb   → Notebook utama yang dijalankan
│                                   berisi EDA, preprocessing, modeling
│
├── app.py                    → Aplikasi prediksi (Streamlit)
│
├── final_model.sav           → Model machine learning yang sudah dilatih
│
├── requirements.txt          → Daftar library Python yang dibutuhkan
```

### **File utama yang dijalankan**

**`Seller_Churn_Analisis.ipynb`**
Ini adalah notebook yang berisi seluruh proses analisis, mulai dari:

* Eksplorasi Data (EDA)
* Pembersihan & Transformasi Data
* Feature Engineering
* Training Model
* Evaluasi Model
* Export model (final_model.sav)

---

## **3. Cara Menjalankan Proyek**

### **A. Menjalankan Notebook Analisis**

1. Pastikan Python 3.x sudah terinstall
2. Install semua dependensi:

   ```
   pip install -r requirements.txt
   ```
3. Jalankan Jupyter Notebook:

   ```
   jupyter notebook
   ```
4. Buka file:

   ```
   Seller_Churn_Analisis.ipynb
   ```

---

### **B. Menjalankan Aplikasi Prediksi (`app.py`)**

Jika app.py menggunakan Streamlit:

```
streamlit run app.py
``` 

Pastikan file `final_model.sav` berada di direktori yang sama karena file tersebut akan diload oleh aplikasi.

Atau dapat diakses dari link https://seller-churn-analysis-wekmr6jh7z9glbjzixaroc.streamlit.app/

---

## **4. Gambaran Proses Analisis**

Notebook analisis menyertakan langkah-langkah berikut:

### **1. Exploratory Data Analysis (EDA)**

* Distribusi seller aktif vs churn
* Tren penurunan performa
* Analisis rating, jumlah pesanan, keterlambatan pengiriman

### **2. Data Cleaning & Preprocessing**

* Menangani missing values
* Encoding variabel kategorikal
* Normalisasi / scaling data jika diperlukan

### **3. Modeling**

Model yang umum digunakan:

* Logistic Regression
* Random Forest
* XGBoost

Model dengan performa terbaik disimpan sebagai `final_model.sav`.

### **4. Evaluasi**

Menggunakan:

* Precision
* Recall
* F1-score
* ROC-AUC

---

## **5. Hasil Utama**

Model mampu mengidentifikasi seller berisiko churn berdasarkan variabel seperti:

* Tren penurunan order
* Rating dan komplain
* Keterlambatan pengiriman
* Penurunan variasi produk

Insight dan interpretasi model ditampilkan langsung di notebook.

---

## **6. Query SQL**

Folder **`SQL Queries`** berisi query yang digunakan untuk:

* Esktraksi data transaksi
* Agregasi performa seller
* Pembuatan dataset akhir sebelum masuk proses analisis

---

## **7. Kontributor**

* Adinda Prilly Cindana
* Dian Margaretha Nainggolan


