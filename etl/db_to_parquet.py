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
    logger.info(f"Saving data at: {config.PARQUET}")
    df.to_parquet(config.PARQUET)
    # df.to_csv(config.CSV)

    logger.info(f"Loading fuel data...")
    df2 = con.query(
        """select dispenser,
                      sales_date,
                      fuel_type,
                      fuel_sales,
                      fuel_sales_discount,
                      fuel_sales_paid,
                      fuel_volume,
                      page
               from all_fuel
            """
    ).to_df()
    logger.info(f" Size of the data: {df2.shape}")
    logger.info(f"Saving data at: {config.FUEL_PARQUET}")
    df2.to_parquet(config.FUEL_PARQUET)
    # df2.to_csv(config.FUEL_CSV)
    logger.info("Data dumped.")
