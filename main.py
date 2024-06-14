from src.api import get_new_orders
from datetime import datetime
from src.tc import fetch_ticket_data, print_ticket
from src.printing import get_default_printer
from dotenv import load_dotenv
import os

load_dotenv()

# Beispielaufruf der Funktion
url = os.getenv('DOAMIN')
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
order_state= os.getenv('ORDER_STATE')
customer_id= os.getenv('CUSTOMER_ID')
printer=get_default_printer()
time = datetime.now().isoformat()
try:
    # Get new orders
    orders = get_new_orders(url, consumer_key, consumer_secret, time, order_state, customer_id)
    # Check if orders were retrieved
    if orders:
        for order in orders:
            order_id = order['id']
            tc_paid_date = None
            for meta in order.get('meta_data', []):
                if meta.get('key') == '_tc_paid_date':
                    tc_paid_date = meta.get('value')
                    break
            order_tickets = fetch_ticket_data(url, order_id, tc_paid_date)
            for ticket in order_tickets['data']:
                print_ticket(url, ticket['ticket_id'],tc_paid_date, ticket['hash'], ticket['ticket_template_POS'], printer)
        # Extract and store order IDs
        order_ids = [order['id'] for order in orders]
    else:
        print("No new orders found.")

except Exception as e:
    print(f"An error occurred: {e}")