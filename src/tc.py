from requests import request

def getTickets (url, order_id, order_key):
    tcUrl = f"{url}?order_id={order_id}&order_key={order_key}"
    print(tcUrl)
    return