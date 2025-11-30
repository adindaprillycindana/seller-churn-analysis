import streamlit as st
import pandas as pd
import pickle

# CONFIG & MODEL
st.set_page_config(
    page_title="Seller Churn Monitoring - Admin",
    layout="wide",
)

@st.cache_resource
def load_model():
    with open("model_terbaik.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# SIDEBAR - INFO ADMIN
st.sidebar.title("Panel Admin")
st.sidebar.markdown(
    """
    Gunakan halaman ini untuk mengecek **risiko churn seller**  
    berdasarkan perilaku historis dan karakteristik tokonya.

    **Tips penggunaan:**
    - Isi fitur sesuai rentang nilai di dokumentasi.
    - Pastikan nilai kategorikal cocok dengan data training.
    - Perhatikan interpretasi probabilitas di bagian hasil.
    """
)

st.sidebar.markdown("---")
st.sidebar.subheader("Status Model")
st.sidebar.markdown(
    """
    - Nama model: `model_terbaik.pkl`  
    - Target: Probabilitas seller churn  
    - Output:  
      - Probabilitas churn  
      - Label: Berisiko churn / Tidak berisiko
    """
)

# HEADER HALAMAN
st.markdown(
    """
    <div style="padding: 10px 0 5px 0;">
        <h1 style="margin-bottom:0;">Seller Churn Monitoring</h1>
        <p style="color:gray; margin-top:4px;">
            Admin panel untuk memonitor dan mengevaluasi risiko churn seller berdasarkan fitur historis.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Placeholder untuk hasil prediksi (agar berasa dashboard)
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    churn_prob_placeholder = st.empty()
with metric_col2:
    churn_label_placeholder = st.empty()
with metric_col3:
    note_placeholder = st.empty()

# TABS: FORM INPUT & DOKUMENTASI
tab_form, tab_doc = st.tabs(["🔍 Cek Risiko Seller", "📄 Dokumentasi Fitur"])

with tab_form:
    st.subheader("Input Profil dan Perilaku Seller")

    st.markdown(
        """
        Lengkapi data di bawah ini untuk satu seller.  
        Sistem akan menghitung probabilitas churn dan memberikan status risiko.
        """
    )

    # Gunakan form supaya terasa lebih rapi seperti halaman admin
    with st.form("seller_form"):
        st.markdown("### Fitur Numerik")

        col1, col2, col3 = st.columns(3)

        with col1:
            product_id_nunique = st.number_input("product_id_nunique (1 - 129.6)", 1.0, 129.6, 10.0)
            price_min = st.number_input("price_min (0.85 - 1299)", 0.85, 1299.0, 50.0)
            freight_value_min = st.number_input("freight_value_min (0 - 71.04)", 0.0, 71.04, 5.0)
            freight_value_max = st.number_input("freight_value_max (0.75 - 218.7)", 0.75, 218.7, 20.0)
            payment_installments_min = st.number_input("payment_installments_min (0 - 10)", 0, 10, 0)
            payment_installments_max = st.number_input("payment_installments_max (1 - 20)", 1, 20, 5)
            payment_installments_median = st.number_input("payment_installments_median (1 - 10)", 1.0, 10.0, 3.0)
            payment_value_min = st.number_input("payment_value_min (0 - 1336.98)", 0.0, 1336.98, 50.0)
            payment_value_sum = st.number_input("payment_value_sum (18.56 - 78346.48)", 18.56, 78346.48, 1000.0)
            review_score_min = st.number_input("review_score_min (1 - 5)", 1, 5, 3)
            product_description_lenght_min = st.number_input("product_description_lenght_min (4 - 3992)", 4, 3992, 50)
            product_description_lenght_max = st.number_input("product_description_lenght_max (4 - 3992)", 4, 3992, 500)
            product_photos_qty_min = st.number_input("product_photos_qty_min (1 - 14)", 1, 14, 1)
            product_photos_qty_max = st.number_input("product_photos_qty_max (1 - 20)", 1, 20, 5)

        with col2:
            product_weight_g_min = st.number_input("product_weight_g_min (2 - 21490)", 2.0, 21490.0, 200.0)
            product_weight_g_max = st.number_input("product_weight_g_max (50 - 30000)", 50.0, 30000.0, 1000.0)
            product_weight_g_median = st.number_input("product_weight_g_median (2 - 24615)", 2.0, 24615.0, 500.0)
            product_length_cm_min = st.number_input("product_length_cm_min (7 - 89)", 7.0, 89.0, 20.0)
            product_height_cm_min = st.number_input("product_height_cm_min (2 - 62)", 2.0, 62.0, 5.0)
            product_height_cm_max = st.number_input("product_height_cm_max (2 - 96.3)", 2.0, 96.3, 20.0)
            product_width_cm_max = st.number_input("product_width_cm_max (8 - 90)", 8.0, 90.0, 20.0)
            seller_customer_distance_km_min = st.number_input("seller_customer_distance_km_min (0 - 2073)", 0.0, 2073.33, 10.0)
            seller_customer_distance_km_max = st.number_input("seller_customer_distance_km_max (1.14 - 3289)", 1.14, 3289.06, 100.0)
            seller_customer_distance_km_median = st.number_input("seller_customer_distance_km_median (1.14 - 2221)", 1.14, 2221.45, 50.0)
            seller_review_response_hours_min = st.number_input("seller_review_response_hours_min (2.42 - 148)", 2.42, 148.42, 10.0)
            seller_review_response_hours_max = st.number_input("seller_review_response_hours_max (4 - 5711)", 4.07, 5711.14, 100.0)
            seller_review_response_hours_mean = st.number_input("seller_review_response_hours_mean (4 - 363)", 4.07, 363.85, 20.0)

        with col3:
            seller_lead_time_approval_hours_min = st.number_input("seller_lead_time_approval_hours_min (0 - 43)", 0.0, 43.22, 1.0)
            seller_lead_time_approval_hours_max = st.number_input("seller_lead_time_approval_hours_max (0 - 258)", 0.0, 258.09, 24.0)
            seller_lead_time_approval_hours_median = st.number_input("seller_lead_time_approval_hours_median (0 - 64)", 0.0, 64.30, 5.0)
            seller_buffer_time_days_min = st.number_input("seller_buffer_time_days_min (-117 - 19)", -117.0, 19.0, 0.0)
            seller_buffer_time_days_max = st.number_input("seller_buffer_time_days_max (-46 - 1046)", -46.0, 1046.0, 5.0)
            seller_buffer_time_days_mean = st.number_input("seller_buffer_time_days_mean (-46 - 32)", -46.0, 32.17, 1.0)
            freight_gmv_ratio = st.number_input("freight_gmv_ratio (0.0015 - 0.5127)", 0.0015, 0.5127, 0.05)
            price_range = st.number_input("price_range (0 - 2198)", 0.0, 2198.72, 100.0)
            price_range_normalized = st.number_input("price_range_normalized (0 - 9.44)", 0.0, 9.44, 1.0)
            account_age = st.number_input("account_age (31 - 703)", 31, 703, 100)
            Activity_Rate = st.number_input("Activity_Rate (0.0014 - 0.9536)", 0.0014, 0.9536, 0.3)

        st.markdown("### Fitur Kategorikal")

        col_cat1, col_cat2 = st.columns(2)

        with col_cat1:
            seller_city_mode = st.text_input("seller_city_mode", "seller_city_contoh")
            customer_city_mode = st.text_input("customer_city_mode", "customer_city_contoh")
            customer_state_mode = st.text_input("customer_state_mode", "state_customer_contoh")

        with col_cat2:
            seller_state_mode = st.text_input("seller_state_mode", "state_seller_contoh")
            payment_type_mode = st.text_input("payment_type_mode", "credit_card")
            order_status_mode = st.text_input("order_status_mode", "delivered")
            product_category_name_english_mode = st.text_input(
                "product_category_name_english_mode",
                "bed_bath_table"
            )

        submitted = st.form_submit_button("Prediksi Risiko Churn")

    # Setelah form disubmit
    if submitted:
        data_dict = {
            "product_id_nunique": [product_id_nunique],
            "price_min": [price_min],
            "freight_value_min": [freight_value_min],
            "freight_value_max": [freight_value_max],
            "payment_installments_min": [payment_installments_min],
            "payment_installments_max": [payment_installments_max],
            "payment_installments_median": [payment_installments_median],
            "payment_value_min": [payment_value_min],
            "payment_value_sum": [payment_value_sum],
            "review_score_min": [review_score_min],
            "product_description_lenght_min": [product_description_lenght_min],
            "product_description_lenght_max": [product_description_lenght_max],
            "product_photos_qty_min": [product_photos_qty_min],
            "product_photos_qty_max": [product_photos_qty_max],
            "product_weight_g_min": [product_weight_g_min],
            "product_weight_g_max": [product_weight_g_max],
            "product_weight_g_median": [product_weight_g_median],
            "product_length_cm_min": [product_length_cm_min],
            "product_height_cm_min": [product_height_cm_min],
            "product_height_cm_max": [product_height_cm_max],
            "product_width_cm_max": [product_width_cm_max],
            "seller_customer_distance_km_min": [seller_customer_distance_km_min],
            "seller_customer_distance_km_max": [seller_customer_distance_km_max],
            "seller_customer_distance_km_median": [seller_customer_distance_km_median],
            "seller_review_response_hours_min": [seller_review_response_hours_min],
            "seller_review_response_hours_max": [seller_review_response_hours_max],
            "seller_review_response_hours_mean": [seller_review_response_hours_mean],
            "seller_lead_time_approval_hours_min": [seller_lead_time_approval_hours_min],
            "seller_lead_time_approval_hours_max": [seller_lead_time_approval_hours_max],
            "seller_lead_time_approval_hours_median": [seller_lead_time_approval_hours_median],
            "seller_buffer_time_days_min": [seller_buffer_time_days_min],
            "seller_buffer_time_days_max": [seller_buffer_time_days_max],
            "seller_buffer_time_days_mean": [seller_buffer_time_days_mean],
            "freight_gmv_ratio": [freight_gmv_ratio],
            "price_range": [price_range],
            "price_range_normalized": [price_range_normalized],
            "account_age": [account_age],
            "Activity_Rate": [Activity_Rate],
            "seller_city_mode": [seller_city_mode],
            "customer_city_mode": [customer_city_mode],
            "customer_state_mode": [customer_state_mode],
            "seller_state_mode": [seller_state_mode],
            "payment_type_mode": [payment_type_mode],
            "order_status_mode": [order_status_mode],
            "product_category_name_english_mode": [product_category_name_english_mode],
        }

        df_input = pd.DataFrame(data_dict)

        st.markdown("### Ringkasan Data Seller")
        st.dataframe(df_input, use_container_width=True)

        try:
            # probabilitas churn
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(df_input)[0][1]
            else:
                proba = float(model.predict(df_input)[0])

            pred = model.predict(df_input)[0]

            # Card di bagian atas
            churn_prob_placeholder.metric(
                "Probabilitas Churn",
                f"{proba:.2%}",
            )

            if pred == 1:
                churn_label_placeholder.markdown(
                    "<div style='padding:10px;border-radius:8px;background-color:#ffe5e5;color:#b00020;'>"
                    "<b>Status:</b> Seller berisiko churn"
                    "</div>",
                    unsafe_allow_html=True,
                )
                note_placeholder.markdown(
                    """
                    **Rekomendasi awal:**
                    - Evaluasi kualitas layanan dan waktu pengiriman.
                    - Buat program retensi, misalnya insentif atau promo khusus.
                    - Pantau kembali dalam periode waktu pendek.
                    """
                )
                st.error("SELLER BERISIKO CHURN")
            else:
                churn_label_placeholder.markdown(
                    "<div style='padding:10px;border-radius:8px;background-color:#e6f4ea;color:#1e4620;'>"
                    "<b>Status:</b> Seller tidak berisiko churn"
                    "</div>",
                    unsafe_allow_html=True,
                )
                note_placeholder.markdown(
                    """
                    **Catatan:**
                    - Pertahankan kualitas layanan dan performa seller.
                    - Seller tetap perlu dimonitor jika terjadi penurunan aktivitas.
                    """
                )
                st.success("SELLER TIDAK BERISIKO CHURN")

            st.markdown("#### Interpretasi Probabilitas")
            st.markdown(
                """
                - Di bawah 0.30: Risiko churn rendah.  
                - 0.30 sampai 0.60: Risiko churn sedang.  
                - Di atas 0.60: Risiko churn tinggi, perlu tindakan retensi.
                """
            )

        except Exception as e:
            st.error("Error saat prediksi.")
            st.exception(e)

with tab_doc:
    st.subheader("Panduan Singkat Penggunaan Data")

    st.markdown(
        """
        Halaman ini berisi ringkasan batas nilai data yang digunakan model.  
        Tujuannya agar admin tahu apakah data seller yang dicek masih berada di kisaran yang wajar.
        """
    )

    st.markdown("### 1. Batas Nilai Fitur Angka (Numerik)")

    st.markdown(
        """
        Nilai di bawah ini adalah kisaran data yang dipakai saat model dibuat.  
        Jika nilai yang dimasukkan jauh di luar kisaran ini, hasil prediksi bisa kurang akurat.
        """
    )

    with st.expander("Lihat tabel batas nilai fitur numerik"):
        st.markdown(
            """
            | Kriteria (Fitur)                   | Rentang Nilai (min - max) | Keterangan Singkat                                 |
            | ---------------------------------- | ------------------------- | -------------------------------------------------- |
            | product_id_nunique                 | 1.00 - 129.60             | Jumlah produk unik yang pernah dijual seller       |
            | price_min                          | 0.85 - 1299.00            | Harga terendah produk seller                       |
            | freight_value_min                  | 0.00 - 71.04              | Ongkir minimum per item                            |
            | freight_value_max                  | 0.75 - 218.70             | Ongkir maksimum per item                           |
            | payment_installments_min           | 0 - 10                    | Cicilan minimum                                    |
            | payment_installments_max           | 1 - 20                    | Cicilan maksimum                                   |
            | payment_installments_median        | 1 - 10                    | Cicilan yang paling sering terjadi                 |
            | payment_value_min                  | 0.00 - 1336.98            | Nilai pembayaran terkecil per pesanan              |
            | payment_value_sum                  | 18.56 - 78,346.48         | Total nilai pembayaran per seller                   |
            | review_score_min                   | 1 - 5                     | Nilai review terendah                              |
            | product_description_lenght_min     | 4 - 3992                  | Panjang deskripsi produk terpendek                 |
            | product_description_lenght_max     | 4 - 3992                  | Panjang deskripsi produk terpanjang                |
            | product_photos_qty_min             | 1 - 14                    | Jumlah foto minimum                                |
            | product_photos_qty_max             | 1 - 20                    | Jumlah foto maksimum                               |
            | product_weight_g_min               | 2 - 21,490                | Berat produk paling ringan                         |
            | product_weight_g_max               | 50 - 30,000               | Berat produk paling berat                          |
            | product_weight_g_median            | 2 - 24,615                | Berat produk yang paling umum                      |
            | product_length_cm_min              | 7 - 89                    | Panjang produk minimum                             |
            | product_height_cm_min              | 2 - 62                    | Tinggi produk minimum                              |
            | product_height_cm_max              | 2 - 96.30                 | Tinggi produk maksimum                             |
            | product_width_cm_max               | 8 - 90                    | Lebar produk maksimum                              |
            | seller_customer_distance_km_min    | 0.00 - 2073.33            | Jarak pelanggan terdekat                           |
            | seller_customer_distance_km_max    | 1.14 - 3289.06            | Jarak pelanggan terjauh                            |
            | seller_customer_distance_km_median | 1.14 - 2221.45            | Jarak pelanggan yang paling umum                   |
            | seller_review_response_hours_min   | 2.42 - 148.42             | Respon tercepat ke review atau komplain            |
            | seller_review_response_hours_max   | 4.07 - 5711.14            | Respon terlambat ke review atau komplain           |
            | seller_review_response_hours_mean  | 4.07 - 363.85             | Rata-rata waktu respon review atau komplain        |
            | seller_lead_time_approval_hours_min| 0.00 - 43.22              | Persetujuan order tercepat                         |
            | seller_lead_time_approval_hours_max| 0.00 - 258.09             | Persetujuan order terlambat                        |
            | seller_lead_time_approval_hours_median | 0.00 - 64.30          | Waktu persetujuan yang paling umum                 |
            | seller_buffer_time_days_min        | -117.00 - 19.00           | Selisih tercepat antara janji kirim dan realisasi  |
            | seller_buffer_time_days_max        | -46.00 - 1046.00          | Selisih terlambat antara janji kirim dan realisasi |
            | seller_buffer_time_days_mean       | -46.00 - 32.17            | Rata-rata selisih janji kirim dan realisasi        |
            | freight_gmv_ratio                  | 0.0015 - 0.5127           | Porsi ongkir terhadap nilai pesanan                |
            | price_range                        | 0.00 - 2198.72            | Rentang harga produk di seller                     |
            | price_range_normalized             | 0.00 - 9.44               | Versi berskala dari rentang harga                  |
            | account_age                        | 31 - 703                  | Umur akun seller (hari)                            |
            | Activity_Rate                      | 0.0014 - 0.9536           | Seberapa aktif seller selama periode data          |
            """,
            unsafe_allow_html=False,
        )

    st.markdown(
        """
        **Ringkasnya:**  
        Jika angka yang dimasukkan masih kurang lebih di dalam kisaran ini, model bekerja lebih stabil.
        """
    )

    st.markdown("### 2. Batas Nilai Fitur Kategorikal")

    st.markdown(
        """
        Untuk kolom kategori, model bekerja paling baik jika admin memakai nilai yang sudah dikenal model dari data sebelumnya.  
        Jika muncul kota, provinsi, atau jenis pembayaran yang baru, model tetap bisa memprediksi tetapi hasilnya bisa kurang tepat.
        """
    )

    with st.expander("Lihat ringkasan kategori yang digunakan model"):
        st.markdown(
            """
            | Fitur Kategorikal                | Contoh Nilai yang Digunakan Model                                                                                             | Catatan untuk Admin                             |
            | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
            | seller_city_mode                 | Nama kota seller yang sudah ada di data historis                                                                             | Kota baru dianggap kategori baru                 |
            | seller_state_mode                | SC, RS, SP, MG, RJ, PR, GO, PE, ES, DF, BA, MT, AM, CE, MS, RN, RO, PB, PI, SE, MA                                           | Gunakan kode provinsi yang konsisten             |
            | order_status_mode                | delivered, canceled, shipped                                                                                                  | Status lain tidak digunakan model                |
            | payment_type_mode                | credit_card, boleto, voucher, debit_card                                                                                      | Metode baru mungkin kurang akurat                |
            | product_category_name_english_mode | Nama kategori produk yang pernah ada di data historis                                                                        | Kategori baru → akurasi bisa turun               |
            | customer_city_mode               | Kota customer dari data historis                                                                                              | Kota baru dianggap kategori baru                 |
            | customer_state_mode              | SP, CE, RS, RJ, MG, PR, GO, BA, DF, MS, SC, PB, MT, TO, ES, PA, AL, PE, MA, RO, AC, PI, SE, AM, AP, RN                      | Pastikan kode provinsi sesuai                    |
            """,
            unsafe_allow_html=False,
        )

    st.markdown(
        """
        **Ringkasnya:**  
        Semakin mirip data yang dimasukkan dengan data historis, semakin bisa dipercaya hasil prediksinya.
        """
    )

    st.markdown("### 3. Catatan Praktis untuk Admin")

    st.markdown(
        """
        - Model melihat pola dari data historis, bukan masa depan yang pasti.  
        - Seller yang sangat baru bisa menghasilkan prediksi kurang stabil.  
        - Perubahan besar seperti promo besar atau kebijakan baru belum tentu tercermin di model.  
        - Gunakan hasil model sebagai **indikasi risiko**, bukan satu-satunya dasar keputusan.
        """
    )
