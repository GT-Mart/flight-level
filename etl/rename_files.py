# -*- coding: utf-8 -*-
import os


def rename(config, folder):
    for file in os.listdir(folder):
        fname, ext = os.path.splitext(file)
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
                if len(fname.split("_")) == 2:
                    prefix, sales_date = fname.split("_")
                    sales_month, sales_day, sales_year = sales_date.split(" ")
                    sales_month = config.MONTH_MAP[sales_month]
                    newfilename = (
                        f"{prefix}_{sales_year}_{sales_day}_{sales_month}{ext}"
                    )
                else:
                    print(f"file {file} does not follow the expected naming standard.")
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
