from os import times
from util import writeOrder
from model import Trade


class Strategy:
    """
    A strategy is an execution of a series of trades.
    """

    def ___init___(self):
        pass

    async def execute(self):
        while True:
            trade = Trade()
            await trade.execute()
            writeOrder(trade)
            times.sleep(10)  # Avoid placing buy order right after