# -*- coding: utf-8 -*-
import os


def run(config, job_name):
    i = 0
    for file in os.listdir(config.EXCEL_FOLDER):
        _, ext = os.path.splitext(file)
        if ext in config.EXCEL_EXTENSIONS:
            newfilename = (
                file.replace(" ", "_")
                .replace("-", "_")
                .replace("__", "_")
                .replace("2202", "2022")
            )
            os.rename(
                os.path.join(config.EXCEL_FOLDER, file),
                os.path.join(config.EXCEL_FOLDER, newfilename),
            )
