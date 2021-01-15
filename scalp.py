import requests
import os
import json
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
import time

# Percent of portfolio to trade
IN_PLAY_PERCENT = 1
# Symbol to scalp
SYMBOL = "BTCUSDT"
DEBUG = True
SCALP_PERCENT = 1


def writeOrder(order: dict) -> None:
    with open("orders.json", "a") as f:
        f.write(json.dumps(order))


load_dotenv()
api_key = os.getenv("KEY")
api_secret = os.getenv("SECRET")
client = Client(api_key, api_secret, tld="us")
api_key = api_secret = ""

USDTBalance = (client.get_asset_balance(asset="USDT"))["free"]
USDTBalance = float(USDTBalance) * (IN_PLAY_PERCENT / 100)

print("Available balance is: " + str(USDTBalance))

while True:
    averagePrice = float(client.get_avg_price(symbol=SYMBOL)["price"])
    print("Average price is: " + str(averagePrice))
    toBuy = averagePrice / USDTBalance
    # order = client.order_limit_buy(
    #     symbol='BNBBTC',
    #     quantity=100,
    #     price='0.00001')
    buyOrder = {"orderId": 1, "clientOrderId": "abc"}
    buyOrderId = buyOrder["orderId"]
    buyClientOrderId = buyOrder["clientOrderId"]
    while not buyOrder["status"] == "filled":
        print("\tAwaiting order fill")
        time.sleep(1)
        # buyOrder = client.get_order(
        #     symbol=SYMBOL,
        #     orderId=buyOrderId,
        #     origClientOrderId=buyClientOrderId,
        # )
        buyOrder["status"] = "filled"
    print(
        "BUY"
        + (" (test)" if DEBUG else "")
        + ": order at "
        + str(buyOrder["price"])
        + " totaling "
        + str(toBuy)
    )
    writeOrder(buyOrder)

    sellLimit = price * (100 / SCALP_PERCENT)
    print("Sell limit is " + str(SCALP_PERCENT) + "% higher at " + str(sellLimit))
    print(
        "SELL LIMIT"
        + (" (test)" if DEBUG else "")
        + ": order at "
        + str(price)
        + " totaling "
        + str(toBuy)
    )
    # order = client.get_order(
    #     symbol=SYMBOL,
    #     orderId=order["orderId"],
    #     origClientOrderId=order["clientOrderId"],
    # )
    while not order["status"] == "filled":
        order = client.get_order(
            symbol=SYMBOL,
            orderId=order["orderId"],
            origClientOrderId=order["clientOrderId"],
        )
        time.sleep(1)


# order = client.order_limit_buy(symbol=SYMBOL, quantity=100, price="0.00001")
# order = client.order_limit_sell(symbol=SYMBOL, quantity=100, price="0.00001")
