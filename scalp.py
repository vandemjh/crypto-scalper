import os
import datetime
import traceback
from settings import *
from util.util import Util
from binance.enums import *
from dotenv import load_dotenv
from util.colors import Colors
from util.client import Client
from model.strategy import Strategy
from model.exchange import ExchangeInformation

# CONST EVAL
OUTPUT_FILE = (
    OUTPUT_FILE + str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + ".json"
)
SCALP_PERCENT = SCALP_PERCENT / 2


load_dotenv()
api_key = os.getenv("KEY")
api_secret = os.getenv("SECRET")
Client(apiKey=api_key, apiSecret=api_secret, tld="us")
api_key = api_secret = None
ExchangeInformation()
Util.printExchangeInformation()

try:
    print(Colors.info("Press Ctrl+C to stop"))
    totalQuantity = Client.getAssetBalance(ExchangeInformation.quoteAsset) * (
        IN_PLAY_PERCENT / 100
    )
    strategy = Strategy(totalQuantity=totalQuantity)
    strategy.execute()

except Exception as e:
    print(Colors.warn("\nInterrupted!"))
    print(Colors.warn("\nStack trace:"))
    print(e)
    traceback.print_exc()
    Util.cancelAllOrders(SYMBOL)
    Client.stopSocket()