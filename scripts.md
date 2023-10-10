# GTMart Scripts

## Objective

This is the source code for the scripts that populate the database that serves as backend for the GTMart dashboard.

The GTMart dashboard is a Power BI report that display insights from the sales of Grocery and Fuel from the GTMart store.


## Technology used

The scripts were written using Python 3.10.X and uses the following libraries:
- Core
  - pandas
  - requests
  - typer
  - python-dotenv
  - pyarrow
- Excel manipulation
  - openpyxl
- PDF manipulation  
  - pdfplumber
- Database
  - duckdb
  - supabase
  - SQLAlchemy
  - psycopg2-binary

## How the scripts work

The scripts were executed through .bat files that are scheduled in a Power Automate flow.
The .bat files call the Main script (main.py) which based on the parameters sent, execute one of the following scripts:

1) Rename Files (etl/rename_files.py)
2) PDF to Sales CSV (etl/pdf_to_sales.py)
3) PDF to Fuel CSV (etl/pdf_to_volumes.py)
4) CSV to DB (etl/csv_to_db.py)
5) All Sales (etl/all_sales.py)
6) DB to Supabase (etl/db_to_supabase.py)

See the description of each script below.


### Rename Files

This code is a Python script that renames files in specific folders based on their extensions and certain patterns in their filenames. The code can be broken down into several parts.


