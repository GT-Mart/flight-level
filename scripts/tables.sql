DROP TABLE IF EXISTS PUBLIC.all_fuel;
CREATE TABLE PUBLIC.all_fuel (
  dispenser VARCHAR NULL,
  sales_date TIMESTAMP NULL,
  fuel_type VARCHAR NULL,
  fuel_sales float8 NULL,
  fuel_sales_discount float8 NULL,
  fuel_sales_paid float8 NULL,
  fuel_volume float8 NULL,
  page int8 NULL
);
CREATE INDEX all_fuel_page_idx
ON PUBLIC.all_fuel USING btree (page);
-- Permissions
ALTER TABLE
  PUBLIC.all_fuel owner TO postgres;
GRANT ALL
  ON TABLE PUBLIC.all_fuel TO postgres;
GRANT ALL
  ON TABLE PUBLIC.all_fuel TO anon;
GRANT ALL
  ON TABLE PUBLIC.all_fuel TO authenticated;
GRANT ALL
  ON TABLE PUBLIC.all_fuel TO service_role;
DROP TABLE IF EXISTS PUBLIC.all_sales;
CREATE TABLE PUBLIC.all_sales (
    product_id int8 NULL,
    product_name VARCHAR NULL,
    product_category VARCHAR NULL,
    package_qty float8 NULL,
    sales_qty int8 NULL,
    product_price float8 NULL,
    sales_price float8 NULL,
    category_pct float8 NULL,
    day_pct float8 NULL,
    sales_date TIMESTAMP NULL,
    page int8 NULL
  );
CREATE INDEX all_sales_page_idx
  ON PUBLIC.all_sales USING btree (page);
-- Permissions
ALTER TABLE
  PUBLIC.all_sales owner TO postgres;
GRANT ALL
  ON TABLE PUBLIC.all_sales TO postgres;
GRANT ALL
  ON TABLE PUBLIC.all_sales TO anon;
GRANT ALL
  ON TABLE PUBLIC.all_sales TO authenticated;
GRANT ALL
  ON TABLE PUBLIC.all_sales TO service_role;
