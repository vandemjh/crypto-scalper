from io import StringIO
import json
from logging import DEBUG
from settings import SYMBOL
import time
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL
from colors import colors, phrases
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor


class Order:
    client: Client
    socket: BinanceSocketManager

    ticketSocketKey: str = None
    latestPrice: float = None
    latestOrder: dict = None
    accountEvent: dict = None

    @staticmethod
    def setClient(client: Client):
        """
        Sets static client for orders, starts socket
        """
        Order.client = client
        Order.socket = BinanceSocketManager(Order.client)
        Order.ticketSocketKey = success = Order.socket.start_trade_socket(
            SYMBOL, Order.processTradeSocket
        )
        Order.socket.start_user_socket(Order.processUserSocket)
        Order.socket.start()

        if not success:
            print(colors.fail("FAILED") + " to open socket connection")
            exit(1)

    def __init__(
        self,
        symbol: str,
        side: SIDE_BUY or SIDE_SELL,
        price: float = 0,
        quantity: float = 0,
    ) -> None:
        self.orderId: str = ""
        self.clientOrderId: str = ""
        self.filled: bool = False

        self.symbol = symbol
        self.symbol: str
        self.side = side
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return (
            phrases.filledOrPlaced(self.filled)
            + phrases.buyOrSell(self.side)
            + " @ "
            + str(self.price)
            + " totaling "
            + str(self.quantity)
            + "."
        )

    def fill(self, price: float, quantity: float):
        """
        Fill this order
        """
        self.filled = True
        self.price = price
        self.quantity = quantity
        self.printStatus()

    def waitForOrder(self) -> dict:
        """
        Waits for the order to fill, returns filled order json
        """
        # getOrder = client.get_order(
        #     symbol=SYMBOL,
        #     orderId=self.orderId,
        #     origClientOrderId=self.clientOrderId,
        # )
        getOrder = Order.getLatestOrder()

        # oldPrice = float(getOrder["price"])
        # newPrice = (oldPrice * (SCALP_PERCENT / 100)) + oldPrice
        # print(
        #     colors.warn(
        #         "\t\tHoping to scalp: %"
        #         + str(SCALP_PERCENT)
        #         + " @ $"
        #         + str(newPrice)
        #     )
        # )
        # while float(getOrder["price"]) < newPrice:
        #     time.sleep(5)
        #     getOrder = Order.client.get_recent_trades(symbol=SYMBOL, limit=1)[0]
        #     print(
        #         colors.warn("Current price: ")
        #         + getOrder["price"]
        #         + " %"
        #         + str(((newPrice / float(getOrder["price"])) - 1) * 100) + " off"
        #     )

        # if not

        time.sleep(5)

        # while not self.filled:
        #     print(colors.info("\tAwaiting order fill..."))
        #     time.sleep(5)
        #     print(
        #         colors.info(
        #             "\t\t" + "Current price: " + str(Order.getLatestOrderPrice())
        #         )
        #     )
        #     if DEBUG:
        #         self.fill(getOrder["price"], getOrder["qty"])
        #     else:
        #         getOrder = Order.client.get_order(
        #             symbol=self.symbol,
        #             orderId=self.orderId,
        #             origClientOrderId=self.clientOrderId,
        #         )
        #         if getOrder["status"] == "filled":
        #             pass
        return getOrder

    def place(self):
        """
        Place the order
        """
        if self.side == SIDE_BUY:
            if DEBUG:
                pass
            else:
                Order.client.order_limit_buy(
                    symbol=self.symbol, quantity=self.quantity, price=self.price
                )
        elif self.side == SIDE_SELL:
            if DEBUG:
                pass
            else:
                Order.client.order_limit_sell(
                    symbol=self.symbol, quantity=self.quantity, price=self.price
                )
        self.printStatus()

    def printStatus(self) -> None:
        print(self)

    @staticmethod
    def processTradeSocket(message: dict) -> None:
        """
        Processes socket message
        """
        Order.latestPrice = float(message["p"])

    @staticmethod
    def processUserSocket(message: dict) -> None:
        """
        Processes user socket event
        """
        Order.accountEvent = json.loads(message)

    @staticmethod
    def getOpenOrders(symbol: str) -> list:
        """
        Returns open orders
        """
        return list(Order.client.get_open_orders(symbol=symbol))

    @staticmethod
    def printOpenOrders(symbol: str) -> None:
        """
        Prints open orders
        """
        openOrders = Order.getOpenOrders(symbol)
        if len(openOrders) == 0:
            print("No open orders")
            return
        for o in openOrders:
            print(o)

    @staticmethod
    def getLatestOrderPrice() -> float:
        if Order.latestPrice == None:
            while Order.latestPrice == None:
                return float(Order.client.get_recent_trades(symbol=SYMBOL, limit=1)[0][
                    "price"
                ])
        return Order.latestPrice

    @staticmethod
    def getLatestOrder() -> dict:
        if Order.latestOrder == None:
            return Order.client.get_recent_trades(symbol=SYMBOL, limit=1)[0]
        return Order.latestOrder
    @staticmethod
    def stopSocket():
        """
        Stops the socket and reactor
        """
        Order.socket.close()
        reactor.stop()