# Makefile für Python-Projekt


# Pfade zu den Dateien
REQUIREMENTS_FILE = requirements.txt
MAIN_SCRIPT = main.py

# Ziel für die virtuelle Umgebung
venv:
	python3 -m venv venv

# Ziel für die Installation der Abhängigkeiten
install: venv
	venv/bin/pip install -r $(REQUIREMENTS_FILE)

# Ziel für das Starten des Skripts
run: venv install
	venv/bin/python $(MAIN_SCRIPT)

# Ziel für das Entfernen der virtuellen Umgebung
clean:
	rm -rf venv
	rm -rf log/script.log

# Standardziel, das alle Schritte nacheinander ausführt
.PHONY: all
all: venv install run

# Hilfsziel zum Testen der Installation
test_install: venv
	venv/bin/pip install -r $(REQUIREMENTS_FILE)
	@echo "Installation erfolgreich"

# Hilfsziel zum Testen der Ausführung
test_run: install
	venv/bin/python $(MAIN_SCRIPT)
	@echo "Ausführung erfolgreich"