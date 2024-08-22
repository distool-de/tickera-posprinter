import subprocess, sys, logging
from src.logging_config import setup_logging

logger = setup_logging(__name__,logging.DEBUG)

def get_default_printer():
    try:
        if sys.platform.startswith('win'):
            logger.debug(f"get Windows default Printer")
            cmd = "wmic printer where default='TRUE' get name"
            logger.debug(f"Executing command to get default printer: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            logger.debug(f"Command output: {result.stdout}")
            output = result.stdout.strip().split('\n')
            printer_name = [line.strip() for line in output if line.strip() and line.strip().lower() != 'name']
            logger.info(f"Default printer found: {printer_name[0]}")
            return printer_name[0]
        
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            logger.debug(f"get Linux default Printer")
            result = subprocess.run(['lpstat', '-d'], capture_output=True, text=True)
            output = result.stdout.strip()
            logger.debug(f"Command output: {output}")
            printer_name = output.split(': ')[1]
            logger.info(f"Default printer found: {printer_name}")
            return printer_name
        else:
            logger.error("Unsupported operating system")

        if not printer_name:
            logger.warning("No default printer found.")
            return None
    except subprocess.SubprocessError as e:
        logger.error(f"Failed to get default printer: {e}")
        return None

# https://github.com/postboxat18/Printer/blob/master/main.py
def pdf_printer(pdf_file, printer_name):
    logger.debug(f"Printing PDF: {pdf_file} on printer: {printer_name}")
    try:
            if sys.platform.startswith('win'):
                subprocess.run(['print', '/D:', printer_name, pdf_file], check=True)
                logger.info(f"Printed {pdf_file} on {printer_name} successfully.")
            elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
                subprocess.run(['lp', '-d', printer_name, pdf_file], check=True)
                logger.info(f"Printed {pdf_file} on {printer_name} successfully.")
            else:
                logger.error("Unsupported operating system")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
