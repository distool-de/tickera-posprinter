# src/api.py
import logging
from woocommerce import API

logger = logging.getLogger(__name__)

def get_new_orders(url, consumer_key, consumer_secret, after, order_state="completed", customer_id=None, known_orders=None):
    """
    Funktion zum Abrufen neuer Bestellungen eines bestimmten Typs von WooCommerce.
    
    Args:
    - url (str): Die URL zur WooCommerce API.
    - consumer_key (str): Der Consumer Key für den API-Zugriff.
    - consumer_secret (str): Der Consumer Secret für den API-Zugriff.
    - order_state (str): Gibt den Status der Bestellungen an, die zurückgegeben werden sollen. Standard ist 'completed'.
    - customer_id (int, optional): Die ID des Kunden, dessen Bestellungen abgerufen werden sollen. Default ist None.
    - after (str): ISO8601-Datum, um Bestellungen ab einem bestimmten Zeitpunkt abzurufen.
    - known_orders (set, optional): Set von bekannten Bestellungs-IDs, die ausgeschlossen werden sollen. Default ist None.
    
    Returns:
    - list: Eine Liste der gefundenen Bestellungen.
    """
    wcapi = API(
        url=url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3",
        wp_api=True,
        order='asc',
    )

    params = {"status": order_state, "after": after}
    params = {"status": order_state}
    if customer_id is not None:
        params["customer"] = customer_id

    if known_orders is not None:
        params["exclude"] = list(known_orders)

    try:
        response = wcapi.get("orders", params=params)
        response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war
        return response.json()
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Bestellungen: {e}")
        return []