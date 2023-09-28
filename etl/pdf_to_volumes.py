# -*- coding: utf-8 -*-
import shutil
import pdfplumber
import pandas as pd
import re
import os
import datetime

from etl.log import get_logger

logger = None


def build_date(filename):
    global logger
    name_parts = filename.split("_")
    if len(name_parts) >= 4:
        sales_year = int(name_parts[1])
        sales_day = int(name_parts[2])
        sales_month = int(name_parts[3])

        if sales_month > 12:
            sales_day = int(name_parts[3])
            sales_month = int(name_parts[2])

        if sales_day > 31:
            sales_day = int(name_parts[2][0:2])
    else:
        logger.info("filename is not formatted correctly")
        return None

    return datetime.datetime(sales_year, sales_month, sales_day)


def parse_pdf(config, filename):
    raw_data = []
    pdf = pdfplumber.open(os.path.join(config.PDF_FUEL_FOLDER, filename))
    for page in pdf.pages:
        for row in page.extract_text_lines():
            raw_data.append(row)
    pdf.close()
    return raw_data


def run(config, job_name):
    global logger

    logger = get_logger(job_name, config)

    logger.info("Starting processing fueld pdf files...")
    for file in os.listdir(config.PDF_FUEL_FOLDER):
        filename, ext = os.path.splitext(file)
        if ext in config.PDF_EXTENSIONS:
            logger.info(f"Processing file {file}")
            sales_date = build_date(filename)
            rows = parse_pdf(config, file)
            data = []
            volumes = []
            orig_record = {}
            for item in rows:
                if config.PDF_PUMP_IDENTIFIER in item["text"]:
                    orig_record = {
                        "dispenser": item["text"].strip(),
                        "sales_date": sales_date,
                    }
                else:
                    fuel_type = item["text"].split(" ")[0]
                    if fuel_type in config.PDF_FUEL_TYPES:
                        matches = re.finditer(
                            config.PDF_FUEL_REGEX, item["text"], re.MULTILINE
                        )
                        mat_list = list(matches)
                        if len(mat_list) > 0:
                            values = list(mat_list[0].groups())
                            record = orig_record.copy()
                            record["fuel_type"] = values[0]
                            record["fuel_sales"] = (
                                values[1].replace("$ ", "").replace(",", "")
                            )
                            record["fuel_sales_discount"] = (
                                values[3].replace("$ ", "").replace(",", "")
                            )
                            record["fuel_sales_paid"] = (
                                values[6].replace("$ ", "").replace(",", "")
                            )
                            data.append(record)
                        else:
                            volumes.append(item["text"])

            if len(volumes) > 0:
                for idx, item in enumerate(volumes):
                    if idx < len(data):
                        values = item.split(" ")
                        if len(values) == 5:
                            data[idx]["fuel_volume"] = values[4].replace(",", "")

            rows_added = False
            if len(data) > 0:
                raw_df = pd.DataFrame(data)
                raw_df.to_csv(
                    os.path.join(
                        config.CSV_FOLDER,
                        f"{sales_date.year}_{sales_date.month}_{sales_date.day}_fuel.csv",
                    ),
                    index=False,
                )
                rows_added = True

            if rows_added:
                file_path = os.path.join(config.PDF_FUEL_FOLDER, file)
                archive_path = os.path.join(config.PDF_FUEL_ARCHIVE_FOLDER, file)
                shutil.move(file_path, archive_path)
