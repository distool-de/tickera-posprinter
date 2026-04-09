import requests, tempfile, os, logging, time
from src.printing import pdf_printer
from src.logging_config import setup_logging

logger = setup_logging(__name__,logging.DEBUG)

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

def print_ticket(url, ticket_id, order_key, nonce, template_id, printer_name):
    params = {
        "download_ticket": ticket_id,
        "order_key": order_key,
        "nonce": nonce,
        "template_id": template_id
    }

    response = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fp:
            fp.write(response.content)
            logger.info(f'Ticket {ticket_id} downloaded successfully to {fp.name}')
            fp.close()
            pdf_printer(fp.name, printer_name)
            time.sleep(2)
            os.unlink(fp.name)
    else:
        logger.error(f'Failed to download Ticket {ticket_id}')