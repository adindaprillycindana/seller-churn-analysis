import streamlit as st
import pandas as pd
import pickle

# Daftar fitur yang dipakai model (harus sama dengan training)
FEATURE_COLS = [
    "product_id_nunique",
    "price_min",
    "freight_value_min",
    "freight_value_max",
    "payment_installments_min",
    "payment_installments_max",
    "payment_installments_median",
    "payment_value_min",
    "payment_value_sum",
    "review_score_min",
    "product_description_lenght_min",
    "product_description_lenght_max",
    "product_photos_qty_min",
    "product_photos_qty_max",
    "product_weight_g_min",
    "product_weight_g_max",
    "product_weight_g_median",
    "product_length_cm_min",
    "product_height_cm_min",
    "product_height_cm_max",
    "product_width_cm_max",
    "seller_customer_distance_km_min",
    "seller_customer_distance_km_max",
    "seller_customer_distance_km_median",
    "seller_review_response_hours_min",
    "seller_review_response_hours_max",
    "seller_review_response_hours_mean",
    "seller_lead_time_approval_hours_min",
    "seller_lead_time_approval_hours_max",
    "seller_lead_time_approval_hours_median",
    "seller_buffer_time_days_min",
    "seller_buffer_time_days_max",
    "seller_buffer_time_days_mean",
    "freight_gmv_ratio",
    "price_range",
    "price_range_normalized",
    "account_age",
    "Activity_Rate",
    "seller_city_mode",
    "customer_city_mode",
    "customer_state_mode",
    "seller_state_mode",
    "payment_type_mode",
    "order_status_mode",
    "product_category_name_english_mode",
]

# CONFIG & MODEL
st.set_page_config(
    page_title="Seller Churn Monitoring - Admin",
    layout="wide",
)

