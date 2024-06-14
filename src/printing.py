import subprocess
import sys

def get_default_printer():
    # Befehl zur Abfrage des Standarddruckers
    cmd = "wmic printer where default='TRUE' get name"
    # Ausführen des Befehls
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # Ausgabe parsen
    output = result.stdout.strip().split('\n')
    # Entfernen der Kopfzeile und leerer Zeilen
    printer_name = [line.strip() for line in output if line.strip() and line.strip().lower() != 'name']
    # Anzeigen des Standarddrucker-Namens
    if printer_name:
        return(printer_name[0])
    else:
        return()


def pdf_printer(pdf_file, printer_name):
    try:
        if sys.platform.startswith('win'):
            subprocess.run((f'print /d:{printer_name} {pdf_file}'), check=True)
        elif sys.platform.startswith('linux'):
            subprocess.run(['lp', '-d', printer_name, pdf_file], check=True)
        else:
            print("Unsupported operating system")
    except Exception as e:
        print(f"Failed => {e}")