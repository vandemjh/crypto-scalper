import requests
import os
import json
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
import time
from colors import colors
from order import order
from settings import *
import datetime

# CONST EVAL
IN_PLAY_PERCENT = IN_PLAY_PERCENT / 100
SCALP_PERCENT = SCALP_PERCENT / 100
OUTPUT_FILE = OUTPUT_FILE + str(datetime.datetime.now()) + ".json"

ORDERHISTORY = []


def writeOrder(order: dict) -> None:
    ORDERHISTORY.append(order)
    with open(OUTPUT_FILE, "a+") as f:
        f.write(json.dumps(ORDERHISTORY))


load_dotenv()
api_key = os.getenv("KEY")
api_secret = os.getenv("SECRET")
client = Client(api_key, api_secret, tld="us")
api_key = api_secret = None

USDTBalance = (client.get_asset_balance(asset="USDT"))["free"]
USDTBalance = float(USDTBalance) * IN_PLAY_PERCENT

print(colors.info("Available balance is: " + str(USDTBalance)))

while True:
    averagePrice = float(client.get_avg_price(symbol=SYMBOL)["price"])
    print("Average price is: " + str(averagePrice))
    toBuyQuantity = USDTBalance / averagePrice

    buyOrder = order(SYMBOL, client, SIDE_BUY, averagePrice, toBuyQuantity)
    # {
    #     "orderId": 1,
    #     "clientOrderId": "abc",
    #     "price": averagePrice,
    #     "status": "not-filled",
    # }
    buyOrder.place()

    writeOrder(buyOrder.waitForOrder())

    sellPrice = buyOrder.price * SCALP_PERCENT
    print(
        colors.BOLD
        + "Sell limit: "
        + colors.END
        + str(SCALP_PERCENT * 100)
        + "% higher at "
        + str(sellPrice)
    )


# order = client.order_limit_buy(symbol=SYMBOL, quantity=100, price="0.00001")
# order = client.order_limit_sell(symbol=SYMBOL, quantity=100, price="0.00001")
