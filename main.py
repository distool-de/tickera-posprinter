# main.py
from src.logging_config import setup_logging
from src.api import get_new_orders
from datetime import datetime, timedelta
from src.tc import fetch_ticket_data, print_ticket, create_session
from src.printing import get_default_printer
from dotenv import load_dotenv
import os
import logging

logger = setup_logging(logging.DEBUG)
logger.name = (__name__)
load_dotenv()

def main():
    url = os.getenv('DOMAIN')
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    order_state = os.getenv('ORDER_STATE', 'completed')
    customer_id = os.getenv('CUSTOMER_ID')
    printer = get_default_printer()
    time = (datetime.now() - timedelta(minutes=1)).isoformat()
    known_order_ids = set()

    if not url or not consumer_key or not consumer_secret:
        logger.error("URL, Consumer Key oder Consumer Secret sind nicht gesetzt.")
        return

    try:
        # Create a session
        session = create_session()
        orders = get_new_orders(url, consumer_key, consumer_secret, time, order_state, customer_id, known_order_ids)
        if orders:
            for order in orders:
                order_id = order['id']
                tc_paid_date = None
                for meta in order.get('meta_data', []):
                    if meta.get('key') == '_tc_paid_date':
                        tc_paid_date = meta.get('value')
                        break
                order_tickets = fetch_ticket_data(session, url, order_id, tc_paid_date)
                for ticket in order_tickets['data']:
                    print_ticket(session, url, ticket['ticket_id'], tc_paid_date, ticket['hash'], ticket['ticket_template_POS'], printer)
                known_order_ids.add(order_id)
        else:
            logger.info("Keine neuen Bestellungen gefunden.")
        session.close()
    except Exception as e:
        logger.error(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()