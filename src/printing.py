import subprocess, sys, logging, time
from src.logging_config import setup_logging

logger = setup_logging(__name__,logging.DEBUG)

def get_default_printer():
    # Befehl zur Abfrage des Standarddruckers
    cmd = "wmic printer where default='TRUE' get name"
    logger.debug(f"Executing command to get default printer: {cmd}")

    try:
        # Ausführen des Befehls
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        logger.debug(f"Command output: {result.stdout}")

        # Ausgabe parsen
        output = result.stdout.strip().split('\n')
        # Entfernen der Kopfzeile und leerer Zeilen
        printer_name = [line.strip() for line in output if line.strip() and line.strip().lower() != 'name']

        # Anzeigen des Standarddrucker-Namens
        if printer_name:
            logger.info(f"Default printer found: {printer_name[0]}")
            return printer_name[0]
        else:
            logger.warning("No default printer found.")
            return None
    except subprocess.SubprocessError as e:
        logger.error(f"Failed to get default printer: {e}")
        return None

def pdf_printer(pdf_file, printer_name):
    logger.debug(f"Printing PDF: {pdf_file} on printer: {printer_name}")

    try:
        if sys.platform.startswith('win'):
            cmd = f'print /d:{printer_name} {pdf_file}'
            subprocess.run(cmd, check=True)
            logger.info(f"Printed {pdf_file} on {printer_name} successfully.")
        elif sys.platform.startswith('linux'):
            cmd = ['lp', '-d', printer_name, pdf_file]
            subprocess.run(cmd, check=True)
            logger.info(f"Printed {pdf_file} on {printer_name} successfully.")
        else:
            logger.error("Unsupported operating system")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to print {pdf_file} on {printer_name}: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")