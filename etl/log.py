# -*- coding: utf-8 -*-
import datetime
import logging
import os


def get_logger(job_name, config):
    # Create logger
    logger = logging.getLogger(job_name)
    logger.setLevel(config.LOG_LEVEL)

    # Ensure the log directory exists
    if not os.path.exists(config.LOG_FOLDER):
        os.makedirs(config.LOG_FOLDER)

    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Define the log file path based on job name, timestamp, and log directory
    log_file_path = os.path.join(config.LOG_FOLDER, f"{job_name}_{timestamp}.log")

    # Define the log format
    log_formatter = logging.Formatter(config.LOG_FORMAT)

    # Create file handler and set its level and format
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(config.LOG_LEVEL)
    file_handler.setFormatter(log_formatter)

    # Add the handler to logger
    logger.addHandler(file_handler)

    return logger


# Example usage:
# class Config:
#     log_directory = '/path/to/log_directory'
#     log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     log_level = logging.DEBUG

# logger = get_logger("sample_job", Config())
# logger.info("This is an info log.")
