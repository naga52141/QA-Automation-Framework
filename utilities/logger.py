import logging
import os


LOG_FILE = os.path.abspath("logs/automation.log")


def get_logger():

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    has_file_handler = any(
        isinstance(handler, logging.FileHandler)
        and handler.baseFilename == LOG_FILE
        for handler in logger.handlers
    )

    if not has_file_handler:
        os.makedirs("logs", exist_ok=True)

        file_handler = logging.FileHandler(LOG_FILE)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger