import logging

def setup_logger():
    # Setting up logging format
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    
    # Setting up logging level
    logging.basicConfig(level=logging.INFO, format=log_format)

    # Logging to a file
    file_handler = logging.FileHandler("image_validation.log")
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)
