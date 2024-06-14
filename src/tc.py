import requests, tempfile, os
from src.printing import pdf_printer

def fetch_ticket_data(url, order_id, order_key):
    params = {
        "order_id": order_id,
        "order_key": order_key
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        return {"status": "401", "message": "Unauthorized access."}
    else:
        return {"status": str(response.status_code), "message": "Request failed."}


def print_ticket(url, ticket_id, order_key, hash, template_id, printer_name):
    params = {
        "download_ticket": ticket_id,
        "order_key": order_key,
        "nonce":hash,
        "template_id":template_id
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
    # Open a local file in binary write mode
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fp:
            fp.write(response.content)
            pdf_printer(fp.name, printer_name)
            print(f'Ticket {ticket_id} downloaded successfully to {fp.name}')
            fp.close()
            os.unlink(fp.name)
    else:
        print(f'Failed to download Ticket {ticket_id}')
        