import logging
import os
from dotenv import load_dotenv

from etl import (
    exceltocsv_run,
    renamefiles_run,
    csvtodb_run,
    allsales_run,
    dbtoparquet_run,
    loadproducts_run,
    volumes_run,
    tosplist_run,
    tosupabase_run,
)


load_dotenv()

# EXCEL TO DB
EXCEL_FOLDER = os.getenv("SLDB_EXCEL_FOLDER")
EXCEL_ARCHIVE_FOLDER = os.getenv("SLDB_EXCEL_ARCHIVE_FOLDER")
CSV_ARCHIVE_FOLDER = os.getenv("SLDB_CSV_ARCHIVE_FOLDER")
EXCEL_EXTENSIONS = eval(os.getenv("SLDB_EXCEL_EXTENSIONS"))
CSV_EXTENSIONS = eval(os.getenv("SLDB_CSV_EXTENSIONS"))
EXCEL_SHEET = os.getenv("SLDB_EXCEL_SHEET")


PDF_FOLDER = "data"
PDF_ARCHIVE_FOLDER = "data/fuel_archive"
PDF_EXTENSIONS = [".pdf"]
PDF_REGEX = r"(\w+)\s(\$\s\S+)\s(\$\s\S+)\s(\$\s\S+)\s(\$\s\S+)\s(\$\s\S+)\s(\$\s\S+)\s(\$\s\S+)"
PDF_PUMP_IDENTIFIER = "Dispenser"
PDF_FUEL_TYPES = ["unleaded", "Premium", "Diesel"]


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
TABLE_COLUMNS = {
    "sales": eval(os.getenv("SLDB_TABLE_COLUMNS")),
    "fuel": "dispenser,sales_date,fuel_type,fuel_sales,fuel_sales_discount,fuel_sales_paid,fuel_volume".split(
        ","
    ),
}

# JOBS CONFIGURATION
JOBS = {
    "exceltocsv": exceltocsv_run,
    "renamefiles": renamefiles_run,
    "csvtodb": csvtodb_run,
    "allsales": allsales_run,
    "toparquet": dbtoparquet_run,
    "loadproducts": loadproducts_run,
    "volumes": volumes_run,
    "tosplist": tosplist_run,
    "tosupabase": tosupabase_run,
}

# LOG CONFIGURATION
LOG_FOLDER = os.getenv("SLDB_LOGS_FOLDER")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG

# DATABASE CONFIGURATION
DATABASE = os.getenv("SLDB_DATABASE")
PARQUET = os.getenv("SLDB_PQT_FOLDER")
FUEL_PARQUET = os.getenv("SLDB_FPQT_FOLDER")
CSV = os.getenv("SLDB_CSV_FOLDER")
FUEL_CSV = os.getenv("SLDB_FCSV_FOLDER")

# YEAR CONFIGURATION
FIRST_YEAR = 2021

# PRODUCTS CONFIGURATION
PROD_FOLDER = os.getenv("SLDB_PROD_FOLDER")
PROD_COL_MAP = {
    "Scan Code": "product_id",
    "Item Name": "product_name",
    "Department": "product_category",
}
PROD_RAW_TABLE = "raw_product"
PROD_TABLE = "product"
ALLSALES_COLUMNS = eval(os.getenv("SLDB_ALLSALES_TABLE_COLUMNS"))


SHAREPOINT_URL = "https://gtmart234.sharepoint.com"
SHAREPOINT_SITE = "https://gtmart234.sharepoint.com/_layouts/15/sharepoint.aspx"  # "https://gtmart234-my.sharepoint.com/personal/walter_gtmart1_com"
SHAREPOINT_LIST = "Sales Data"
SHAREPOINT_USERNAME = "walter@gtmart1.com"
SHAREPOINT_PASSWORD = os.getenv("SLDB_SHP_PWD")

SHP_CLIENT_ID = os.getenv("SLDB_CLIENTID")
SHP_CLIENT_SECRET = os.getenv("SLDB_CLIENTSECRET")
SHP_TOKEN = os.getenv("SLDB_TOKEN")
POSTG_CON = os.getenv("POSTG_CON")
