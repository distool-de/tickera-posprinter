from src.api import get_new_orders
from datetime import datetime
from src.tc import fetch_ticket_data, print_ticket
from src.printing import get_default_printer
import concurrent.futures

# Beispielaufruf der Funktion
url = 'https://oldenburgknights.de/'
consumer_key = 'ck_b5b023efc187bad52505b0225d05d44efbf6548e'
consumer_secret = 'cs_fa79e80a42d9aac24a5e7eb76206bcb5eee5823d'
order_state='completed'
customer_id='447'
printer = get_default_printer()
time = datetime.now().isoformat()

# Speicher für bekannte Order-IDs
known_order_ids = set()

def process_order(order):
    order_id = order['id']
    if order_id in known_order_ids:
        print(f"Order ID {order_id} is already known.")
        return
    known_order_ids.add(order_id)

    tc_paid_date = None
    for meta in order.get('meta_data', []):
        if meta.get('key') == '_tc_paid_date':
            tc_paid_date = meta.get('value')
            break

    order_tickets = fetch_ticket_data(url, order_id, tc_paid_date)
    for ticket in order_tickets['data']:
        print_ticket(url, ticket['ticket_id'], tc_paid_date, ticket['hash'], ticket['ticket_template_POS'], printer)

try:
    # Get new orders
    orders = get_new_orders(url, consumer_key, consumer_secret, time, order_state)
    
    # Check if orders were retrieved
    if orders:
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_order, orders)
    else:
        print("No new orders found.")

except Exception as e:
    print(f"An error occurred: {e}")