1. **Function `rename`**:
```python
def rename(config, folder):
    ...
```
This function is designed to rename files in a specific folder based on their extensions:

   - It loops over each file in the specified folder.
   - Splits the file into its name and extension.
   - If the file extension matches a set of Excel extensions:
     - It renames the file to replace spaces, dashes, and the string "2202" with underscores and the string "2022" respectively.
   - If the file extension matches a set of PDF extensions:
     - It tries to split the filename into a prefix, a sales date, and an hour. Then, it reconstructs the filename in a new format.
     - If the split operation fails (for example, due to a file name that doesn't match the expected format), the renaming is skipped for that file.
   - If there's a new filename generated, it renames the original file to the new filename in the same directory.

1. **Function `run`**:
```python
def run(config, job_name):
    ...
```
This function is presumably meant to be the main function to be called when the script runs. It takes in a configuration object and a job name (although the job name is unused in the function). This function calls the previously defined `rename` function on two folders specified in the configuration: `PDF_SALES_FOLDER` and `PDF_FUEL_FOLDER`.

**Additional Context**:

- The actual values for `EXCEL_EXTENSIONS`, `PDF_EXTENSIONS`, `PDF_SALES_FOLDER`, and `PDF_FUEL_FOLDER` are expected to be defined in the passed `config` object. Without that information, we can't be sure what specific extensions or folders this script is working with.
- The renaming logic seems to be tailored to specific requirements, like renaming files with "2202" in their name to "2022".
- The error handling for the PDF renaming logic is quite broad: any error in the splitting and reconstruction process will just result in that file not being renamed.


### PDF to Sales CSV

This script performs a set of operations to parse and extract sales information from PDF files, then convert and save that information into CSV format. Below is an explanation of each part:

1. **Function `build_date`**:
   - Takes a filename and extracts sales year, day, and month from it.
   - Handles potential issues like month values greater than 12 or day values greater than 31.
   - Returns a `datetime` object using the extracted values.

2. **Function `parse`**:
   - Opens a PDF file from a specified folder.
   - Iterates through pages of the PDF.
   - Extracts rows of text and checks if they contain sales data.
   - It starts parsing after it identifies a header row ("PLU No."). Once this row is found, it starts extracting sales data based on a regex pattern (likely describing the format of the sales data in the PDF).
   - Each extracted row is transformed into a dictionary of values and appended to a `data` list.
   - Handles special characters like `$` and `%` in the sales data, converting them to appropriate number formats.
   - If a row doesn't match the regex but also isn't a header/footer ("Page" or "Total"), it's considered as a continuation of the product name of the last parsed row.

3. **Function `run`**:
   - Initializes the logger.
   - Iterates over all files in the sales PDF folder.
   - For each file with an extension matching the specified PDF extensions:
     1. Logs the file name.
     2. Builds the sales date from the filename.
     3. Parses the PDF to extract sales data.
     4. Converts the parsed data to a DataFrame and saves it as a CSV file with a filename based on the sales date.
     5. Moves the processed PDF to an archive folder.
   - Completes the process and logs the completion.

In summary, this script is designed to:

- Parse sales information from a collection of PDFs.
- Convert and save that data in CSV format.
- Move processed PDFs to an archive folder for record-keeping.

The script assumes specific naming conventions for the PDFs and a specific structure in the PDF content. The `config` object provides necessary parameters like folder paths, file extensions, and the regex pattern for parsing the PDF content.

### PDF to Fuel CSV

This script is designed to extract specific sales data from PDF files related to fuel transactions and then save that extracted data into CSV format. After processing, the original PDF files are moved to an archive folder. Here's a breakdown of the script:


1. **Function `build_date`**:
    - This function extracts a sales date from a filename.
    - The filename is assumed to have specific parts separated by underscores.
    - It also has some error handling to deal with possible issues in the date extracted from the filename, like an invalid month or day value.

2. **Function `parse_pdf`**:
    - Opens a PDF file from a specified folder and extracts text from it row by row.
    - Returns a list of extracted rows.

3. **Function `run`**:
    - This function carries out the main logic:
        1. Initializes the logger.
        2. Iterates over all files in the fuel PDF folder.
        3. For each file with an extension that matches the given configuration:
            - Extracts the sales date from the filename.
            - Parses the PDF and retrieves rows of text data.
            - Processes each row to extract details like the dispenser ID, fuel type, and various sales figures.
            - It assumes a specific structure/format in the PDF content.
            - The processed rows are accumulated in a data list.
            - If additional volume data is detected (possibly in a different section of the PDF), it's associated with previously processed rows.
            - The accumulated data is converted into a DataFrame and then saved as a CSV file.
            - The processed PDF is then moved to an archive folder for record-keeping.

In summary, this script:

- Parses fuel sales data from PDFs, focusing on specific metrics related to different fuel types, their sales amounts, discounts, and final amounts paid.
- Processes and saves this data into structured CSV files, naming them based on the sales date.
- Moves the processed PDFs to an archive directory for retention and to avoid reprocessing in the future.

The script relies heavily on configurations (`config`) that dictate folder paths, specific PDF extensions to look for, specific patterns in the PDF content to parse, and more.

### CSV To DB

This script is designed to read CSV files, which store sales data, and then save that data into a database. Here's a breakdown of the script:


1. **Function `build_date`**:
   - This function aims to extract a sales date from a filename. 
   - The filename is expected to be in a particular format with parts separated by underscores.
   - It includes some error handling for possible invalid dates.
  
2. **Function `save_to_database`**:
   - Given a filename and sales date, this function reads the data from the CSV file and saves it into a database table.
   - Based on the prefix of the filename (either "sales" or something else), specific processing steps and SQL table creation commands are executed.
   - If an error occurs, it logs the traceback of the error for debugging purposes.

3. **Function `run`**:
   - This is the main driver function.
     1. Initializes the logger.
     2. Connects to a database using `duckdb`.
     3. Iterates over all the files in a specified CSV folder.
     4. For each CSV file:
        - It extracts the sales date from the filename.
        - Calls the `save_to_database` function to process and save the data.
        - If the data was successfully saved, the CSV file is then moved to an archive folder.
  
4. **Database Table Creation**:
   - The script uses SQL commands to create tables in a `duckdb` database. The table structure depends on the prefix of the filename.
   - For "sales" prefix: The table will have columns like product_id, package_qty, etc.
   - For any other prefix: The table will have columns related to fuel sales.

5. **CSV File Naming Convention**:
   - The script assumes the CSV filenames contain the year, month, and day of the sales data they hold.
   - It also assumes an additional prefix (like "sales") to determine the nature of the data.

6. **Special Processing for "Sales"**:
   - If the prefix is "sales", the script goes through additional preprocessing for the data, like removing rows with NaN values in the "product_id" column or formatting product IDs.

7. **Database Interaction**:
   - Tables are created, existing ones are dropped if they exist, and data is inserted into the database.

8.  **File Archiving**:
   - Once a CSV file's data has been successfully saved to the database, that file is moved to an archive folder.

In essence, the script ingests sales data from CSV files into a `duckdb` database. It handles both general sales and fuel sales, formats the data as necessary, creates or overwrites database tables, and archives processed CSV files.


### All Sales

The script focuses on data consolidation in a `duckdb` database. It deals with sales data, including general sales and fuel sales. Here's a breakdown of the script:


1. **Function `create_all_sales_table`**:
   - This function aims to create a consolidated table (`all_sales`) of sales data across multiple years.
   - It first drops the existing `all_sales` table, if it exists.
   - Then, for each year from the `first_year` to the current year:
     1. It identifies all tables prefixed with "sales_" followed by that year.
     2. Constructs a SQL query to union the content of these tables.
     3. Inserts the consolidated data into the `all_sales` table.

2. **Function `create_all_fuel_table`**:
   - Similar to the previous function but focuses on fuel data. 
   - It creates a consolidated table (`all_fuel`) for fuel sales data.
   - This also checks for each year's tables starting with `fuel_` followed by the year, unions the data, and then saves the consolidated data.

3. **Function `create_product_table`**:
   - This function focuses on creating a product table from raw product data.
   - The purpose seems to be creating a table that only includes products that have corresponding sales.
   - It creates the new table by selecting all entries from the raw table that exist in the `all_sales` table.

4. **Function `run`**:
   - This is the main driver function.
   - Initializes the logger.
   - Connects to a database using `duckdb`.
   - Calls the previous functions to:
     1. Create the `all_sales` table.
     2. Create the product table.
     3. Create the `all_fuel` table.

5. **Database Table Creation**:
   - The script consolidates data from multiple tables into singular tables (`all_sales`, `all_fuel`), possibly for easier querying or reporting.
   - During this consolidation, some older tables might be queried for their structure, so the script can identify which tables to consolidate.

In essence, this script's primary purpose is to consolidate data from multiple tables, possibly scattered across years, into a few master tables. This might be part of a monthly or yearly ETL (Extract, Transform, Load) process where data from different sources or tables is brought together for easier access and querying.

### DB To Supabase

The given code is designed to fetch sales and fuel data from a `duckdb` database and then save this data into a PostgreSQL database. Let's break down the code:

1. **Function `run`**:
   - This is the primary function that carries out the data migration process.
   
   1. **Logger Initialization**:
      - The logger is initialized using the provided `job_name` and `config`.
   
   2. **Connect to duckdb Database**:
      - A connection to a `duckdb` database is established using the connection string provided in the `config`.
   
   3. **Fetch Sales Data**:
      - A SQL query fetches sales data from the `all_sales` table and joins it with the `product` table using the `product_id` as the key. The `coalesce` function is used to choose non-null values between the two tables.
      - The query result is converted into a pandas DataFrame (`df`).
   
   4. **Connect to PostgreSQL Database**:
      - A connection to a PostgreSQL database is established using the `create_engine` function from the `sqlalchemy` library.
      - Within the established connection:
        1. The `all_sales` table in the PostgreSQL database is truncated (emptied).
        2. Data from the `df` DataFrame is saved into the `all_sales` table of the PostgreSQL database using the `to_sql` method. The data is appended in chunks of 10,000 rows.
        
   5. **Fetch Fuel Data**:
      - Similarly, the fuel data is fetched from the `all_fuel` table in the `duckdb` database and converted into another DataFrame (`df2`).
   
   6. **Save Fuel Data to PostgreSQL Database**:
      - The fuel data from the `df2` DataFrame is saved into the `all_fuel` table of the PostgreSQL database, again in chunks of 10,000 rows.
   
   7. **Logging**:
      - Throughout the process, the logger is used to log messages about what the script is doing, such as when it's connecting to databases, the size of fetched data, and when data has been saved.

In summary, the code's primary function is to migrate data from two tables (`all_sales` and `all_fuel`) in a `duckdb` database to a PostgreSQL database. It first fetches data, processes it a bit (in the case of sales data), and then saves it to the respective tables in the PostgreSQL database.

