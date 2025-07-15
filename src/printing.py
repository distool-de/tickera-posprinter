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

def pdf_printer(pdf_file, printer_name):
    if not os.path.isfile(pdf_file):
        logger.error(f"Datei nicht gefunden: {pdf_path}")
        retrun
        
    system = sys.platform

    if system == "win32":
        gs_command = [
            "gswin64c",
            "-dBATCH",
            "-dNOPAUSE",
            "-dNOSAFER",
            "-sDEVICE=mswinpr2",
            f"-sOutputFile=%printer%{printer_name}",
            pdf_file
        ]
    else:
        gs_command = [
            "gs",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=cups",
            f"-sOutputFile=%printer%{printer_name}",
            pdf_file
        ]
    
    try:
        logger.info(f"Start Printing PDF: {pdf_file} on printer: {printer_name}")
        subprocess.run(gs_command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Fehler beim Drucken der Datei:", e)
    except FileNotFoundError:
        logger.error("Ghostscript nicht gefunden. Stelle sicher, dass es installiert ist und im PATH liegt.")
