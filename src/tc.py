# tc.py
import requests
import tempfile
import os
from src.printing import pdf_printer

def create_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0"
    })
    return session

def fetch_ticket_data(session, url, order_id, order_key):
    params = {
        "order_id": order_id,
        "order_key": order_key
    }

    response = session.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        return {"status": "401", "message": "Unauthorized access."}
    else:
        return {"status": str(response.status_code), "message": "Request failed."}

def print_ticket(session, url, ticket_id, order_key, hash, template_id, printer_name):
    params = {
        "download_ticket": ticket_id,
        "order_key": order_key,
        "nonce": hash,
        "template_id": template_id
    }

    response = session.get(url, params=params)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fp:
            fp.write(response.content)
            pdf_printer(fp.name, printer_name)
            print(f'Ticket {ticket_id} downloaded successfully to {fp.name}')
            fp.close()
            os.unlink(fp.name)
    else:
        print(f'Failed to download Ticket {ticket_id}')
        

        