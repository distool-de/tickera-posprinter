# logging_config.py
import logging
import os

def setup_logging(log_level=logging.INFO):
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=log_level, format=log_format)
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Optional: Log to a file with DEBUG level
    log_file = os.getenv("LOG_FILE", "app.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    return logger