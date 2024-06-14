from woocommerce import API

def get_new_orders(url, consumer_key, consumer_secret, after ,order_state="completed", customer_id=None):
    """
    Funktion zum Abrufen neuer Bestellungen eines bestimmten Typs von WooCommerce.
    
    Args:
    - url (str): Die URL zur WooCommerce API.
    - consumer_key (str): Der Consumer Key für den API-Zugriff.
    - consumer_secret (str): Der Consumer Secret für den API-Zugriff.
    - order_state (str): Gibt den Status der Bestellungen an, die zurückgegeben werden sollen. Standard ist 'completed'.
    - customer_id (int, optional): Die ID des Kunden, dessen Bestellungen abgerufen werden sollen. Default ist None.
    - after (str, optional): ISO8601-Datum, um Bestellungen ab einem bestimmten Zeitpunkt abzurufen. Default ist None, wird auf aktuelle Zeit gesetzt.
    
    
    Returns:
    - list: Eine Liste der gefundenen Bestellungen.
    """
    # Parameter für die Anfrage
    wcapi = API(
        url=url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3",
        wp_api=True,
    )

    # Erstellen der Parameter-Diktion für die Anfrage
    params = {"status": order_state}
    if customer_id is not None:
        params["customer"] = customer_id
    #params["after"] = after

    # Testanfrage, um sicherzustellen, dass die URL funktioniert
    try:
        response = wcapi.get("orders", params=params)
        response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war
        orders = response.json()
        return orders
    except Exception as e:
        print(f"Fehler beim Abrufen der Bestellungen: {e}")
        return []
