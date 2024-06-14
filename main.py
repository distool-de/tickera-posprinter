from src.api import get_new_orders
from datetime import datetime, timedelta
from src.tc import fetch_ticket_data, print_ticket, create_session
from src.printing import get_default_printer
from dotenv import load_dotenv
from src.logging_config import setup_logging
import logging, concurrent.futures, os

logger = setup_logging(__name__,logging.DEBUG)
setup_logging("urllib3", logging.DEBUG)
load_dotenv()

def main():
    url = os.getenv('DOMAIN')
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    order_state = os.getenv('ORDER_STATE', 'completed')
    customer_id = os.getenv('CUSTOMER_ID')
    printer = get_default_printer()
    time_threshold = (datetime.now() - timedelta(minutes=1)).isoformat()
    known_order_ids = set()
    session = None

    if not url or not consumer_key or not consumer_secret:
        logger.error("URL, Consumer Key oder Consumer Secret sind nicht gesetzt.")
        return
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        try:
            while True:  # Endlosschleife für kontinuierlichen Betrieb
                if session is None:
                    session = create_session()

                orders = get_new_orders(url, consumer_key, consumer_secret, time_threshold, order_state, customer_id, known_order_ids)
                if orders:
                    for order in orders:
                        order_id = order['id']
                        tc_paid_date = None
                        for meta in order.get('meta_data', []):
                            if meta.get('key') == '_tc_paid_date':
                                tc_paid_date = meta.get('value')
                                break
                        order_tickets = fetch_ticket_data(session, url, order_id, tc_paid_date)
                        future_to_tickets = {executor.submit(print_ticket, session, url, ticket['ticket_id'], tc_paid_date, ticket['hash'], ticket['ticket_template_POS'], printer): ticket for ticket in order_tickets['data']}
                        known_order_ids.add(order_id)
                else:
                    logger.info("Keine neuen Bestellungen gefunden.")

        except Exception as e:
            logger.error(f"Ein Fehler ist aufgetreten: {e}")
        finally:
            if session:
                session.close()
                logger.info("Session wurde geschlossen.")

if __name__ == "__main__":
    main()