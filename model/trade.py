import time
from util.client import Client
from util.util import Util
from binance.enums import SIDE_BUY, SIDE_SELL
from settings import SYMBOL
from model.exchange import ExchangeInformation
from model.order import Order


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

    def setBuyValues(self, averagePrice: float):
        self.buyPrice = averagePrice - (averagePrice * (self.spreadPercent) / 100)
        self.buyQuantity = self.quantity / self.buyPrice
        self.buyCancelThreshold: float = averagePrice + (
            averagePrice * (self.spreadPercent / 100)
        )

    def setSellValues(self, averagePrice: float):
        self.sellPrice = averagePrice + (averagePrice * (self.spreadPercent) / 100)
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
        time.sleep(1)  # Wait for order to be accepted by exchange
        order = self.buyOrder.waitForOrder()
        while not order:  # Order cancelled or not filled
            self.setValues()
            self.initBuy()
            self.buyOrder.place()  # Place new order
            order = self.buyOrder.waitForOrder()
        return {}.update(order=order)

    def placeAndAwaitSell(self) -> dict:
        self.sellOrder.place()
        time.sleep(1)  # Wait for order to be accepted by exchange
        return {}.update(order=self.sellOrder.waitForOrder())

    def execute(self) -> dict:
        toReturn: dict = {}
        toReturn.update(buy=self.placeAndAwaitBuy())
        toReturn.update(sell=self.placeAndAwaitSell())
        Util.writeOrder(toReturn)
        return toReturn

    def executeForever(self) -> None:
        while True:
            self.execute()