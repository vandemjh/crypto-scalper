import os
import json
import time
import asyncio
import datetime
import traceback
from settings import *
from trade import Trade
from util.util import Util
from binance.enums import *
from dotenv import load_dotenv
from util.colors import Colors
from util.client import Client
from model.exchange import ExchangeInformation

# CONST EVAL
OUTPUT_FILE = (
    OUTPUT_FILE + str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + ".json"
)

ORDER_HISTORY = []


def init() -> None:
    load_dotenv()
    api_key = os.getenv("KEY")
    api_secret = os.getenv("SECRET")
    Client.init(apiKey=api_key, apiSecret=api_secret, tld="us")
    api_key = api_secret = None


init()
ExchangeInformation().init()
Util.printExchangeInformation()

try:
    print(Colors.info("Press Ctrl+C to stop"))

except Exception as e:
    print(Colors.warn("\nInterrupted!"))
    Util.cancelAllOrders(SYMBOL)

    print(Colors.warn("\nStack trace:"))
    print(e)
    traceback.print_exc()
    pass
finally:
    Client.stopSocket()