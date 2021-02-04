from util.colors import Colors
from model.trade import Trade
from threading import Thread
from settings import NUMBER_OF_TRADES, SCALP_PERCENT
from typing import List


class Strategy:
    """
    A strategy is an execution of a series of trades.
    """

    def __init__(self, numberOfTrades=NUMBER_OF_TRADES, totalQuantity: float = 0):
        self.trades: list[Trade] = []
        tradeQuantity: float = totalQuantity / numberOfTrades
        count = 1
        for i in range(numberOfTrades):
            tempScalp = SCALP_PERCENT * count
            self.trades.append(Trade(spreadPercent=tempScalp, quantity=tradeQuantity))
            count = count + 1

    def execute(self) -> List[Thread]:
        threads: List[Thread] = []
        for trade in self.trades:
            t = Thread(target=trade.executeForever)
            threads.append(t)
            t.start()
        return threads
