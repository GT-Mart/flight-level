# -*- coding: utf-8 -*-
import os
import duckdb
import pandas as pd

from sqlalchemy import create_engine, text

from .log import get_logger

logger = None


def run(config, job_name):
    global logger
    i = 0
    logger = get_logger(job_name, config)

    logger.info("Migrating data to parquet format...")

    logger.info("Connecting to the database...")
    con = duckdb.connect(config.DATABASE)

    logger.info(f"Loading sales data...")
    df = con.query(
        """select  a.product_id, 
                   coalesce(p.product_name, a.product_name) as product_name,
                   coalesce(p.product_category, a.product_category) as product_category,
                   a.package_qty,
                   a.sales_qty,
                   a.product_price,
                   a.sales_price,
                   a.category_pct,
                   a.day_pct,
                   a.sales_date,
                   a.page
           from all_sales a left join product p on a.product_id = p.product_id
        """
    ).to_df()
    logger.info(f" Size of the data: {df.shape}")
    logger.info(f"Saving data at Postgres Database...")

    my_eng = create_engine(config.POSTG_CON)
    with my_eng.connect() as my_conn:
        my_conn.execute(text(f"TRUNCATE TABLE all_sales"))
        my_conn.commit()
        df.to_sql(
            "all_sales", my_conn, if_exists="append", index=False, chunksize=10000
        )

        logger.info(f"Loading fuel data...")
        df2 = con.query(
            """select  *
               from all_fuel
            """
        ).to_df()
        logger.info(f" Size of the data: {df2.shape}")
        logger.info(f"Saving data at Postgres Database...")
        df2.to_sql(
            "all_fuel", my_conn, if_exists="append", index=False, chunksize=10000
        )

    logger.info("Data dumped.")
