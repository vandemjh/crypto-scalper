from util.colors import Colors
from model.trade import Trade
from threading import Thread
from settings import NUMBER_OF_TRADES, SCALP_PERCENT


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
            print(
                Colors.info(
                    "Init trade #"
                    + str(i)
                    + " scalping: "
                    + str(tempScalp)
                    + " totaling: "
                    + str(tradeQuantity)
                )
            )
            self.trades.append(Trade(spreadPercent=tempScalp, quantity=tradeQuantity))
            count = count + 1

    def execute(self):
        for trade in self.trades:
            Thread(target=trade.executeForever()).start()
