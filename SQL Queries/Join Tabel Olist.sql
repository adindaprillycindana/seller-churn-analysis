
## Merubah nama kolom pada tabel product_category_name_translation
-- ALTER TABLE olist.product_category_name_translation
-- RENAME COLUMN string_field_0 TO product_category_name;
-- ALTER TABLE  olist.product_category_name_translation
-- RENAME COLUMN string_field_1 TO product_category_name_english;

## Membuat tabel seller_orders, join 8 tabel
CREATE TABLE olist.seller_orders AS
SELECT
  s.*,
  oi.* EXCEPT(seller_id),                     -- hilangkan kolom join yang bentrok
  o.* EXCEPT(order_id),
  op.* EXCEPT(order_id),
  r.*EXCEPT(order_id),
  p.* EXCEPT(product_id),
  ct.product_category_name_english,
  c.* EXCEPT(customer_id)
FROM `olist.olist_sellers_dataset` s
LEFT JOIN `olist.olist_order_items_dataset` oi ON s.seller_id = oi.seller_id
LEFT JOIN `olist.olist_orders_dataset` o ON oi.order_id = o.order_id
LEFT JOIN `olist.olist_order_payments_dataset` op ON oi.order_id = op.order_id
LEFT JOIN `olist.olist_order_reviews_dataset` r ON oi.order_id = r.order_id
LEFT JOIN `olist.olist_products_dataset` p ON oi.product_id = p.product_id
LEFT JOIN `olist.product_category_name_translation` ct ON p.product_category_name = ct.product_category_name
LEFT JOIN `olist.olist_customers_dataset` c ON o.customer_id = c.customer_id;

## Agregasi tabel geolocation karena satu zip code ada banyak lat, lng
CREATE TABLE `olist.geo_slim` AS
SELECT
  geolocation_zip_code_prefix,

  -- median latitude
  APPROX_QUANTILES(geolocation_lat, 2)[OFFSET(1)] AS geolocation_lat,

  -- median longitude
  APPROX_QUANTILES(geolocation_lng, 2)[OFFSET(1)] AS geolocation_lng,

  -- mode city
  ARRAY_AGG(geolocation_city ORDER BY geolocation_city DESC LIMIT 1)[OFFSET(0)] AS geolocation_city,

  -- mode state
  ARRAY_AGG(geolocation_state ORDER BY geolocation_state DESC LIMIT 1)[OFFSET(0)] AS geolocation_state

FROM `olist.olist_geolocation_dataset`
GROUP BY geolocation_zip_code_prefix;

## Membuat tabel geolocation untuk seller
CREATE TABLE olist.geo_seller AS
SELECT
    geolocation_zip_code_prefix AS seller_zip_code_prefix,
    geolocation_lat  AS seller_lat,
    geolocation_lng  AS seller_lng,
    geolocation_city AS seller_geo_city,
    geolocation_state AS seller_geo_state
FROM olist.geo_slim;

## Membuat tabel geolocation untuk customer
CREATE TABLE olist.geo_customer AS
SELECT
    geolocation_zip_code_prefix AS customer_zip_code_prefix,
    geolocation_lat  AS customer_lat,
    geolocation_lng  AS customer_lng,
    geolocation_city AS customer_geo_city,
    geolocation_state AS customer_geo_state
FROM olist.geo_slim;

## Join tabel seller_orders dengan geo_seller dan geo_customer
CREATE TABLE olist.seller_final AS
SELECT
    so.*,
    gs.seller_lat,
    gs.seller_lng,
    gs.seller_geo_city,
    gs.seller_geo_state,
    gc.customer_lat,
    gc.customer_lng,
    gc.customer_geo_city,
    gc.customer_geo_state
FROM olist.seller_orders so
LEFT JOIN olist.geo_seller gs
    ON so.seller_zip_code_prefix = gs.seller_zip_code_prefix
LEFT JOIN olist.geo_customer gc
    ON so.customer_zip_code_prefix = gc.customer_zip_code_prefix;




