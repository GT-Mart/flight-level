import logging
import os
from dotenv import load_dotenv

from etl import (
    exceltocsv_run,
    renamefiles_run,
    exceltodb_run,
    allsales_run,
    dbtoparquet_run,
)


load_dotenv()

# EXCEL TO DB
EXCEL_FOLDER = os.getenv("SLDB_EXCEL_FOLDER")
EXCEL_ARCHIVE_FOLDER = os.getenv("SLDB_EXCEL_ARCHIVE_FOLDER")
CSV_ARCHIVE_FOLDER = os.getenv("SLDB_CSV_ARCHIVE_FOLDER")
EXCEL_EXTENSIONS = eval(os.getenv("SLDB_EXCEL_EXTENSIONS"))
CSV_EXTENSIONS = eval(os.getenv("SLDB_CSV_EXTENSIONS"))
EXCEL_SHEET = os.getenv("SLDB_EXCEL_SHEET")

# COLUMNS CONFIGURATION
COL_MAP = {
    "PLU No.": "product_id",
    "Pkg. Qty": "package_qty",
    "Description": "product_name",
    "Department": "product_category",
    "Count": "sales_qty",
    "Price": "product_price",
    "Sales": "sales_price",
    "% of Dept": "category_pct",
    "% of Total": "day_pct",
}
EXCEL_COLUMNS = eval(os.getenv("SLDB_EXCEL_COLUMNS"))
TABLE_COLUMNS = eval(os.getenv("SLDB_TABLE_COLUMNS"))

# JOBS CONFIGURATION
JOBS = {
    "exceltocsv": exceltocsv_run,
    "renamefiles": renamefiles_run,
    "exceltodb": exceltodb_run,
    "allsales": allsales_run,
    "toparquet": dbtoparquet_run,
}

# LOG CONFIGURATION
LOG_FOLDER = os.getenv("SLDB_LOGS_FOLDER")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG

# DATABASE CONFIGURATION
DATABASE = os.getenv("SLDB_DATABASE")
PARQUET = os.getenv("SLDB_PQT_FOLDER")

# YEAR CONFIGURATION
FIRST_YEAR = 2021
