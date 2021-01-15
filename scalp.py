import requests
import os
import json
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *

# Percent of portfolio to trade
IN_PLAY_PERCENT = 1
# Symbol to scalp
SYMBOL = "BTCUSDT"


load_dotenv()
api_key = os.getenv("KEY")
api_secret = os.getenv("SECRET")
client = Client(api_key, api_secret, tld="us")
api_key = api_secret = ""

USDTBalance = (client.get_asset_balance(asset="USDT"))["free"]
USDTBalance = float(USDTBalance) * (IN_PLAY_PERCENT / 100)

# avg_price = client.get_avg_price(symbol=SYMBOL)

# print(avg_price)


# order = client.order_limit_buy(symbol=SYMBOL, quantity=100, price="0.00001")
# order = client.order_limit_sell(symbol=SYMBOL, quantity=100, price="0.00001")
