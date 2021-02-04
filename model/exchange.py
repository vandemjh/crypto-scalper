from settings import IN_PLAY_PERCENT, SYMBOL
from util.client import Client


class ExchangeInformation:
    baseAsset: str = None
    baseAssetPrecision: int = None
    quoteAsset: str = None
    quoteAssetPrecision: int = None
    minPrice: float = None
    maxPrice: float = None
    tickSize: float = None
    stepSize: float = None
    balance: float = None

    @staticmethod
    def init():
        exchangeInfo: dict = Client.getExchangeInformation()
        symbols = exchangeInfo["symbols"]
        filters: list = []
        for symbol in symbols:
            if symbol["symbol"] == SYMBOL:
                ExchangeInformation.baseAsset = symbol["baseAsset"]
                ExchangeInformation.baseAssetPrecision = symbol["baseAssetPrecision"]
                ExchangeInformation.quoteAsset = symbol["quoteAsset"]
                ExchangeInformation.quoteAssetPrecision = symbol["quotePrecision"]
                filters = symbol["filters"]
        for filter in filters:
            if filter["filterType"] == "PRICE_FILTER":
                ExchangeInformation.minPrice = float(filter["minPrice"])
                ExchangeInformation.maxPrice = float(filter["maxPrice"])
                ExchangeInformation.tickSize = float(filter["tickSize"])
                print(ExchangeInformation.tickSize)
            if filter["filterType"] == "LOT_SIZE":
                ExchangeInformation.stepSize = float(filter["stepSize"])

        ExchangeInformation.balance = float(
            Client.getAssetBalance(ExchangeInformation.quoteAsset)
        ) * (IN_PLAY_PERCENT / 100)
