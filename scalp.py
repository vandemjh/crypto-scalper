import os
import json
import time
import asyncio
import datetime
import traceback
from util.util import Util
from trade import Trade
from settings import *
from order import Order
from binance.enums import *
from dotenv import load_dotenv
from util.colors import colors
from util.client import Client

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
exchangeInfo = Client.getExchangeInformation()
symbols = exchangeInfo["symbols"]

baseAsset: str = None
baseAssetPrecision: int = None
quoteAsset: str = None
quoteAssetPrecision: int = None
filters: list = []
minPrice: float = 0
maxPrice: float = 0
tickSize: float = 0
stepSize: float = 0
for symbol in symbols:
    if symbol["symbol"] == SYMBOL:
        baseAsset = symbol["baseAsset"]
        baseAssetPrecision = symbol["baseAssetPrecision"]
        quoteAsset = symbol["quoteAsset"]
        quoteAssetPrecision = symbol["quotePrecision"]
        filters = symbol["filters"]

for filter in filters:
    if filter["filterType"] == "PRICE_FILTER":
        minPrice = float(filter["minPrice"])
        maxPrice = float(filter["maxPrice"])
        tickSize = float(filter["tickSize"])
    if filter["filterType"] == "LOT_SIZE":
        stepSize = float(filter["stepSize"])

balance: float = Client.getAssetBalance("USDT")
balance = float(balance) * (IN_PLAY_PERCENT / 100)

print(colors.info("Available balance is: " + str(balance)))
print(colors.info("Scalping: " + str(SCALP_PERCENT) + "%"))

print(
    colors.warn("Exchange information")
    + colors.info("\n\tBase asset: ")
    + colors.BUY
    + baseAsset
    + colors.END
    + colors.info("\n\tBase asset precision: ")
    + str(baseAssetPrecision)
    + colors.info("\n\tQuote asset: ")
    + colors.SELL
    + quoteAsset
    + colors.END
    + colors.info("\n\tQuote asset precision: ")
    + str(quoteAssetPrecision)
    + colors.info("\n\tMinimum price: ")
    + str(minPrice)
    + colors.info("\n\tMaximum price: ")
    + str(maxPrice)
    + colors.info("\n\tTick size: ")
    + str(tickSize)
    + colors.info("\n\tStep size: ")
    + str(stepSize)
)


try:
    print(colors.info("Press Ctrl+C to stop"))

except Exception as e:
    print(colors.warn("\nInterrupted!"))
    Util.cancelAllOrders(SYMBOL)

    print(colors.warn("\nStack trace:"))
    print(e)
    traceback.print_exc()
    pass
finally:
    Client.stopSocket()