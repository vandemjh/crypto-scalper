import sys

from twisted.internet import reactor
from settings import SYMBOL
import colors
from binance.client import Client
from binance.websockets import BinanceSocketManager


class Client:
    """
    Encapsulation of binance.Client
    """

    client: Client
    socket: BinanceSocketManager

    ticketSocketKey: str = None
    userSocketKey: str = None

    latestPrice: float = None
    latestOrder: dict = None
    accountEvent: dict = None

    @staticmethod
    def setClient(client: Client):
        """
        Sets static client for orders, starts socket
        """
        Client.client = client
        Client.socket = BinanceSocketManager(Client.client)
        Client.ticketSocketKey = Client.socket.start_trade_socket(
            SYMBOL, Client.processTradeSocket
        )
        Client.userSocketKey = Client.socket.start_user_socket(Client.processUserSocket)
        Client.socket.start()

        if Client.ticketSocketKey == False or Client.userSocketKey == False:
            print(colors.fail("FAILED") + " to open socket connection")
            exit(1)

    @staticmethod
    def processTradeSocket(message: dict) -> None:
        """
        Processes socket message
        """
        for i in range(len(str(message["p"]))):
            sys.stdout.write("\b")
        sys.stdout.write(str(message["p"]))
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
        return list(Client.client.get_open_orders(symbol=symbol))

    @staticmethod
    def getLatestOrderPrice() -> float:
        if Client.latestPrice == None:
            while Client.latestPrice == None:
                return float(
                    Client.client.get_recent_trades(symbol=SYMBOL, limit=1)[0]["price"]
                )
        return Client.latestPrice

    @staticmethod
    def getLatestOrder() -> dict:
        if Client.latestOrder == None:
            return Client.client.get_recent_trades(symbol=SYMBOL, limit=1)[0]
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
        return Client.client.cancel_order(symbol=symbol, orderId=orderId)

    @staticmethod
    def getAssetBalance(asset: str) -> float:
        return float(Client.client.get_asset_balance(asset=asset)["free"])

    @staticmethod
    def getAveragePrice(asset: str) -> float:
        return float(Client.client.get_avg_price(symbol=asset)["price"])

    @staticmethod
    def getPriceChangeStatistics(asset: str) -> dict:
        return Client.client.get_ticker(symbol=asset)["weightedAvgPrice"]
