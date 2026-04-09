# Tickera-POSPrinter

Automatischer Ticketdruck für WooCommerce/Tickera-Shops. Das Skript überwacht kontinuierlich eingehende Bestellungen und druckt neue Tickera-Tickets sofort auf einem angeschlossenen POS-Drucker.

## Funktionsweise

1. Das Skript fragt regelmäßig die WooCommerce-REST-API nach neuen Bestellungen mit dem konfigurierten Status ab.
2. Für jede neue Bestellung werden die zugehörigen Tickera-Ticket-PDFs heruntergeladen.
3. Die PDFs werden über Ghostscript an den Standarddrucker des Systems gesendet.
4. Bereits verarbeitete Bestellungen werden im Arbeitsspeicher gemerkt und nicht erneut gedruckt.

## Voraussetzungen

- **Python 3**
- **Ghostscript** installiert und im PATH verfügbar
  - Linux/macOS: `gs`
  - Windows: `gswin64c`
- Ein konfigurierter **Standarddrucker** auf dem System (CUPS unter Linux/macOS, Windows-Druckerdienst)
- Ein WooCommerce-Shop mit installiertem **Tickera-Plugin**
- WooCommerce REST API Zugangsdaten (Consumer Key + Secret)

## Installation

```bash
make install
```

Oder manuell:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Konfiguration

Eine `.env`-Datei im Projektverzeichnis anlegen:

```env
DOMAIN='https://example.de'
CONSUMER_KEY='ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
CONSUMER_SECRET='cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
ORDER_STATE='completed'
CUSTOMER_ID='123'
LOG_FILE=script.log
```

| Variable          | Pflicht | Standard      | Beschreibung                                          |
|-------------------|---------|---------------|-------------------------------------------------------|
| `DOMAIN`          | Ja      | —             | URL des WooCommerce-Shops (z. B. `https://example.de`) |
| `CONSUMER_KEY`    | Ja      | —             | WooCommerce REST API Consumer Key                     |
| `CONSUMER_SECRET` | Ja      | —             | WooCommerce REST API Consumer Secret                  |
| `ORDER_STATE`     | Nein    | `completed`   | Bestellstatus, nach dem gefiltert wird                |
| `CUSTOMER_ID`     | Nein    | —             | Optional: nur Bestellungen eines bestimmten Kunden    |
| `LOG_FILE`        | Nein    | `app.log`     | Pfad zur Log-Datei                                    |

## Starten

```bash
make run
```

Oder alles in einem Schritt (venv erstellen, Abhängigkeiten installieren, starten):

```bash
make all
```

Das Skript läuft als Dauerprozess und muss manuell beendet werden (`Ctrl+C`).

## Aufräumen

```bash
make clean
```

Entfernt die virtuelle Umgebung und die Log-Datei.

## Plattformen

Unterstützt werden Linux, macOS und Windows.
