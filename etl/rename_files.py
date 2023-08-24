# -*- coding: utf-8 -*-
import os


def run(config, job_name):
    i = 0
    for file in os.listdir(config.EXCEL_FOLDER):
        _, ext = os.path.splitext(file)
        newfilename = None
        if ext in config.EXCEL_EXTENSIONS:
            newfilename = (
                file.replace(" ", "_")
                .replace("-", "_")
                .replace("__", "_")
                .replace("2202", "2022")
            )
        elif ext in config.PDF_EXTENSIONS:
            prefix, sales_date, hour = file.split(" ")
            sales_year, sales_month, sales_day = sales_date.split("-")
            newfilename = f"Fuel_Sales_{sales_year}_{sales_day}_{sales_month}{ext}"

        if newfilename:
            os.rename(
                os.path.join(config.EXCEL_FOLDER, file),
                os.path.join(config.EXCEL_FOLDER, newfilename),
            )
