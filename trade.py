from threading import Thread
import time
from util.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL
from settings import SYMBOL
from typing import Callable, List
from order import Order


class Trade:
    """
    A trade is a set of one buy and one sell order
    """

    def ___init___(
        self,
        quantity=0,
        spreadPercent=0,
        basePrecision=0,
        quotePrecision=0,
        tickSize=0,
        stepSize=0,
        cancelThreshold=0,
    ):
        assetPrice: float = Client.latestPrice
        self.buyOrder: Order = Order(
            symbol=SYMBOL,
            side=SIDE_BUY,
            price=assetPrice + (assetPrice * spreadPercent / 100),
            quantity=quantity,
            basePrecision=basePrecision,
            quotePrecision=quotePrecision,
            tickSize=tickSize,
            stepSize=stepSize,
            cancelThreshold=cancelThreshold,
        )
        self.sellOrder = Order(
            symbol=SYMBOL,
            side=SIDE_SELL,
            price=assetPrice - (assetPrice * spreadPercent / 100),
            quantity=quantity,
            basePrecision=basePrecision,
            quotePrecision=quotePrecision,
            tickSize=tickSize,
            stepSize=stepSize,
            cancelThreshold=cancelThreshold,
        )

    def placeAndAwaitBuy(self) -> dict:
        self.buyOrder.place()
        time.sleep(1)  # Wait for order to be accepted by exchange
        return {}.update(filled=self.buyOrder.waitForOrder())

    def placeAndAwaitSell(self) -> dict:
        self.sellOrder.place()
        time.sleep(1)  # Wait for order to be accepted by exchange
        return {}.update(filled=self.sellOrder.waitForOrder())

    async def execute(self) -> dict:
        return (
            {}.update(buy=self.placeAndAwaitBuy()).update(sell=self.placeAndAwaitSell())
        )
