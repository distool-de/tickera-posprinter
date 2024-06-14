import logging, os

def setup_logging(log_name,log_level=logging.INFO):
    log_format = "%(asctime)s - %(threadName)s - %(processName)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=log_level, format=log_format)
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    # Optional: Log to a file
    log_file = os.getenv("LOG_FILE", "app.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    return logger