# -*- coding: utf-8 -*-
import os
import datetime
import shutil
import pandas as pd
import duckdb
import traceback

from .log import get_logger
from .all_sales import create_all_sales_table

logger = None


def build_date(filename):
    global logger
    name_parts = filename.split("_")
    if len(name_parts) >= 3:
        sales_year = int(name_parts[0])
        sales_day = int(name_parts[1])
        sales_month = int(name_parts[2])

        if sales_month > 12:
            sales_day = int(name_parts[2])
            sales_month = int(name_parts[1])

        if sales_day > 31:
            sales_day = int(name_parts[1][0:2])
    else:
        logger.info("filename is not formatted correctly")
        return None

    return datetime.datetime(sales_year, sales_month, sales_day)


def save_to_database(filename, sales_date, db, col_map, fields):
    global logger
    sql_table = f"sales_{sales_date.strftime('%Y%m%d')}"

    try:
        logger.info("Loading the file...")
        pre_data = pd.read_csv(filename)
        pre_data["sales_date"] = sales_date
        pre_data.rename(columns=col_map, inplace=True)
        pre_data.dropna(subset=["product_id"], inplace=True)

        logger.info("Saving the data to database...")
        db.sql(f"DROP TABLE IF EXISTS {sql_table};")

        db.sql(
            f"CREATE TABLE {sql_table} (product_id VARCHAR, package_qty DOUBLE, product_name VARCHAR, product_category VARCHAR, sales_qty BIGINT, product_price DOUBLE, sales_price DOUBLE, category_pct DOUBLE, day_pct DOUBLE, sales_date TIMESTAMP);"
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
    changes_in_database = False
    for file in os.listdir(config.EXCEL_FOLDER):
        filename, ext = os.path.splitext(file)
        csvfilename = os.path.join(config.EXCEL_FOLDER, file)
        archivecsvfilename = os.path.join(config.CSV_ARCHIVE_FOLDER, file)

        if ext in config.CSV_EXTENSIONS:
            logger.info(f"Processing file {csvfilename} ...")

            sales_date = build_date(filename)
            if sales_date:
                logger.info(f"Processing sales for date: {sales_date}")
                data_saved = save_to_database(
                    csvfilename, sales_date, con, config.COL_MAP, config.TABLE_COLUMNS
                )
                if data_saved:
                    shutil.move(csvfilename, archivecsvfilename)
                    logger.info(f"File {csvfilename} saved into database.")
                    changes_in_database = True
                else:
                    logger.error(f"File {csvfilename} was not saved into database.")

    if changes_in_database:
        logger.info("Recreating the all_sales table...")
        create_all_sales_table(config.FIRST_YEAR, con, logger, config.TABLE_COLUMNS)

    logger.info("Process finished.")
