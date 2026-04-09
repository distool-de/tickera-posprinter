import logging
from src.logging_config import setup_logging

logger = setup_logging(__name__,logging.DEBUG)

def get_new_orders(wcapi, after, order_state="completed", customer_id=None, known_orders=None):
    """
    Funktion zum Abrufen neuer Bestellungen eines bestimmten Typs von WooCommerce.

    Args:
    - wcapi: Ein bereits initialisierter WooCommerce API-Client.
    - order_state (str): Gibt den Status der Bestellungen an, die zurückgegeben werden sollen. Standard ist 'completed'.
    - customer_id (int, optional): Die ID des Kunden, dessen Bestellungen abgerufen werden sollen. Default ist None.
    - after (str): ISO8601-Datum, um Bestellungen ab einem bestimmten Zeitpunkt abzurufen.
    - known_orders (set, optional): Set von bekannten Bestellungs-IDs, die ausgeschlossen werden sollen. Default ist None.

    Returns:
    - list: Eine Liste der gefundenen Bestellungen.
    """
    params = {"status": order_state, "after": after}
    if customer_id is not None:
        params["customer"] = customer_id

    if known_orders is not None:
        params["exclude"] = ",".join(str(oid) for oid in known_orders)

    try:
        response = wcapi.get("orders", params=params)
        response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war
        return response.json()
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Bestellungen: {e}")
        return []