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
        buyOrder = Order(SYMBOL, SIDE_BUY, buyPrice, buyQuantity)
        buyOrder.place()
        writeOrder(buyOrder.waitForOrder())

        # Place and wait for sell order
        sellPrice = buyPrice - (buyPrice * (SCALP_PERCENT / 100))
        sellQuantity = (client.get_asset_balance(asset=SELL_SYMBOL))["free"]
        sellOrder = Order(SYMBOL, SIDE_SELL, sellPrice, sellQuantity)
        sellOrder.place()
        writeOrder(sellOrder.waitForOrder())
except KeyboardInterrupt:
    print(colors.warn("\nInterrupted!") + " you should probably close open orders:")
    Order.printOpenOrders(SYMBOL)
    pass
