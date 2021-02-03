import sys
import json

from twisted.internet import reactor
from settings import SYMBOL
from util.colors import *
from binance.client import Client as BinanceClient
from binance.websockets import BinanceSocketManager


class Client:
    """
    Encapsulation of binance.Client
    """

    binanceClient: BinanceClient
    socket: BinanceSocketManager

    ticketSocketKey: str = None
    userSocketKey: str = None

    latestPrice: float = None
    latestOrder: dict = None
    accountEvent: dict = None

    @staticmethod
    def init(apiKey: str = "", apiSecret: str = "", tld: str = "com"):
        """
        Sets static client for orders, starts socket
        """
        Client.binanceClient = BinanceClient(api_key=apiKey, api_secret=apiSecret, tld=tld)
        Client.socket = BinanceSocketManager(Client.binanceClient)
        Client.ticketSocketKey = Client.socket.start_trade_socket(
            SYMBOL, Client.processTradeSocket
        )
        Client.latestPrice = Client.getLatestOrderPrice(SYMBOL)
        Client.userSocketKey = Client.socket.start_user_socket(Client.processUserSocket)
        Client.socket.start()

        if Client.ticketSocketKey == False or Client.userSocketKey == False:
            print(Colors.fail("FAILED") + " to open socket connection")
            exit(1)

    @staticmethod
    def processTradeSocket(message: dict, printOut=False) -> None:
        """
        Processes socket message
        """
        if DEBUG or printOut:
            toPrint: str = message["p"]
            for i in range(len(toPrint)):
                sys.stdout.write("\b")
            sys.stdout.write(toPrint)
            sys.stdout.flush()
        Client.latestPrice = float(message["p"])

    @staticmethod
    def processUserSocket(message: dict) -> None:
        """
        Processes user socket event
        """
        print(message)
        Client.accountEvent = json.loads(message)

    @staticmethod
    def getOpenOrders(symbol: str) -> list:
        """
        Returns open orders
        """
        return list(Client.binanceClient.get_open_orders(symbol=symbol))

    @staticmethod
    def getLatestOrderPrice(symbol: str) -> float:
        if Client.latestPrice == None:
            return float(
                Client.binanceClient.get_recent_trades(symbol=symbol, limit=1)[0]["price"]
            )
        return Client.latestPrice

    @staticmethod
    def getLatestOrder(symbol: str) -> dict:
        if Client.latestOrder == None:
            return Client.binanceClient.get_recent_trades(symbol=symbol, limit=1)[0]
        return Client.latestOrder

    @staticmethod
    def getAccountEvent() -> dict:
        return Client.accountEvent

    @staticmethod
    def stopSocket():
        """
        Stops the socket and reactor
        """
        Client.socket.close()
        reactor.stop()

    @staticmethod
    def cancelOrder(symbol: str, orderId: str) -> dict:
        """
        Cancel an order
        """
        return Client.binanceClient.cancel_order(symbol=symbol, orderId=orderId)

    @staticmethod
    def getAssetBalance(asset: str) -> float:
        return float(Client.binanceClient.get_asset_balance(asset=asset)["free"])

    @staticmethod
    def getAveragePrice(asset: str) -> float:
        return float(Client.binanceClient.get_avg_price(symbol=asset)["price"])

    @staticmethod
    def getPriceChangeStatistics(asset: str) -> dict:
        return Client.binanceClient.get_ticker(symbol=asset)["weightedAvgPrice"]

    @staticmethod
    def getExchangeInformation():
        return Client.binanceClient.get_exchange_info()
