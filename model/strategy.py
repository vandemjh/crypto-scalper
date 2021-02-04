from os import times
from util import writeOrder
from trade import Trade

class Strategy:
    """
    A strategy is an execution of a series of trades.
    """

    def ___init___(self):
        pass

    async def execute(self):
        while True:
            writeOrder(
                Trade(
                    baseAsset=baseAsset,
                    quoteAsset=quoteAsset,
                    basePrecision=baseAssetPrecision,
                    quotePrecision=quoteAssetPrecision,
                    tickSize=tickSize,
                    stepSize=stepSize,
                ).execute()
            )
            times.sleep(10)  # Avoid placing buy order right after