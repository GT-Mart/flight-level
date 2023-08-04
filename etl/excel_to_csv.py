# -*- coding: utf-8 -*-
import openpyxl
import os
import csv
import shutil


def saveas(file_path, output_csv_path, archive_path, sheet_name=None, columns=None):
    # Open the Excel workbook
    wb = openpyxl.load_workbook(
        file_path, data_only=True
    )  # data_only=True to get values instead of formulas

    if sheet_name:
        sheet = wb[sheet_name]
    else:
        sheet = wb.active

    with open(output_csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file, quotechar='"', quoting=csv.QUOTE_ALL)

        # Write rows from the Excel sheet to the CSV file
        include_rows = False
        rows_added = False
        for row in sheet.iter_rows():
            if row[0].value == "PLU No.":
                include_rows = True

            if include_rows:
                rows_added = True
                writer.writerow([f"{cell.value}" for cell in row])

        if not include_rows:
            writer.writerow(columns)
            for row in sheet.iter_rows():
                writer.writerow([f"{cell.value}" for cell in row[1:]])
                rows_added = True

        if rows_added:
            shutil.move(file_path, archive_path)


def run(config, job_name):
    i = 0
    for file in os.listdir(config.EXCEL_FOLDER):
        filename, ext = os.path.splitext(file)
        if ext in config.EXCEL_EXTENSIONS:
            print(file)
            saveas(
                os.path.join(config.EXCEL_FOLDER, file),
                os.path.join(config.EXCEL_FOLDER, filename + ".csv"),
                os.path.join(config.EXCEL_ARCHIVE_FOLDER, file),
                columns=config.EXCEL_COLUMNS,
            )
