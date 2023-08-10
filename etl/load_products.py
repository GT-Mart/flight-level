# -*- coding: utf-8 -*-
import os
import pandas as pd
import duckdb

from .log import get_logger

logger = None


def saveas(file_path, col_map=None, db=None, table=None):
    # Open the Excel workbook
    pre_data = pd.read_excel(file_path)
    pre_data.rename(columns=col_map, inplace=True)
    pre_data["product_id"] = pre_data["product_id"].astype(int)

    if db and table:
        db.sql(f"DROP TABLE IF EXISTS {table};")
        db.sql(
            f"CREATE TABLE {table} (product_id BIGINT, product_name VARCHAR, product_category VARCHAR);"
        )
        db.sql(
            f"INSERT INTO {table} SELECT product_id, product_name, product_category from pre_data"
        )


def run(config, job_name):
    global logger
    i = 0
    logger = get_logger(job_name, config)

    logger.info("Connecting to the database...")
    con = duckdb.connect(config.DATABASE)

    logger.info("Starting process to load products into database...")
    for file in os.listdir(config.PROD_FOLDER):
        filename, ext = os.path.splitext(file)
        if ext in config.EXCEL_EXTENSIONS:
            logger.info(file)
            saveas(
                os.path.join(config.PROD_FOLDER, file),
                col_map=config.PROD_COL_MAP,
                db=con,
                table=config.PROD_RAW_TABLE,
            )
    logger.info("Process completed.")
