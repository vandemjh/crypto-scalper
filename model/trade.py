import time
from util.client import Client
from util.util import Util
from binance.enums import SIDE_BUY, SIDE_SELL
from settings import SLEEP_MULTIPLIER, SYMBOL
from model.exchange import ExchangeInformation
from model.order import Order
from binance.exceptions import BinanceAPIException


class Trade:
    """
    A trade is a set of one buy and one sell order
    """

    def findBestPrice(self) -> float:
        return (
            Client.getAveragePrice(SYMBOL)
            if Client.getAveragePrice(SYMBOL) < Client.getLatestOrderPrice(SYMBOL)
            else Client.getLatestOrderPrice(SYMBOL)
        )

    def setValues(self):
        self.setBuyValues(self.findBestPrice())
        self.setSellValues(self.findBestPrice())
        if self.buyPrice >= self.sellPrice:
            raise Exception("Buy price higher than sell")

    def setBuyValues(self, bestPrice: float):
        self.buyPrice = bestPrice - (bestPrice * (self.spreadPercent) / 100)
        self.buyQuantity = self.quantity / self.buyPrice
        self.buyCancelThreshold: float = bestPrice + (
            bestPrice * (self.spreadPercent / 100)
        )

    def setSellValues(self, bestPrice: float):
        self.sellPrice = bestPrice + (bestPrice * (self.spreadPercent) / 100)
        self.sellQuantity = self.buyQuantity
        self.sellCancelThreshold = None  # Unused right now

    def initBuy(self):
        self.buyOrder: Order = Order(
            symbol=SYMBOL,
            side=SIDE_BUY,
            price=self.buyPrice,
            quantity=self.buyQuantity,
            baseAssetPrecision=ExchangeInformation.baseAssetPrecision,
            quoteAssetPrecision=ExchangeInformation.quoteAssetPrecision,
            tickSize=ExchangeInformation.tickSize,
            stepSize=ExchangeInformation.stepSize,
            cancelThreshold=self.buyCancelThreshold,
        )

    def initSell(self):
        self.sellOrder = Order(
            symbol=SYMBOL,
            side=SIDE_SELL,
            price=self.sellPrice,
            quantity=self.sellQuantity,
            baseAssetPrecision=ExchangeInformation.baseAssetPrecision,
            quoteAssetPrecision=ExchangeInformation.quoteAssetPrecision,
            tickSize=ExchangeInformation.tickSize,
            stepSize=ExchangeInformation.stepSize,
            cancelThreshold=self.sellCancelThreshold,
        )

    def __init__(self, spreadPercent: float = 0, quantity: float = 0):
        self.spreadPercent = spreadPercent
        self.quantity = quantity
        self.buyPrice = 0
        self.sellPrice = 0

        self.setValues()
        self.initBuy()
        self.initSell()

    def placeAndAwaitBuy(self) -> dict:
        self.buyOrder.place()
        time.sleep(SLEEP_MULTIPLIER * 1)  # Wait for order to be accepted by exchange
        order = self.buyOrder.waitForOrder()
        while not order:  # Order cancelled or not filled
            self.setValues()
            self.initBuy()
            self.buyOrder.place()  # Place new order
            time.sleep(
                SLEEP_MULTIPLIER * 1
            )  # Wait for order to be accepted by exchange
            order = self.buyOrder.waitForOrder()
        toReturn: dict = {}
        toReturn.update(order=order)
        return toReturn

    def placeAndAwaitSell(self) -> dict:
        time.sleep(SLEEP_MULTIPLIER * 1)  # Wait for order to be accepted by exchange
        self.sellOrder.place()
        toReturn: dict = {}
        toReturn.update(order=self.sellOrder.waitForOrder())
        return toReturn

    def execute(self) -> dict:
        toReturn: dict = {}
        toReturn.update(buy=self.placeAndAwaitBuy())
        toReturn.update(sell=self.placeAndAwaitSell())
        Util.writeOrder(toReturn)
        return toReturn

    def executeForever(self) -> None:
        while True:
            try:
                self.execute()
            except BinanceAPIException as e:
                time.sleep(SLEEP_MULTIPLIER * 2)
                if e.status_code == 1006:  # Connection reset, establish new connection
                    Util.initClient()
                    continue
                else:
                    raise