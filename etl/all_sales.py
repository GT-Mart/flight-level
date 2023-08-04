# -*- coding: utf-8 -*-
import datetime
import duckdb

from .log import get_logger

logger = None


def create_all_sales_table(first_year, db, logger, fields):
    logger.info("Dropping current all_sales table...")
    db.sql("DROP TABLE IF EXISTS all_sales;")
    logger.info("Identifying daily sales table...")
    idx = first_year
    while idx <= datetime.datetime.now().year:
        logger.info(f"Processing year {idx}...")
        r1 = db.sql(
            f"SELECT 'SELECT {','.join(fields)} FROM '|| name FROM sqlite_master where type = 'table' AND name like 'sales_{idx}%' ORDER BY name"
        ).fetchall()

        tables = [query[0] for query in r1]
        logger.info(f"Insert content from {len(tables)} dates...")

        if idx == first_year:
            logger.info("Building create statement...")
            create_table = f"""
          CREATE TABLE all_sales AS {' UNION '.join(tables)}
        """
        else:
            logger.info("Building insert statement...")
            create_table = f"""
          INSERT INTO all_sales({','.join(fields)}) {' UNION '.join(tables)}
        """
        logger.info("Running statement...")
        db.sql(create_table)
        idx += 1

    logger.info("Table created.")


def run(config, job_name):
    global logger
    i = 0
    logger = get_logger(job_name, config)

    logger.info("Ingesting CSV files into database...")

    logger.info("Connecting to the database...")
    con = duckdb.connect(config.DATABASE)

    logger.info(f"Creating all_sales table...")
    create_all_sales_table(config.FIRST_YEAR, con, logger, config.TABLE_COLUMNS)
    logger.info("all_sales table created.")
