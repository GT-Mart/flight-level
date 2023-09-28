CREATE TABLE all_fuel (
  dispenser VARCHAR,
  sales_date TIMESTAMP,
  fuel_type VARCHAR,
  fuel_sales FLOAT,
  fuel_sales_discount FLOAT,
  fuel_sales_paid FLOAT,
  fuel_volume FLOAT
);
CREATE TABLE all_sales (
  product_id bigint,
  product_name VARCHAR,
  product_category VARCHAR,
  package_qty FLOAT,
  sales_qty bigint,
  product_price FLOAT,
  sales_price FLOAT,
  category_pct FLOAT,
  day_pct FLOAT,
  sales_date TIMESTAMP
);
