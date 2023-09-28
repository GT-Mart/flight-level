# -*- coding: utf-8 -*-
import pdfplumber
import pandas as pd
import re
import os
import shutil
import datetime

from .log import get_logger

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


def parse(config, file, sales_date):
    pdf = pdfplumber.open(os.path.join(config.PDF_SALES_FOLDER, file))
    data = []
    start_parse = False
    for page in pdf.pages:
        rows = page.extract_text_lines()
        for item in rows:
            if "PLU No." in item["text"]:
                start_parse = True
            else:
                if start_parse:
                    matches = re.finditer(
                        config.PDF_SALES_REGEX, item["text"], re.MULTILINE
                    )
                    mat_list = list(matches)
                    if len(mat_list) > 0:
                        for idx, match in enumerate(mat_list, start=1):
                            values = list(match.groups())
                            data.append(
                                {
                                    "sales_date": sales_date,
                                    "product_id": values[0],
                                    "package_qty": int(values[1]),
                                    "product_name": values[2],
                                    "product_category": values[3],
                                    "sales_qty": float(values[4]),
                                    "product_price": float(values[5].replace("$", "")),
                                    "sales_price": float(values[6].replace("$", "")),
                                    "category_pct": round(
                                        float(values[7].replace("%", "")) / 100, 5
                                    ),
                                    "day_pct": round(
                                        float(values[8].replace("%", "")) / 100, 5
                                    ),
                                }
                            )
                    else:
                        if "Page" not in item["text"] and "Total" not in item["text"]:
                            if len(data) > 0:
                                data[len(data) - 1]["product_name"] += (
                                    " " + item["text"]
                                )
    pdf.close()
    return data


def run(config, job_name):
    global logger
    i = 0
    logger = get_logger(job_name, config)

    logger.info("Starting process to convert excel files to csv...")
    for file in os.listdir(config.PDF_SALES_FOLDER):
        filename, ext = os.path.splitext(file)
        if ext in config.PDF_EXTENSIONS:
            logger.info(file)
            sales_date = build_date(filename)

            logger.info("Parsing PDF...")
            data = parse(config, file, sales_date)

            logger.info("Saving the CSV...")
            raw_df = pd.DataFrame(data)
            raw_df.to_csv(
                os.path.join(
                    config.CSV_FOLDER,
                    f"{sales_date.year}_{sales_date.month}_{sales_date.day}_sales.csv",
                ),
                index=False,
            )
            logger.info("Archiving the PDF...")
            file_path = os.path.join(config.PDF_SALES_FOLDER, file)
            archive_path = os.path.join(config.PDF_SALES_ARCHIVE_FOLDER, file)
            shutil.move(file_path, archive_path)

    logger.info("Process completed.")
