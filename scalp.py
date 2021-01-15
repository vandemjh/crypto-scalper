import requests
import os
import json
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
import time
from colors import colors

# Percent of portfolio to trade
IN_PLAY_PERCENT = 1
# Symbol to scalp
SYMBOL = "BTCUSDT"
DEBUG = True
SCALP_PERCENT = 1

# CONST EVAL
IN_PLAY_PERCENT = IN_PLAY_PERCENT / 100
SCALP_PERCENT = SCALP_PERCENT / 100


def writeOrder(order: dict) -> None:
    with open("orders.json", "a") as f:
        f.write(json.dumps(order))


def waitForOrder(buyOrderId: int, buyClientOrderId: str) -> dict:
    # buyOrder = client.get_order(
    #     symbol=SYMBOL,
    #     orderId=buyOrderId,
    #     origClientOrderId=buyClientOrderId,
    # )
    while not buyOrder["status"] == "filled":
        print(colors.INFO + "\tAwaiting order fill..." + colors.END)
        time.sleep(1)
        # buyOrder = client.get_order(
        #     symbol=SYMBOL,
        #     orderId=buyOrderId,
        #     origClientOrderId=buyClientOrderId,
        # )
        buyOrder["status"] = "filled"
        buyOrder["executedQty"] = toBuyQuantity
    return buyOrder

load_dotenv()
api_key = os.getenv("KEY")
api_secret = os.getenv("SECRET")
client = Client(api_key, api_secret, tld="us")
api_key = api_secret = None

USDTBalance = (client.get_asset_balance(asset="USDT"))["free"]
USDTBalance = float(USDTBalance) * IN_PLAY_PERCENT

print("Available balance is: " + str(USDTBalance))

while True:
    averagePrice = float(client.get_avg_price(symbol=SYMBOL)["price"])
    print("Average price is: " + str(averagePrice))
    toBuyQuantity = USDTBalance / averagePrice
    # order = client.order_limit_buy(
    #     symbol=SYMBOL,
    #     quantity=toBuyQuantity,
    #     price='0.00001')
    buyOrder = {
        "orderId": 1,
        "clientOrderId": "abc",
        "price": averagePrice,
        "status": "not-filled",
    }
    buyOrderId = buyOrder["orderId"]
    buyClientOrderId = buyOrder["clientOrderId"]
    print(
        colors.PLACED
        + "PLACED:"
        + colors.BUY
        + " BUY"
        + colors.END
        + (" (test)" if DEBUG else "")
        + ": order PLACED at "
        + str(buyOrder["price"])
        + " totaling "
        + str(toBuyQuantity)
    )
    waitForOrder()

    filledBuyOrderPrice = float(buyOrder["price"])
    filledBuyOrderQuantity = float(buyOrder["executedQty"])
    print(
        colors.FILLED
        + "FILLED: "
        + colors.BUY
        + "BUY"
        + colors.END
        + (" (test)" if DEBUG else "")
        + ": @ "
        + str(filledBuyOrderPrice)
        + " totaling "
        + str(filledBuyOrderQuantity)
    )
    writeOrder(buyOrder)

    sellPrice = filledBuyOrderPrice * SCALP_PERCENT
    print(
        colors.BOLD
        + "Sell limit: "
        + colors.END
        + str(SCALP_PERCENT * 100)
        + "% higher at "
        + str(sellPrice)
    )
    print(
        colors.PLACED
        + "PLACED "
        + colors.SELL
        + "SELL "
        + colors.END
        + "LIMIT"
        + (" (test)" if DEBUG else "")
        + ": order at "
        + str(sellPrice)
        # + " totaling "
        # + str(toBuy)
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
