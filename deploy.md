# GTMart Deploy

This file explains how the dpeloyment of the scripts were done on the GTMart computer.

## Software Installed

We have installed the following software:

1) Python - we have installed version 3.10.10
2) Git - we have installed the github client


## Installation Steps

1) Created folder on E: drive, called Projects

2) Inside the Projects folder, executed the command to download the GitHub repository: 
   `git clone https://github.com/GT-Mart/flight-level.git` 

3) After this download enter on the folder and run the commands:
   `python -m venv venv`
   `pip install -r requirements.txt`

4) If everything was installed correctly, then:
   - On the root of Projects folder, create a new folder called `scripts`
   - Copy from the original repository folder the following folders and files:
     - data
     - etl
     - logs
     - config.py
     - main.py

5) Create a .env file, that will need to contain the following variables configured:
```
SLDB_PDF_SALES_FOLDER="data"
SLDB_PDF_SALES_ARCHIVE_FOLDER = "data/archive"
SLDB_CSV_ARCHIVE_FOLDER = "data/csv_archive"
SLDB_EXCEL_EXTENSIONS = [".xlsx", ".xls", ".xlsm", ".xlsb"]
SLDB_CSV_EXTENSIONS = [".csv"]
SLDB_EXCEL_SHEET = "Table 1"
SLDB_EXCEL_COLUMNS = ["PLU No.","Pkg. Qty", "Description", "Department", "Count", "Price", "Sales", "% of Dept", "% of Total"]
SLDB_TABLE_COLUMNS = ["product_id", "package_qty", "product_name", "product_category", "sales_qty", "product_price", "sales_price", "category_pct", "day_pct", "sales_date"]
SLDB_DATABASE = "data/database/flight_sales.duckdb"
SLDB_LOGS_FOLDER = "logs"
SLDB_PQT_FOLDER = "/Users/wpcortes/VirtualBox VMs/powerbi/all_sales.parquet"
SLDB_FPQT_FOLDER = "/Users/wpcortes/VirtualBox VMs/powerbi/all_fuel.parquet"
SLDB_CSV_FOLDER = "data/all_sales.csv"
SLDB_FCSV_FOLDER = "data/all_fuel.csv"
SLDB_PROD_FOLDER = "data/products"
SLDB_ALLSALES_TABLE_COLUMNS = ["product_id", "product_name", "product_category", "package_qty", "sales_qty", "product_price", "sales_price", "category_pct", "day_pct", "sales_date"]
```

The variables above should be copied as is. The variables below will require you to use the email with the information.

```
SUPABASE_URL="<supabase url>"
SUPABASE_KEY="<supabase api key>"

POSTG_CON = "postgresql+psycopg2://postgres:<supabase db password>@<supabase db url>/postgres"
```

6) Copy the content of the `dash` folder Into the OneDrive folder called `Dash Board`

7) Inside the `Projects` folder create one .cmd file for each script:

- run_renamefiles.cmd
  ```cmd
  cd scripts
  python main.py renamefiles
  ```

- run_export_to_csv.cmd
  ```cmd
  cd scripts
  python main.py salestocsv fueltocsv
  ```

- run_import_to_db.cmd
  ```cmd
  cd scripts
  python main.py csvtodb allsales
  ```

- run_to_supabase.cmd
  ```cmd
  cd scripts
  python main.py tosupabase
  ```