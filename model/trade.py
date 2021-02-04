from threading import Thread
import time
from util.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL
from settings import SCALP_PERCENT, SYMBOL
from model import ExchangeInformation
from model import Order


class Trade:
    """
    A trade is a set of one buy and one sell order
    """

    def findBestPrice() -> float:
        return (
            Order.getAveragePrice(SYMBOL)
            if Order.getAveragePrice(SYMBOL) < Order.getLatestOrderPrice(SYMBOL)
            else Order.getLatestOrderPrice(SYMBOL)
        )

    def setValues(self):
        self.setBuyValues(self.findBestPrice())
        self.setSellValues(self.findBestPrice())
        if self.buyPrice >= self.sellPrice:
            raise Exception("Buy price higher than sell")

    def setBuyValues(self, averagePrice: float):
        self.buyPrice = averagePrice - (averagePrice * (self.spreadPercent) / 100)
        self.buyQuantity = Client.getAssetBalance(self.quoteAsset) / self.buyPrice
        self.buyCancelThreshold: float = averagePrice + (
            averagePrice * (SCALP_PERCENT / 100)
        )

    def setSellValues(self, averagePrice: float):
        self.sellPrice = averagePrice + (averagePrice * (self.spreadPercent) / 100)
        self.sellQuantity = Order.getAssetBalance(self.baseAsset)
        self.sellCancelThreshold = None  # Unused right now

    def initBuy(self, basePrecision, quotePrecision, tickSize, stepSize):
        self.buyOrder: Order = Order(
            symbol=SYMBOL,
            side=SIDE_BUY,
            price=self.buyPrice,
            quantity=self.buyQuantity,
            basePrecision=self.basePrecision,
            quotePrecision=self.quotePrecision,
            tickSize=self.tickSize,
            stepSize=self.stepSize,
            cancelThreshold=self.buyCancelThreshold,
        )

    def initSell(self):
        self.sellOrder = Order(
            symbol=SYMBOL,
            side=SIDE_SELL,
            price=self.sellPrice,
            quantity=self.sellQuantity,
            basePrecision=self.basePrecision,
            quotePrecision=self.quotePrecision,
            tickSize=self.tickSize,
            stepSize=self.stepSize,
            cancelThreshold=self.sellCancelThreshold,
        )

    def ___init___(self):
        self.baseAsset = ExchangeInformation.baseAsset
        self.spreadPercent = SCALP_PERCENT / 2
        self.quoteAsset = ExchangeInformation.quoteAsset
        self.basePrecision = ExchangeInformation.basePrecision
        self.quotePrecision = ExchangeInformation.quotePrecision
        self.tickSize = ExchangeInformation.tickSize
        self.stepSize = ExchangeInformation.stepSize
        self.buyPrice = 0
        self.sellPrice = 0

        self.setValues(self.findBestPrice())
        self.initBuy()
        self.initSell()

    def placeAndAwaitBuy(self) -> dict:
        self.buyOrder.place()
        time.sleep(1)  # Wait for order to be accepted by exchange
        order = self.buyOrder.waitForOrder()
        while not order:  # Order cancelled or not filled
            self.setValues()
            self.initBuy()
            order = self.buyOrder.waitForOrder()
        return {}.update(order=order)

    def placeAndAwaitSell(self) -> dict:
        self.sellOrder.place()
        time.sleep(1)  # Wait for order to be accepted by exchange
        return {}.update(order=self.sellOrder.waitForOrder())

    async def execute(self) -> dict:
        return (
            {}.update(buy=self.placeAndAwaitBuy()).update(sell=self.placeAndAwaitSell())
        )