# THEME: Custom brand colors + layout
st.markdown(
    """
    <style>
    :root {
        --primary-blue: #0D50E4;
        --light-blue: #7D97E4;
        --accent-red: #E05442;
        --bg-soft: #F2F6FF;
    }

    /* -----------------------------------------------------
    BACKGROUND APLIKASI
    ----------------------------------------------------- */
    body,
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(
            135deg,
            #F2F6FF 0%,
            #ECF1FF 40%,
            #F5F8FF 100%
        ) !important;
        color: #111827;
    }

    [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] {
        color: #111827;
    }

    /* -----------------------------------------------------
    SIDEBAR
    ----------------------------------------------------- */
    [data-testid="stSidebar"] {
        background: #E4ECFF !important;
        color: #111827 !important;
    }
    [data-testid="stSidebar"] * {
        color: #111827 !important;
    }
    [data-testid="stSidebar"] a {
        color: var(--primary-blue) !important;
    }

    /* -----------------------------------------------------
    INPUT TEXT / NUMBER
    ----------------------------------------------------- */
    [data-baseweb="input"] input {
        background-color: #0B1F5B !important;
        color: #FFFFFF !important;
        border-radius: 999px !important;
        border: 1px solid #7D97E4 !important;
        padding: 0.45rem 0.75rem !important;
    }

    [data-baseweb="input"] input::placeholder {
        color: #E5E7EB !important;
    }

    /* -----------------------------------------------------
    SELECTBOX
    ----------------------------------------------------- */
    [data-baseweb="select"] > div {
        background-color: #0B1F5B !important;
        color: #FFFFFF !important;
        border-radius: 999px !important;
        border: 1px solid #7D97E4 !important;
        padding: 0.1rem 0.5rem !important;
    }
    [data-baseweb="select"] span {
        color: #FFFFFF !important;
    }

    /* -----------------------------------------------------
    TABS
    ----------------------------------------------------- */
    [data-baseweb="tab-list"] {
        gap: 0.25rem;
    }
    [data-baseweb="tab-list"] button[role="tab"] {
        border-radius: 999px;
        padding: 0.35rem 1rem;
        font-weight: 500;
        color: var(--primary-blue);
    }
    [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: rgba(13, 80, 228, 0.12);
        border-bottom: 3px solid var(--primary-blue);
        color: var(--primary-blue);
    }

    /* -----------------------------------------------------
    METRIC CARD
    ----------------------------------------------------- */
    [data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 0.85rem 1rem;
        border-radius: 16px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
        border: 1px solid rgba(125, 151, 228, 0.35);
    }
    [data-testid="stMetricLabel"] {
        color: #7D97E4 !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: #0D50E4 !important;
        font-weight: 700 !important;
    }

    /* -----------------------------------------------------
    TABEL DATAFRAME
    ----------------------------------------------------- */
    .dataframe {
        border-collapse: collapse !important;
    }
    .dataframe th {
        background-color: #0D50E4 !important;
        color: #FFFFFF !important;
        border: 1px solid #D0D7F5 !important;
    }
    .dataframe td {
        color: #111827 !important;
        border: 1px solid #E5E7EB !important;
    }

    /* -----------------------------------------------------
    MARKDOWN TABLE
    ----------------------------------------------------- */
    [data-testid="stMarkdownContainer"] table {
        border-collapse: collapse;
        width: 100%;
    }
    [data-testid="stMarkdownContainer"] th,
    [data-testid="stMarkdownContainer"] td {
        border: 1px solid #D0D7F5;
        padding: 8px 12px;
    }
    [data-testid="stMarkdownContainer"] th {
        background-color: #E4ECFF;
        color: #0D50E4;
        font-weight: 600;
    }

    /* -----------------------------------------------------
    PARAGRAF
    ----------------------------------------------------- */
    .stMarkdown p {
        text-align: justify !important;
        text-justify: inter-word !important;
        margin-right: 4rem !important;
        margin-left: 0.5rem !important;
        max-width: 900px !important;
        line-height: 1.55 !important;
    }

    /* -----------------------------------------------------
    EXPANDER
    ----------------------------------------------------- */
    details[data-testid="stExpander"] {
        background-color: #E4ECFF !important;
        border: 1px solid #AFC3F7 !important;
        border-radius: 12px !important;
        padding: 0.3rem 0.8rem !important;
        margin-bottom: 1rem !important;
    }

    details[data-testid="stExpander"] > summary {
        background-color: #D8E4FF !important;
        color: #0D50E4 !important;
        padding: 0.6rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    details[data-testid="stExpander"] div[role="region"] {
        background-color: #F5F8FF !important;
        padding: 1rem !important;
        border-radius: 8px !important;
    }

    /* -----------------------------------------------------
    HEADING
    ----------------------------------------------------- */
    h1, h2, h3 {
        color: var(--primary-blue);
    }

    /* =====================================================
    FIX PENTING — TOMBOL SUBMIT FORM
    ===================================================== */

    /* Tombol submit khusus untuk st.form_submit_button */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #D0D7F5 !important;
        color: white !important;
        border-radius: 999px !important;
        border: 1px solid #D0D7F5 !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(13,80,228,0.25);
        cursor: pointer;
    }

    /* Hover effect */
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #7D97E4 !important;
        box-shadow: 0 6px 14px rgba(13,80,228,0.35);
    }

    /* Backup: semua tombol standar juga ikut biru */
    .stButton > button {
        background-color: #0D50E4 !important;
        color: #FFFFFF !important;
        border-radius: 999px !important;
        border: 1px solid #0D50E4 !important;
    }
    .numeric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem 1.5rem;
        margin-bottom: 2rem;
    }

    .numeric-grid > div {
        width: 100%;
    }

    /* --- FIX LAYOUT 3 KOLOM NUMERIC --- */
    div[data-testid="column"] {
        min-width: 320px !important;   /* atur lebar minimum kolom */
    }

    div[data-testid="stNumberInput"] > div {
        width: 100% !important;        /* paksa input mengikuti lebar kolom */
    }

    label {
        font-size: 0.85rem !important; /* kecilkan label agar tidak turun baris */
        line-height: 1.2 !important;
    }


    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def load_model():
    """
    Muat model dari file .sav.
    Jika gagal, tampilkan error dan kembalikan None supaya app tidak crash.
    """
    try:
        with open("final_model.sav", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error("File model 'final_model.sav' tidak ditemukan. Pastikan file ada di direktori yang sama dengan app.")
    except Exception as e:
        st.error("Gagal memuat model dari 'final_model.sav'.")
        st.exception(e)
    return None


model = load_model()

# SIDEBAR - INFO ADMIN
st.sidebar.title("Panel Admin")
st.sidebar.markdown(
    """
    Gunakan halaman ini untuk mengecek **risiko churn seller**  
    berdasarkan perilaku historis dan karakteristik tokonya.

    **Definisi churn:**
    Seller dianggap churn jika **tidak aktif atau tidak menerima pesanan baru selama 30 hari**.

    **Tips penggunaan:**
    - Isi fitur sesuai rentang nilai di dokumentasi.
    - Pastikan nilai kategorikal cocok dengan data training.
    - Perhatikan interpretasi probabilitas di bagian hasil (probabilitas churn 30 hari).
    """
)

st.sidebar.markdown("---")
st.sidebar.subheader("Status Model")
st.sidebar.markdown(
    """
    - Nama model: <span style="color:#0D50E4; font-weight:600;">final_model.sav</span>  
    - Target: Probabilitas seller churn   
    - Output:  
      - Probabilitas churn  
      - Label: Berisiko churn / Tidak berisiko 
    """,
    unsafe_allow_html=True,
)


# HEADER HALAMAN
# HEADER HALAMAN
header_left, header_right = st.columns([6, 1])

with header_left:
    st.markdown(
        """
        <div style="padding: 10px 0 5px 0;">
            <h1 style="margin-bottom:0;color:#0D50E4;">
                Olist Seller Churn Monitoring
            </h1>
            <p style="color:#7D97E4; margin-top:4px; font-size:0.95rem;">
                Admin panel untuk memonitor dan mengevaluasi risiko churn seller dalam 30 hari berdasarkan fitur historis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.image("logo.png", width=180)   # bisa diganti 200, 250, dst





# Placeholder untuk hasil prediksi (agar berasa dashboard)
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    churn_prob_placeholder = st.empty()
with metric_col2:
    churn_label_placeholder = st.empty()
with metric_col3:
    note_placeholder = st.empty()

# TABS: SINGLE, BATCH, DOKUMENTASI
tab_form, tab_batch, tab_doc = st.tabs(
    ["🔍 Cek Risiko Seller (Single)", "📦 Cek Batch Seller", "📄 Dokumentasi Fitur"]
)

# TAB SINGLE SELLER
with tab_form:
    # Garis pemisah sebelum judul form
    st.markdown(
        "<hr style='border:0;border-top:1px solid #D0D7F5;margin:1.5rem 0;'>",
        unsafe_allow_html=True,
    )

    st.subheader("Input Profil dan Perilaku Seller (Single)")

    st.markdown(
        """
        Lengkapi data di bawah ini untuk satu seller.  
        Sistem akan menghitung **probabilitas seller akan churn dalam 30 hari ke depan**  
        dan memberikan status risiko.
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
            product_photos_qty_min = st.number_input("product_photos_qty_min (1 - 14)", 1, 14, 1)
            product_photos_qty_max = st.number_input("product_photos_qty_max (1 - 20)", 1, 20, 5)

        st.markdown("### Fitur Kategorikal")

        col_cat1, col_cat2 = st.columns(2)

        with col_cat1:
            seller_city_mode = st.selectbox("seller_city_mode", [...])  # POTONG LIST DI SINI BIAR RINGKAS
            customer_city_mode = st.selectbox("customer_city_mode", [...])  # POTONG LIST DI SINI BIAR RINGKAS
            customer_state_mode = st.selectbox(
                "customer_state_mode",
                ['SP', 'CE', 'RS', 'RJ', 'MG', 'PR', 'GO', 'BA', 'DF', 'MS', 'SC',
                 'PB', 'MT', 'TO', 'ES', 'PA', 'AL', 'PE', 'MA', 'RO', 'AC', 'PI',
                 'SE', 'AM', 'AP', 'RN']
            )

        with col_cat2:
            seller_state_mode = st.selectbox(
                "seller_state_mode",
                ['SC', 'RS', 'SP', 'MG', 'RJ', 'PR', 'GO', 'PE', 'ES', 'DF', 'BA',
                 'MT', 'AM', 'CE', 'MS', 'RN', 'RO', 'PB', 'PI', 'SE', 'MA']
            )
            payment_type_mode = st.selectbox(
                "payment_type_mode",
                ['credit_card', 'boleto', 'voucher', 'debit_card']
            )
            order_status_mode = st.selectbox(
                "order_status_mode",
                ['delivered', 'canceled', 'shipped']
            )
            product_category_name_english_mode = st.selectbox(
                "product_category_name_english_mode",
                ['sports_leisure', 'fashion_bags_accessories', 'furniture_decor',
                 'housewares', 'health_beauty', 'auto', 'air_conditioning', 'toys',
                 'baby', 'furniture_living_room', 'cool_stuff',
                 'construction_tools_lights', 'computers_accessories',
                 'small_appliances', 'construction_tools_construction',
                 'books_general_interest', 'bed_bath_table', 'perfumery',
                 'stationery', 'garden_tools', 'watches_gifts', 'home_appliances',
                 'construction_tools_safety', 'food', 'telephony', 'pet_shop',
                 'musical_instruments', 'electronics', 'consoles_games',
                 'costruction_tools_garden', 'home_confort', 'drinks', 'art',
                 'audio', 'furniture_bedroom', 'books_technical',
                 'kitchen_dining_laundry_garden_furniture',
                 'fashio_female_clothing', 'fixed_telephony', 'home_appliances_2',
                 'cine_photo', 'market_place', 'luggage_accessories',
                 'home_construction', 'furniture_mattress_and_upholstery',
                 'office_furniture', 'food_drink', 'industry_commerce_and_business',
                 'costruction_tools_tools', 'party_supplies',
                 'fashion_underwear_beach', 'computers', 'arts_and_craftmanship',
                 'dvds_blu_ray', 'fashion_sport', 'agro_industry_and_commerce',
                 'diapers_and_hygiene', 'signaling_and_security', 'music',
                 'la_cuisine', 'christmas_supplies', 'books_imported',
                 'small_appliances_home_oven_and_coffee', 'fashion_shoes',
                 'fashion_male_clothing', 'tablets_printing_image']
            )

        submitted = st.form_submit_button("Prediksi Risiko")

    # Setelah form single disubmit
    if submitted:
        if model is None:
            st.error("Model belum berhasil dimuat, tidak bisa melakukan prediksi.")
        else:
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

            df_input = pd.DataFrame(data_dict)[FEATURE_COLS]

            # Garis pemisah sebelum tabel ringkasan
            st.markdown(
                "<hr style='border:0;border-top:1px solid #D0D7F5;margin:1.5rem 0;'>",
                unsafe_allow_html=True,
            )

            st.markdown("### Ringkasan Data Seller")
            st.dataframe(df_input, use_container_width=True)

            try:
                # probabilitas churn
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(df_input)[0][1]
                else:
                    # fallback: model tidak punya predict_proba, pakai output langsung
                    proba = float(model.predict(df_input)[0])

                # Pakai threshold custom: churn jika proba > 0.05
                threshold = 0.05
                pred = 1 if proba > threshold else 0

                # Card di bagian atas
                churn_prob_placeholder.metric(
                    "Probabilitas Churn",
                    f"{proba:.2%}",
                )

                if pred == 1:
                    churn_label_placeholder.markdown(
                        """
                        <div style="
                            padding:12px 14px;
                            border-radius:12px;
                            background-color:#FFE7E3;
                            color:#8E2514;
                            border:1px solid #E05442;
                            font-weight:500;
                        ">
                            <b>Status:</b> Seller berisiko churn dalam 30 hari
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    note_placeholder.markdown(
                        """
                        **Rekomendasi awal (prioritas tinggi):**
                        - Evaluasi kualitas layanan dan waktu pengiriman.
                        - Buat program retensi, misalnya insentif atau promo khusus.
                        - Pantau tren aktivitas seller beberapa minggu ke depan.
                        """
                    )
                    st.error("SELLER BERISIKO CHURN")
                else:
                    churn_label_placeholder.markdown(
                        """
                        <div style="
                            padding:12px 14px;
                            border-radius:12px;
                            background-color:#E4ECFF;
                            color:#0D50E4;
                            border:1px solid #7D97E4;
                            font-weight:500;
                        ">
                            <b>Status:</b> Seller tidak berisiko churn
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    note_placeholder.markdown(
                        """
                        **Catatan:**
                        - Pertahankan kualitas layanan dan performa seller.
                        - Seller tetap perlu dimonitor jika terjadi penurunan aktivitas sebelum 30 hari.
                        """
                    )
                    st.success("SELLER TIDAK BERISIKO CHURN")

                st.markdown("#### Interpretasi Probabilitas")
                st.markdown(
                    """
                    Probabilitas di atas menggambarkan peluang bahwa seller akan **churn**  
                    (tidak aktif atau tidak menerima pesanan baru selama 30 hari).

                    - Di bawah 0.30: Risiko churn rendah.  
                    - 0.30 sampai 0.60: Risiko churn sedang.  
                    - Di atas 0.60: Risiko churn tinggi, perlu tindakan retensi.
                    """
                )

            except Exception as e:
                st.error("Error saat prediksi.")
                st.exception(e)

# TAB BATCH SELLER
with tab_batch:
    st.markdown(
        "<hr style='border:0;border-top:1px solid #D0D7F5;margin:1.5rem 0;'>",
        unsafe_allow_html=True,
    )

    st.subheader("Cek Batch Seller (Multi-row)")

    st.markdown(
        """
        Gunakan fitur ini jika admin ingin mengecek beberapa seller sekaligus dalam satu file.

        Ketentuan file:
        - Format: CSV  
        - Satu baris = satu seller  
        - Minimal harus berisi semua kolom fitur yang digunakan model:
          kolom dalam daftar FEATURE_COLS  
        - File boleh mengandung kolom tambahan seperti seller_id, kolom ini tidak dipakai model untuk prediksi
        """
    )

    uploaded_file = st.file_uploader(
        "Upload file CSV berisi beberapa seller", type=["csv"], key="batch_uploader"
    )

    st.markdown(
        "<hr style='border:0;border-top:1px solid #D0D7F5;margin:1.5rem 0;'>",
        unsafe_allow_html=True,
    )

    if uploaded_file is not None:
        if model is None:
            st.error("Model belum berhasil dimuat, tidak bisa melakukan prediksi batch.")
        else:
            try:
                df_batch_raw = pd.read_csv(uploaded_file)

                st.markdown("### Preview Data Batch (Raw)")
                st.dataframe(df_batch_raw.head(), use_container_width=True)

                # Cek apakah semua fitur yang dibutuhkan ada di file
                missing_cols = [c for c in FEATURE_COLS if c not in df_batch_raw.columns]
                if missing_cols:
                    st.error(
                        "Kolom berikut belum ada di file dan dibutuhkan model:\n\n"
                        + ", ".join(missing_cols)
                    )
                else:
                    # Hanya kolom fitur yang dipakai model
                    X_batch = df_batch_raw[FEATURE_COLS].copy()

                    # Prediksi probabilitas dan label
                    if hasattr(model, "predict_proba"):
                        batch_proba = model.predict_proba(X_batch)[:, 1]
                    else:
                        batch_proba = model.predict(X_batch).astype(float)

                    threshold = 0.05
                    batch_pred = (batch_proba > threshold).astype(int)


                    # Gabungkan ke hasil penuh (untuk internal)
                    df_result = df_batch_raw.copy()
                    df_result["churn_proba"] = batch_proba
                    df_result["churn_label"] = [
                        "Berisiko churn" if p == 1 else "Tidak berisiko churn"
                        for p in batch_pred
                    ]

                    # Tentukan kolom ID seller (opsional)
                    possible_id_cols = ["seller_id", "seller_unique_id", "seller_name", "id"]
                    id_col = None
                    for col in possible_id_cols:
                        if col in df_result.columns:
                            id_col = col
                            break

                    # Dataframe untuk ditampilkan: rank + id (jika ada) + proba + label
                    if id_col is not None:
                        df_display = df_result[[id_col, "churn_proba", "churn_label"]].copy()
                    else:
                        df_display = df_result[["churn_proba", "churn_label"]].copy()

                    # Urutkan dari proba tertinggi ke terendah dan beri nomor rank
                    df_display = df_display.sort_values("churn_proba", ascending=False)
                    df_display.insert(0, "rank", range(1, len(df_display) + 1))

                    st.markdown("### Hasil Prediksi Batch (Ranked)")
                    st.dataframe(df_display, use_container_width=True)

                    # Cari seller dengan probabilitas churn tertinggi di batch (pakai df_result)
                    idx_max = df_result["churn_proba"].idxmax()
                    row_max = df_result.loc[[idx_max]].iloc[0]

                    st.markdown("### Ringkasan Risiko Tertinggi di Batch")

                    if id_col is not None:
                        identified = f"{id_col} = {row_max[id_col]}"
                        title_top = f"Seller dengan risiko churn tertinggi ({identified})"
                    else:
                        title_top = "Seller dengan risiko churn tertinggi"

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric(
                            title_top,
                            f"{row_max['churn_proba']:.2%}",
                        )
                    with col_b:
                        st.metric(
                            "Prediksi label",
                            row_max["churn_label"],
                        )

                    st.markdown(
                        """
                        **Catatan:**
                        - Rank = 1 adalah seller dengan probabilitas churn tertinggi di batch.
                        - Seller dengan probabilitas churn tertinggi perlu menjadi prioritas untuk program retensi.
                        - Admin dapat mengekspor tabel hasil dari menu di pojok kanan atas tabel.
                        """
                    )

            except Exception as e:
                st.error("Terjadi error saat membaca atau memproses file batch.")
                st.exception(e)
    else:
        st.info("Silakan upload file CSV untuk mulai cek batch seller.")

# TAB DOKUMENTASI
with tab_doc:
    st.markdown(
        "<hr style='border:0;border-top:1px solid #D0D7F5;margin:1.5rem 0;'>",
        unsafe_allow_html=True,
    )

    st.subheader("Panduan Singkat Penggunaan Data")

    st.markdown(
        """
        Halaman ini berisi ringkasan batas nilai data yang digunakan model.  
        Tujuannya agar admin tahu apakah data seller yang dicek masih berada di kisaran yang wajar.

        **Definisi churn yang digunakan model:**
        - Seller dianggap churn jika tidak aktif atau tidak menerima pesanan baru selama 30 hari.
        - Semua probabilitas dan label di dashboard merujuk pada risiko churn.
        """
    )

    st.markdown("### 1. Batas Nilai Fitur Angka (Numerik)")

    st.markdown(
        """
        Nilai di bawah ini adalah kisaran data yang dipakai saat model dibuat.  
        Jika nilai yang dimasukkan jauh di luar kisaran ini, hasil prediksi risiko churn bisa kurang akurat.
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
            | payment_value_sum                  | 18.56 - 78,346.48         | Total nilai pembayaran per seller                  |
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
        Ringkasnya:  
        Jika angka yang dimasukkan masih kurang lebih di dalam kisaran ini, model churn bekerja lebih stabil.
        """
    )

    st.markdown("### 2. Batas Nilai Fitur Kategorikal")

    st.markdown(
        """
        Untuk kolom kategori, model bekerja paling baik jika admin memakai nilai yang sudah dikenal model dari data sebelumnya.  
        Jika muncul kota, provinsi, atau jenis pembayaran yang baru, model tetap bisa memprediksi risiko churn tetapi hasilnya bisa kurang tepat.
        """
    )

    with st.expander("Lihat ringkasan kategori yang digunakan model"):
        st.markdown(
            """
            | Fitur Kategorikal                  | Contoh Nilai yang Digunakan Model                                                                                             | Catatan untuk Admin                             |
            | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
            | seller_city_mode                   | Nama kota seller yang sudah ada di data historis                                                                              | Kota baru dianggap kategori baru                |
            | seller_state_mode                  | SC, RS, SP, MG, RJ, PR, GO, PE, ES, DF, BA, MT, AM, CE, MS, RN, RO, PB, PI, SE, MA                                           | Gunakan kode provinsi yang konsisten            |
            | order_status_mode                  | delivered, canceled, shipped                                                                                                  | Status lain tidak digunakan model               |
            | payment_type_mode                  | credit_card, boleto, voucher, debit_card                                                                                      | Metode baru mungkin kurang akurat               |
            | product_category_name_english_mode | Nama kategori produk yang pernah ada di data historis                                                                        | Kategori baru dapat menurunkan akurasi          |
            | customer_city_mode                 | Kota customer dari data historis                                                                                              | Kota baru dianggap kategori baru                |
            | customer_state_mode                | SP, CE, RS, RJ, MG, PR, GO, BA, DF, MS, SC, PB, MT, TO, ES, PA, AL, PE, MA, RO, AC, PI, SE, AM, AP, RN                      | Pastikan kode provinsi sesuai                   |
            """,
            unsafe_allow_html=False,
        )

    st.markdown(
        """
        Ringkasnya:  
        Semakin mirip data yang dimasukkan dengan data historis, semakin bisa dipercaya hasil prediksi risiko churn dalam 90 hari.
        """
    )

    st.markdown("### 3. Catatan Praktis untuk Admin")

    st.markdown(
        """
        - Model melihat pola dari data historis, bukan masa depan yang pasti.  
        - Seller yang sangat baru bisa menghasilkan prediksi risiko churn yang kurang stabil.  
        - Perubahan besar seperti promo besar atau kebijakan baru belum tentu tercermin di model.  
        - Gunakan hasil model sebagai indikasi risiko churn, bukan satu-satunya dasar keputusan.
        """
    )

