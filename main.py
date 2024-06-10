from src.api import get_new_orders
from datetime import datetime
from src.tc import getTickets

# Beispielaufruf der Funktion
url = ''
consumer_key = ''
consumer_secret = ''
order_state='completed'
customer_id='123'
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
            getTickets(url, order_id, tc_paid_date)
        # Extract and store order IDs
        order_ids = [order['id'] for order in orders]
        print("Order IDs:", order_ids)
    else:
        print("No new orders found.")

except Exception as e:
    print(f"An error occurred: {e}")