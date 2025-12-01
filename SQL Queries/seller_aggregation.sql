# Deklarasi Konstanta untuk Rumus Haversine
DECLARE EARTH_RADIUS_KM FLOAT64 DEFAULT 6371;

CREATE OR REPLACE TABLE
  `olist.seller_features_AGG`
AS (
WITH
  -- ==========================================================
  -- BAGIAN 1: PEMBERSINAN DATA (Cleaned Data CTE)
  -- ==========================================================

  data_filtered_dates AS (
    SELECT * FROM `olist.seller_final`
    WHERE order_approved_at IS NOT NULL AND order_delivered_carrier_date IS NOT NULL
  ),
  median_review_per_seller AS (SELECT seller_id, ROUND(APPROX_QUANTILES(review_score, 2)[OFFSET(1)]) AS seller_median FROM data_filtered_dates WHERE review_score IS NOT NULL GROUP BY 1),
  global_review_median AS (SELECT APPROX_QUANTILES(review_score, 2)[OFFSET(1)] AS global_median FROM data_filtered_dates WHERE review_score IS NOT NULL),
  data_imputed_review AS (
    SELECT t1.* EXCEPT(review_score), COALESCE(t1.review_score, t2.seller_median, (SELECT global_median FROM global_review_median)) AS review_score
    FROM data_filtered_dates AS t1 LEFT JOIN median_review_per_seller AS t2 ON t1.seller_id = t2.seller_id
  ),
  data_filtered_review_dates AS (
    SELECT * FROM data_imputed_review
    WHERE review_creation_date IS NOT NULL AND review_answer_timestamp IS NOT NULL
  ),
  data_filtered_payment AS (
    SELECT * FROM data_filtered_review_dates
    WHERE payment_sequential IS NOT NULL AND payment_type IS NOT NULL AND payment_installments IS NOT NULL AND payment_value IS NOT NULL
  ),
  median_product_attr_per_seller AS (
    SELECT seller_id, ROUND(APPROX_QUANTILES(product_name_lenght, 2)[OFFSET(1)]) AS seller_median_name, ROUND(APPROX_QUANTILES(product_description_lenght, 2)[OFFSET(1)]) AS seller_median_desc, ROUND(APPROX_QUANTILES(product_photos_qty, 2)[OFFSET(1)]) AS seller_median_qty FROM data_filtered_payment GROUP BY 1
  ),
  global_product_medians AS (
    SELECT APPROX_QUANTILES(product_name_lenght, 2)[OFFSET(1)] AS global_median_name, APPROX_QUANTILES(product_description_lenght, 2)[OFFSET(1)] AS global_median_desc, APPROX_QUANTILES(product_photos_qty, 2)[OFFSET(1)] AS global_median_qty FROM data_filtered_payment
  ),
  data_imputed_product_attr AS (
    SELECT t1.* EXCEPT(product_name_lenght, product_description_lenght, product_photos_qty), COALESCE(t1.product_name_lenght, t2.seller_median_name, (SELECT global_median_name FROM global_product_medians)) AS product_name_lenght, COALESCE(t1.product_description_lenght, t2.seller_median_desc, (SELECT global_median_desc FROM global_product_medians)) AS product_description_lenght, COALESCE(t1.product_photos_qty, t2.seller_median_qty, (SELECT global_median_qty FROM global_product_medians)) AS product_photos_qty
    FROM data_filtered_payment AS t1 LEFT JOIN median_product_attr_per_seller AS t2 ON t1.seller_id = t2.seller_id
  ),
  data_filtered_product_dim AS (
    SELECT * FROM data_imputed_product_attr
    WHERE product_weight_g IS NOT NULL AND product_length_cm IS NOT NULL AND product_height_cm IS NOT NULL AND product_width_cm IS NOT NULL
  ),
  mode_category_per_seller AS (
    SELECT seller_id, ANY_VALUE(t.product_category_name_english) AS seller_cat_mode FROM data_filtered_product_dim AS t WHERE product_category_name_english IS NOT NULL GROUP BY 1 QUALIFY ROW_NUMBER() OVER (PARTITION BY seller_id ORDER BY COUNT(*) DESC) = 1
  ),
  global_category_mode AS (
    SELECT product_category_name_english AS global_mode FROM data_filtered_product_dim GROUP BY 1 ORDER BY COUNT(*) DESC LIMIT 1
  ),
  mode_category_with_fallback AS (
    SELECT seller_id, COALESCE(seller_cat_mode, (SELECT global_mode FROM global_category_mode)) AS seller_cat_mode FROM mode_category_per_seller
    UNION DISTINCT
    SELECT seller_id, (SELECT global_mode FROM global_category_mode) FROM data_filtered_product_dim WHERE seller_id NOT IN (SELECT seller_id FROM mode_category_per_seller)
  ),
  data_imputed_category AS (
    SELECT t1.* EXCEPT(product_category_name_english), COALESCE(t1.product_category_name_english, t2.seller_cat_mode) AS product_category_name_english
    FROM data_filtered_product_dim AS t1 LEFT JOIN mode_category_with_fallback AS t2 ON t1.seller_id = t2.seller_id
  ),
  data_filtered_geo AS (
    SELECT * EXCEPT(review_comment_title, review_comment_message, order_delivered_customer_date, review_id, product_category_name)
    FROM data_imputed_category
    WHERE seller_lat IS NOT NULL AND seller_lng IS NOT NULL AND seller_geo_city IS NOT NULL AND seller_geo_state IS NOT NULL
    AND customer_lat IS NOT NULL AND customer_lng IS NOT NULL AND customer_geo_city IS NOT NULL AND customer_geo_state IS NOT NULL
  ),

  -- ==========================================================
  -- BAGIAN 2: PEMBUATAN FITUR (Feature Engineering)
  -- ==========================================================
  data_valid AS (
    SELECT seller_id, COALESCE(price, 0) AS price, COALESCE(payment_value, 0) AS payment_value FROM data_filtered_geo WHERE order_status != 'canceled'
  ),
  monetary_summary AS (
    SELECT seller_id, SUM(price) AS price_sum_valid, MIN(price) AS price_min_valid, MAX(price) AS price_max_valid, AVG(price) AS price_mean_valid, SUM(payment_value) AS payment_sum_valid FROM data_valid GROUP BY 1
  ),
  freight_summary AS (
    SELECT seller_id, SUM(freight_value) AS freight_sum_all FROM data_filtered_geo GROUP BY 1
  ),
  data_with_features AS (
    SELECT
      *,
      -- seller_customer_distance_km (KOREKSI RADIANS)
      (
        EARTH_RADIUS_KM * 2 * ASIN(
          SQRT(
            POWER(SIN((customer_lat - seller_lat) * ACOS(-1) / 360), 2) +
            COS(seller_lat * ACOS(-1) / 180) * COS(customer_lat * ACOS(-1) / 180) *
            POWER(SIN((customer_lng - seller_lng) * ACOS(-1) / 360), 2)
          )
        )
      ) AS seller_customer_distance_km,
      TIMESTAMP_DIFF(order_approved_at, order_purchase_timestamp, HOUR) AS seller_lead_time_approval_hours,
      TIMESTAMP_DIFF(review_answer_timestamp, review_creation_date, HOUR) AS seller_review_response_hours,
      DATE_DIFF(shipping_limit_date, order_delivered_carrier_date, DAY) AS seller_buffer_time_days
    FROM data_filtered_geo
  ),
  data_with_window_features AS (
    SELECT
      t1.*,
      COUNT(DISTINCT t1.order_id) OVER (PARTITION BY t1.seller_id) AS order_nunique,
      COUNT(DISTINCT t1.product_id) OVER (PARTITION BY t1.seller_id) AS product_nunique,
      COUNT(DISTINCT t1.customer_unique_id) OVER (PARTITION BY t1.seller_id) AS customer_nunique,
      COUNT(t1.order_item_id) OVER (PARTITION BY t1.seller_id) AS item_count,
      MAX(t1.order_delivered_carrier_date) OVER () AS global_max_delivery_date,
      MIN(t1.order_delivered_carrier_date) OVER (PARTITION BY t1.seller_id) AS seller_first_delivery_date,
      MAX(t1.order_delivered_carrier_date) OVER (PARTITION BY t1.seller_id) AS seller_last_delivery_date
    FROM data_with_features AS t1
  ),
  data_with_final_features AS (
    SELECT
      t1.*,
      t2.price_sum_valid, t2.payment_sum_valid, t2.price_min_valid, t2.price_max_valid, t2.price_mean_valid,
      t3.freight_sum_all,
      SAFE_DIVIDE(t1.order_nunique, t1.product_nunique) AS order_product_ratio,
      SAFE_DIVIDE(t1.item_count, t1.order_nunique) AS avg_items_per_order,
      SAFE_DIVIDE(t2.payment_sum_valid, t1.order_nunique) AS gmv_per_order,
      SAFE_DIVIDE(t2.payment_sum_valid, t1.customer_nunique) AS gmv_per_customer,
      SAFE_DIVIDE(t3.freight_sum_all, t2.payment_sum_valid) AS freight_gmv_ratio,
      (t2.price_max_valid - t2.price_min_valid) AS price_range,
      SAFE_DIVIDE((t2.price_max_valid - t2.price_min_valid), t2.price_mean_valid) AS price_range_normalized,
      DATE_DIFF(t1.global_max_delivery_date, t1.seller_first_delivery_date, DAY) AS account_age_days,
      DATE_DIFF(t1.global_max_delivery_date, t1.seller_last_delivery_date, DAY) AS recency_days,
      SAFE_DIVIDE(t2.price_sum_valid, t1.order_nunique) AS AOV
    FROM data_with_window_features AS t1
    INNER JOIN monetary_summary AS t2 ON t1.seller_id = t2.seller_id
    INNER JOIN freight_summary AS t3 ON t1.seller_id = t3.seller_id
  ),

  -- 8. Filter account_age > 30 hari & Hitung Activity Rate
  data_filtered_age AS (
    SELECT
      *,
      SAFE_DIVIDE(order_nunique, account_age_days) AS Activity_Rate
    FROM data_with_final_features
    WHERE account_age_days > 30
  ),

  -- ==========================================================
  -- BAGIAN 3: AGREGASI 
  -- ==========================================================
  final_aggregation AS (
    SELECT
      seller_id,

      -- Membuat kolom Churn
      CASE WHEN ANY_VALUE(recency_days) > 30 THEN 1 ELSE 0 END AS churn,

      -- Seller Info (MODE)
      ANY_VALUE(seller_city) AS seller_city_mode,
      ANY_VALUE(seller_state) AS seller_state_mode,

      -- Order & Product
      COUNT(DISTINCT order_id) AS order_id_nunique, COUNT(order_item_id) AS order_item_id_count, COUNT(DISTINCT product_id) AS product_id_nunique,

      -- Price (ALL)
      MIN(price) AS price_min, MAX(price) AS price_max, AVG(price) AS price_mean, SUM(price) AS price_sum, APPROX_QUANTILES(price, 2)[OFFSET(1)] AS price_median,

      -- Freight (ALL)
      MIN(freight_value) AS freight_value_min, MAX(freight_value) AS freight_value_max, AVG(freight_value) AS freight_value_mean, SUM(freight_value) AS freight_value_sum, APPROX_QUANTILES(freight_value, 2)[OFFSET(1)] AS freight_value_median,

      -- Customers & Order Status (MODE)
      COUNT(DISTINCT customer_id) AS customer_id_nunique, ANY_VALUE(order_status) AS order_status_mode,

      -- Payments (ALL)
      ANY_VALUE(payment_type) AS payment_type_mode,
      MIN(payment_installments) AS payment_installments_min, MAX(payment_installments) AS payment_installments_max, APPROX_QUANTILES(payment_installments, 2)[OFFSET(1)] AS payment_installments_median, AVG(payment_installments) AS payment_installments_mean,
      MIN(payment_value) AS payment_value_min, MAX(payment_value) AS payment_value_max, AVG(payment_value) AS payment_value_mean, SUM(payment_value) AS payment_value_sum, APPROX_QUANTILES(payment_value, 2)[OFFSET(1)] AS payment_value_median,

      -- Review Scores (ALL)
      MIN(review_score) AS review_score_min, MAX(review_score) AS review_score_max, AVG(review_score) AS review_score_mean, APPROX_QUANTILES(review_score, 2)[OFFSET(1)] AS review_score_median,

      -- Product Metadata (ALL)
      MIN(product_name_lenght) AS product_name_lenght_min, MAX(product_name_lenght) AS product_name_lenght_max, APPROX_QUANTILES(product_name_lenght, 2)[OFFSET(1)] AS product_name_lenght_median, AVG(product_name_lenght) AS product_name_lenght_mean,
      MIN(product_description_lenght) AS product_description_lenght_min, MAX(product_description_lenght) AS product_description_lenght_max, APPROX_QUANTILES(product_description_lenght, 2)[OFFSET(1)] AS product_description_lenght_median, AVG(product_description_lenght) AS product_description_lenght_mean,
      MIN(product_photos_qty) AS product_photos_qty_min, MAX(product_photos_qty) AS product_photos_qty_max, APPROX_QUANTILES(product_photos_qty, 2)[OFFSET(1)] AS product_photos_qty_median, AVG(product_photos_qty) AS product_photos_qty_mean,
      MIN(product_weight_g) AS product_weight_g_min, MAX(product_weight_g) AS product_weight_g_max, APPROX_QUANTILES(product_weight_g, 2)[OFFSET(1)] AS product_weight_g_median, AVG(product_weight_g) AS product_weight_g_mean,
      MIN(product_length_cm) AS product_length_cm_min, MAX(product_length_cm) AS product_length_cm_max, APPROX_QUANTILES(product_length_cm, 2)[OFFSET(1)] AS product_length_cm_median, AVG(product_length_cm) AS product_length_cm_mean,
      MIN(product_height_cm) AS product_height_cm_min, MAX(product_height_cm) AS product_height_cm_max, APPROX_QUANTILES(product_height_cm, 2)[OFFSET(1)] AS product_height_cm_median, AVG(product_height_cm) AS product_height_cm_mean,
      MIN(product_width_cm) AS product_width_cm_min, MAX(product_width_cm) AS product_width_cm_max, APPROX_QUANTILES(product_width_cm, 2)[OFFSET(1)] AS product_width_cm_median, AVG(product_width_cm) AS product_width_cm_mean,

      -- Category & Customer Info (MODE)
      ANY_VALUE(product_category_name_english) AS product_category_name_english_mode,

      -- TIME (BARU)
      MIN(order_delivered_carrier_date) AS order_delivered_carrier_date_min,
      MAX(order_delivered_carrier_date) AS order_delivered_carrier_date_max,

      -- Customer Area (MODE)
      ANY_VALUE(customer_city) AS customer_city_mode,
      ANY_VALUE(customer_state) AS customer_state_mode,

      -- Fitur Baru (Aggregasi)
      MIN(seller_customer_distance_km) AS seller_customer_distance_km_min, MAX(seller_customer_distance_km) AS seller_customer_distance_km_max, AVG(seller_customer_distance_km) AS seller_customer_distance_km_mean, APPROX_QUANTILES(seller_customer_distance_km, 2)[OFFSET(1)] AS seller_customer_distance_km_median,
      MIN(seller_review_response_hours) AS seller_review_response_hours_min, MAX(seller_review_response_hours) AS seller_review_response_hours_max, AVG(seller_review_response_hours) AS seller_review_response_hours_mean, APPROX_QUANTILES(seller_review_response_hours, 2)[OFFSET(1)] AS seller_review_response_hours_median,
      MIN(seller_lead_time_approval_hours) AS seller_lead_time_approval_hours_min, MAX(seller_lead_time_approval_hours) AS seller_lead_time_approval_hours_max, AVG(seller_lead_time_approval_hours) AS seller_lead_time_approval_hours_mean, APPROX_QUANTILES(seller_lead_time_approval_hours, 2)[OFFSET(1)] AS seller_lead_time_approval_hours_median,
      MIN(seller_buffer_time_days) AS seller_buffer_time_days_min, MAX(seller_buffer_time_days) AS seller_buffer_time_days_max, AVG(seller_buffer_time_days) AS seller_buffer_time_days_mean, APPROX_QUANTILES(seller_buffer_time_days, 2)[OFFSET(1)] AS seller_buffer_time_days_median,

      -- Fitur Baru (First/Unique Value)
      ANY_VALUE(avg_items_per_order) AS avg_items_per_order,
      ANY_VALUE(gmv_per_order) AS gmv_per_order,
      ANY_VALUE(gmv_per_customer) AS gmv_per_customer,
      ANY_VALUE(freight_gmv_ratio) AS freight_gmv_ratio,
      ANY_VALUE(price_range) AS price_range,
      ANY_VALUE(price_range_normalized) AS price_range_normalized,
      ANY_VALUE(account_age_days) AS account_age,
      ANY_VALUE(recency_days) AS recency,
      ANY_VALUE(Activity_Rate) AS Activity_Rate,
      ANY_VALUE(AOV) AS AOV

    FROM
      data_filtered_age
    GROUP BY
      1
  )

SELECT * FROM final_aggregation
);