# -*- coding: utf-8 -*-
import os
import datetime
import shutil
import pandas as pd
import duckdb
import traceback

from .log import get_logger

logger = None


def build_date(filename):
    global logger
    name_parts = filename.split("_")
    if len(name_parts) >= 3:
        sales_year = int(name_parts[0])
        sales_day = int(name_parts[2])
        sales_month = int(name_parts[1])

        if sales_month > 12:
            sales_day = int(name_parts[1])
            sales_month = int(name_parts[2])

        if sales_day > 31:
            sales_day = int(name_parts[2][0:2])
    else:
        logger.info("filename is not formatted correctly")
        return None

    return datetime.datetime(sales_year, sales_month, sales_day)


def save_to_database(filename, sales_date, db, config):
    global logger
    prefix = filename.split("_")[3].replace(".csv", "")
    sql_table = f"{prefix}_{sales_date.strftime('%Y%m%d')}"
    col_map = config.COL_MAP
    fields = config.TABLE_COLUMNS[prefix]

    try:
        logger.info("Loading the file...")
        pre_data = pd.read_csv(filename)
        if prefix == "sales":
            pre_data["sales_date"] = sales_date
            pre_data.rename(columns=col_map, inplace=True)
            pre_data.dropna(subset=["product_id"], inplace=True)
            pre_data["product_id"] = pre_data["product_id"].astype(str)
            pre_data["product_id"] = pre_data["product_id"].str.replace(".0", "")
            pre_data.query(
                "~product_id.str.contains('Total PLU')", engine="python", inplace=True
            )

            pre_data["product_id"] = pre_data["product_id"].apply(
                lambda x: x[:-1] if len(x) == 11 or len(x) == 12 else x
            )

            pre_data["product_id"] = pre_data["product_id"].astype(int)

        logger.info("Saving the data to database...")
        db.sql(f"DROP TABLE IF EXISTS {sql_table};")

        if prefix == "sales":
            db.sql(
                f"CREATE TABLE {sql_table} (product_id BIGINT, package_qty DOUBLE, product_name VARCHAR, product_category VARCHAR, sales_qty BIGINT, product_price DOUBLE, sales_price DOUBLE, category_pct DOUBLE, day_pct DOUBLE, sales_date TIMESTAMP);"
            )
        else:
            db.sql(
                f"CREATE TABLE {sql_table} (dispenser VARCHAR,sales_date TIMESTAMP,fuel_type VARCHAR,fuel_sales DOUBLE,fuel_sales_discount DOUBLE,fuel_sales_paid DOUBLE,fuel_volume DOUBLE);"
            )

        db.sql(
            f"INSERT INTO {sql_table}({','.join(fields)}) SELECT {','.join(fields)} FROM pre_data"
        )

        logger.info(f"Data saved into the table {sql_table}...")
        return True
    except:
        logger.error(traceback.format_exc())
        return False


def run(config, job_name):
    global logger
    i = 0
    logger = get_logger(job_name, config)

    logger.info("Ingesting CSV files into database...")

    logger.info("Connecting to the database...")
    con = duckdb.connect(config.DATABASE)

    logger.info(
        f"Processing available csv files on the folder {config.EXCEL_FOLDER}..."
    )

    for file in os.listdir(config.EXCEL_FOLDER):
        filename, ext = os.path.splitext(file)
        csvfilename = os.path.join(config.EXCEL_FOLDER, file)
        archivecsvfilename = os.path.join(config.CSV_ARCHIVE_FOLDER, file)

        if ext in config.CSV_EXTENSIONS:
            logger.info(f"Processing file {csvfilename} ...")

            sales_date = build_date(filename)
            if sales_date:
                logger.info(f"Processing sales for date: {sales_date}")
                data_saved = save_to_database(csvfilename, sales_date, con, config)
                if data_saved:
                    shutil.move(csvfilename, archivecsvfilename)
                    logger.info(f"File {csvfilename} saved into database.")
                else:
                    logger.error(f"File {csvfilename} was not saved into database.")

    logger.info("Process finished.")
