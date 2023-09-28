# -*- coding: utf-8 -*-
import os


def rename(config, folder):
    for file in os.listdir(folder):
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
            try:
                prefix, sales_date, hour = file.split(" ")
                sales_year, sales_month, sales_day = sales_date.split("-")
                newfilename = f"{prefix}_{sales_year}_{sales_day}_{sales_month}{ext}"
            except:
                newfilename = None

        if newfilename:
            os.rename(
                os.path.join(folder, file),
                os.path.join(folder, newfilename),
            )


def run(config, job_name):
    rename(config, config.PDF_SALES_FOLDER)
    rename(config, config.PDF_FUEL_FOLDER)
