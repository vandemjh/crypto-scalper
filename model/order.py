from util.util import Util
from model.exchange import ExchangeInformation
from typing import Callable
from util.client import Client

from binance.exceptions import BinanceAPIException
from settings import DEBUG, SLEEP_MULTIPLIER
import time
from binance.enums import SIDE_BUY, SIDE_SELL
from util.colors import Colors, phrases


class Order:
    def __init__(
        self,
        symbol: str,
        side: SIDE_BUY or SIDE_SELL,
        price: float = 0,
        quantity: float = 0,
        baseAssetPrecision: int = 8,
        quoteAssetPrecision: int = 8,
        tickSize: float = 0,
        stepSize: float = 0,
        cancelThreshold: float or None = None,
        cancelled: bool = False,
    ) -> None:
        self.orderId: int = 0
        self.clientOrderId: str = ""
        self.filled: bool = False

        self.symbol = symbol
        self.symbol: str
        self.side = side
        self.cancelThreshold = cancelThreshold

        # self.price = round(price, quoteAssetPrecision)
        ticks = 0
        temp = tickSize
        while temp < 1:
            temp = temp * 10
            ticks = ticks + 1
        self.price = round(price, ticks)

        # self.quantity = round(quantity, baseAssetPrecision)
        ticks = 0
        temp = stepSize
        while temp < 1:
            temp = temp * 10
            ticks = ticks + 1
        self.quantity = round(quantity, ticks)

        self.baseAssetPrecision = baseAssetPrecision
        self.quoteAssetPrecision = quoteAssetPrecision
        self.tickSize = tickSize
        self.cancelled = cancelled

    def __str__(self) -> str:
        return (
            ("\n" if DEBUG else "")  # Added newline
            + phrases.cancelled(self.cancelled)
            + phrases.filledOrPlaced(self.filled)
            + phrases.buyOrSell(self.side)
            + "@ "
            + str(self.price)
            + Colors.buy("(" + str(ExchangeInformation.quoteAsset) + ")")
            + Util.getPercentDiff(self.price)
            + " totaling "
            + str(self.quantity)
            + Colors.sell("(" + str(ExchangeInformation.baseAsset) + ") ")
            + phrases.thresholdPricedOrNot(self.cancelThreshold)
            + Util.getPercentDiff(self.cancelThreshold)
            + "."
        )

    def fill(self):
        """
        Fill this order
        """
        self.filled = True
        self.printStatus()

    def waitForOrder(self, callback: Callable or None = None) -> dict or False:
        """
        Waits for the order to fill, returns filled order dict
        :param callback function cancels this order
        :returns False if order is cancelled before being fully filled
        """
        # getOrder = Order.getAccountEvent()
        # while (
        #     getOrder == None
        #     or not "X" in getOrder
        #     or not "i" in getOrder
        #     or not getOrder["X"] == "FILLED"
        #     or not int(getOrder["i"]) == self.orderId
        # ):
        #     time.sleep(SLEEP_MULTIPLIER *1)
        #     getOrder = Order.getAccountEvent()
        # print(getOrder)
        # self.fill()
        # return getOrder
        if DEBUG:
            time.sleep(SLEEP_MULTIPLIER * 3)
            return {}

        retryTimes: int = 3
        count: int = 0
        getOrder = None
        while getOrder == None:
            try:
                getOrder = Client.getOrder(orderId=self.orderId)
            except BinanceAPIException:
                time.sleep(
                    SLEEP_MULTIPLIER * 1
                )  # Wait for order to be accepted by exchange
                count = count + 1
                if count > retryTimes:
                    raise
        try:
            # Does not account for partially filled orders
            while not getOrder["status"] == "FILLED":
                if (not callback == None and callback()) or (
                    not self.cancelThreshold == None
                    and self.side == SIDE_BUY
                    and Client.getAveragePrice() > self.cancelThreshold
                ):
                    self.cancel()
                    return False
                time.sleep(SLEEP_MULTIPLIER * 10)
                getOrder = Client.getOrder(orderId=self.orderId)
        except:
            raise
        self.fill()
        return getOrder

    def place(self) -> dict or None:
        """
        Place the order
        :returns api response or None if in debug mode
        """
        self.printStatus()
        if self.side == SIDE_BUY:
            if DEBUG:
                pass
            else:
                try:
                    result = Client.orderLimitBuy(
                        quantity=self.quantity,
                        price=self.price,
                    )
                    self.orderId = int(result["orderId"])
                    self.clientOrderId = result["clientOrderId"]
                    return result
                except BinanceAPIException:
                    time.sleep(SLEEP_MULTIPLIER * 2)
                    print(Colors.warn("Error placing buy, trying again"))
                    result = Client.orderLimitBuy(
                        quantity=self.quantity,
                        price=self.price,
                    )
                    self.orderId = int(result["orderId"])
                    self.clientOrderId = result["clientOrderId"]
                    return result
        elif self.side == SIDE_SELL:
            if DEBUG:
                pass
            else:
                try:
                    result = Client.orderLimitSell(
                        quantity=self.quantity,
                        price=self.price,
                    )
                    self.orderId = int(result["orderId"])
                    self.clientOrderId = result["clientOrderId"]
                    return result
                except BinanceAPIException:
                    time.sleep(SLEEP_MULTIPLIER * 2)
                    print(Colors.warn("Error placing sell, trying again"))
                    time.sleep(SLEEP_MULTIPLIER * 1)  # Last order likely not completed
                    result = Client.orderLimitSell(
                        quantity=self.quantity,
                        price=self.price,
                    )
                    self.orderId = int(result["orderId"])
                    self.clientOrderId = result["clientOrderId"]
                    return result
        return None

    def printStatus(self) -> None:
        print(self)

    def cancel(self) -> dict:
        """
        Cancel this order
        :returns api response
        """
        self.cancelled = True
        self.printStatus()
        return Client.cancelOrder(self.orderId)