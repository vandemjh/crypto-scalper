import os
import json
import threading
import time
from binance.client import Client as BinanceClient
from dotenv import load_dotenv
from binance.enums import *
from util.client import Client

load_dotenv()
api_key = os.getenv("KEY")
api_secret = os.getenv("SECRET")
Client.init(api_key, api_secret, tld="us")
api_key = api_secret = None

ORDER_HISTORY = []
OUTPUT_FILE = "out.json"

def writeToFile() -> None:
    with open(OUTPUT_FILE, "w+") as f:
        f.write(json.dumps(ORDER_HISTORY))


count = 0
while True:
    count = count + 1
    time.sleep(1)
    ORDER_HISTORY.append(Client.latestPrice)
    if count > 600:
        threading.Thread(target=writeToFile).start()
        count = 0