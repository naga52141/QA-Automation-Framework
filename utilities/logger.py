import logging
import os


def get_logger():

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    os.makedirs("logs", exist_ok=True)

    file_handler = logging.FileHandler(
        "logs/automation.log"
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(
        formatter
    )

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger