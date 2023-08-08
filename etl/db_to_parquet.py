# -*- coding: utf-8 -*-
import duckdb
import pandas as pd

from .log import get_logger

logger = None


def run(config, job_name):
    global logger
    i = 0
    logger = get_logger(job_name, config)

    logger.info("Migrating data to parquet format...")

    logger.info("Connecting to the database...")
    con = duckdb.connect(config.DATABASE)

    logger.info(f"Loading data...")
    df = con.query(
        "select * from all_sales where product_id[1] in ('0','1','2','3','4','5','6','7','8','9')"
    ).to_df()
    df.to_parquet(config.PARQUET)
    logger.info("Data dumped.")
