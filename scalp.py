import requests
import os
import json
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
import time
from colors import colors
from order import Order
from settings import *
import datetime

# CONST EVAL
OUTPUT_FILE = (
    OUTPUT_FILE + str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + ".json"
)

ORDER_HISTORY = []

load_dotenv()
api_key = os.getenv("KEY")
api_secret = os.getenv("SECRET")
client = Client(api_key, api_secret, tld="us")
api_key = api_secret = None
Order.setClient(client)

balance = (client.get_asset_balance(asset="USDT"))["free"]
balance = float(balance) * (IN_PLAY_PERCENT / 100)

print(colors.info("Available balance is: " + str(balance)))
print(colors.info("Scalping: " + str(SCALP_PERCENT) + "%"))
exchangeInfo = client.get_exchange_info()
symbols = exchangeInfo["symbols"]

baseAsset: str = None
baseAssetPrecision: int = None
quoteAsset: str = None
quotePrecision: int = None
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
        quotePrecision = symbol["quotePrecision"]
        filters = symbol["filters"]

for filter in filters:
    if filter["filterType"] == "PRICE_FILTER":
        minPrice = float(filter["minPrice"])
        maxPrice = float(filter["maxPrice"])
        tickSize = float(filter["tickSize"])
    if filter["filterType"] == "LOT_SIZE":
        stepSize = float(filter["stepSize"])

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
    + str(quotePrecision)
    + colors.info("\n\tMinimum price: ")
    + str(minPrice)
    + colors.info("\n\tMaximum price: ")
    + str(maxPrice)
    + colors.info("\n\tTick size: ")
    + str(tickSize)
    + colors.info("\n\tStep size: ")
    + str(stepSize)
)


def writeOrder(order: dict) -> None:
    ORDER_HISTORY.append(order)
    with open(OUTPUT_FILE, "w+") as f:
        f.write(json.dumps(ORDER_HISTORY))


try:
    print(colors.info("Press Ctrl+C to stop"))
    while True:
        latestTradePrice = Order.getLatestOrderPrice()
        buyPrice = latestTradePrice - (latestTradePrice * (SCALP_PERCENT / 100))
        buyQuantity = balance / buyPrice

        # Place and wait for buy order
        buyOrder = Order(
            symbol=SYMBOL,
            side=SIDE_BUY,
            price=buyPrice,
            quantity=buyQuantity,
            basePrecision=baseAssetPrecision,
            quotePrecision=quotePrecision,
            tickSize=tickSize,
            stepSize=stepSize,
        )
        buyOrder.place()
        writeOrder(buyOrder.waitForOrder())

        # Place and wait for sell order
        sellPrice = buyPrice - (buyPrice * (SCALP_PERCENT / 100))
        sellQuantity = (client.get_asset_balance(asset=baseAsset))["free"]
        sellOrder = Order(
            symbol=SYMBOL,
            side=SIDE_SELL,
            price=sellPrice,
            quantity=sellQuantity,
            basePrecision=quotePrecision,
            quotePrecision=quotePrecision,
            tickSize=tickSize,
            stepSize=stepSize,
        )
        sellOrder.place()
        writeOrder(sellOrder.waitForOrder())
        time.sleep(10)  # Avoid placing buy order right after
except KeyboardInterrupt:
    print(colors.warn("\nInterrupted!") + " canceling open orders:")
    Order.stopSocket()

    for order in Order.getOpenOrders(SYMBOL):
        print(order["orderId"])
        Order.cancelOrder(order["symbol"], order["orderId"])
    pass
