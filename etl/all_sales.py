# -*- coding: utf-8 -*-
import datetime
import duckdb
import traceback

from .log import get_logger

logger = None


def create_all_sales_table(first_year, db, logger, fields):
    logger.info("Dropping current all_sales table...")
    db.sql("DROP TABLE IF EXISTS all_sales;")
    db.sql(
        "CREATE TABLE all_sales (product_id BIGINT, product_name VARCHAR, product_category VARCHAR, package_qty DOUBLE, sales_qty BIGINT, product_price DOUBLE, sales_price DOUBLE, category_pct DOUBLE, day_pct DOUBLE, sales_date TIMESTAMP);"
    )
    logger.info("Identifying daily sales table...")
    idx = first_year
    while idx <= datetime.datetime.now().year:
        logger.info(f"Processing year {idx}...")
        r1 = db.sql(
            f"SELECT 'SELECT {','.join(fields)} FROM '|| name FROM sqlite_master where type = 'table' AND name like 'sales_{idx}%' ORDER BY name"
        ).fetchall()

        tables = [query[0] for query in r1]
        logger.info(f"Insert content from {len(tables)} dates...")

        logger.info("Building insert statement...")
        create_table = f"""
          INSERT INTO all_sales({','.join(fields)}) {' UNION '.join(tables)}
        """

        try:
            logger.info("Running statement...")
            db.sql(create_table)
        except:
            logger.error(traceback.format_exc())
        idx += 1

    logger.info("Table created.")


def create_all_fuel_table(first_year, db, logger, fields):
    logger.info("Dropping current all_fuel table...")
    db.sql("DROP TABLE IF EXISTS all_fuel;")
    db.sql(
        "CREATE TABLE all_fuel (dispenser VARCHAR,sales_date TIMESTAMP,fuel_type VARCHAR,fuel_sales DOUBLE,fuel_sales_discount DOUBLE,fuel_sales_paid DOUBLE,fuel_volume DOUBLE);"
    )
    logger.info("Identifying daily fuel table...")
    idx = first_year
    while idx <= datetime.datetime.now().year:
        logger.info(f"Processing year {idx}...")
        r1 = db.sql(
            f"SELECT 'SELECT {','.join(fields)} FROM '|| name FROM sqlite_master where type = 'table' AND name like 'fuel_{idx}%' ORDER BY name"
        ).fetchall()

        tables = [query[0] for query in r1]
        logger.info(f"Insert content from {len(tables)} dates...")

        logger.info("Building insert statement...")
        create_table = f"""
          INSERT INTO all_fuel({','.join(fields)}) {' UNION '.join(tables)}
        """

        try:
            logger.info("Running statement...")
            db.sql(create_table)
        except:
            logger.error(traceback.format_exc())
        idx += 1

    logger.info("Table created.")


def create_product_table(db, logger, table_name, raw_table_name):
    logger.info("Creating PROD table...")
    db.sql(f"DROP TABLE IF EXISTS {table_name};")
    db.sql(
        f"CREATE TABLE {table_name} AS SELECT * FROM {raw_table_name} r WHERE exists (select 1 from all_sales where product_id = r.product_id)"
    )
    logger.info("PROD table created.")


def run(config, job_name):
    global logger
    i = 0
    logger = get_logger(job_name, config)

    logger.info("Connecting to the database...")
    con = duckdb.connect(config.DATABASE)

    logger.info(f"Creating all_sales table...")
    create_all_sales_table(config.FIRST_YEAR, con, logger, config.ALLSALES_COLUMNS)
    logger.info("all_sales table created.")

    create_product_table(con, logger, config.PROD_TABLE, config.PROD_RAW_TABLE)

    logger.info(f"Creating all_fuel table...")
    create_all_fuel_table(config.FIRST_YEAR, con, logger, config.TABLE_COLUMNS["fuel"])
    logger.info("all_fuel table created.")
