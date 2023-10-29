import logging
import os
from dotenv import load_dotenv

from etl import (
    salestocsv_run,
    renamefiles_run,
    csvtodb_run,
    allsales_run,
    dbtoparquet_run,
    loadproducts_run,
    fueltocsv_run,
    tosplist_run,
    tosupabase_run,
    exceltocsv_run,
)


load_dotenv()

# EXCEL TO DB
PDF_SALES_FOLDER = os.getenv("SLDB_PDF_SALES_FOLDER")
PDF_SALES_ARCHIVE_FOLDER = os.getenv("SLDB_PDF_SALES_ARCHIVE_FOLDER")
PDF_SALES_REGEX = r"([0-9]+)\s([0-9]{1})\s(.+)\s(Grocery No Tax|Lottery|Grocery Tax|Beer|Scratch Sales|Automotive|Candy \/ Gum|Cigarette Carton|Cigarette Pack|Moist Tabacco|Liquor|Wine)\s([0-9]+)\s([$0-9.]+)\s([$0-9.]+)\s([0-9.%]+)\s([0-9.%]+)"
CSV_FOLDER = "data"
CSV_ARCHIVE_FOLDER = os.getenv("SLDB_CSV_ARCHIVE_FOLDER")
EXCEL_EXTENSIONS = eval(os.getenv("SLDB_EXCEL_EXTENSIONS"))
CSV_EXTENSIONS = eval(os.getenv("SLDB_CSV_EXTENSIONS"))
EXCEL_SHEET = os.getenv("SLDB_EXCEL_SHEET")
MONTH_MAP = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}

PDF_FUEL_FOLDER = "data/fuel"
PDF_FUEL_ARCHIVE_FOLDER = "data/fuel_archive"
PDF_EXTENSIONS = [".pdf"]
PDF_FUEL_REGEX = r"(\w+)\s(\$\s\S+)\s(\$\s\S+)\s(\$\s\S+)\s(\$\s\S+)\s(\$\s\S+)\s(\$\s\S+)\s(\$\s\S+)"
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
    "salestocsv": salestocsv_run,
    "exceltocsv": exceltocsv_run,
    "renamefiles": renamefiles_run,
    "csvtodb": csvtodb_run,
    "allsales": allsales_run,
    "toparquet": dbtoparquet_run,
    "loadproducts": loadproducts_run,
    "fueltocsv": fueltocsv_run,
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
FIRST_YEAR = 2020

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
ALLFUEL_COLUMNS = "dispenser,sales_date,fuel_type,fuel_sales,fuel_sales_discount,fuel_sales_paid,fuel_volume".split(
    ","
)


SHAREPOINT_URL = "https://gtmart234.sharepoint.com"
SHAREPOINT_SITE = "https://gtmart234.sharepoint.com/_layouts/15/sharepoint.aspx"  # "https://gtmart234-my.sharepoint.com/personal/walter_gtmart1_com"
SHAREPOINT_LIST = "Sales Data"
SHAREPOINT_USERNAME = "walter@gtmart1.com"
SHAREPOINT_PASSWORD = os.getenv("SLDB_SHP_PWD")

SHP_CLIENT_ID = os.getenv("SLDB_CLIENTID")
SHP_CLIENT_SECRET = os.getenv("SLDB_CLIENTSECRET")
SHP_TOKEN = os.getenv("SLDB_TOKEN")
POSTG_CON = os.getenv("POSTG_CON")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = "lake"
