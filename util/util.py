import json
from util.colors import Colors
from model.exchange import ExchangeInformation
from settings import IN_PLAY_PERCENT, NUMBER_OF_TRADES, ORDER_HISTORY, OUTPUT_FILE, SCALP_PERCENT, SYMBOL
from util.client import Client


class Util:
    @staticmethod
    def cancelAllOrders(symbol=SYMBOL):
        openOrders = Client.getOpenOrders(symbol)
        if len(openOrders) != 0:
            print("Canceling open orders for " + Colors.info(SYMBOL) + ":")
        else:
            print("No open orders")
        for order in openOrders:
            print(order["orderId"])
            Client.cancelOrder(order["symbol"], order["orderId"])

    @staticmethod
    def writeOrder(
        order: dict, orderHistory: dict = ORDER_HISTORY, outputFile: str = OUTPUT_FILE
    ) -> None:
        orderHistory.append(order)
        with open(outputFile, "w+") as f:
            f.write(json.dumps(orderHistory))

    @staticmethod
    def printExchangeInformation() -> None:
        print(Colors.info("Available balance is: " + str(ExchangeInformation.balance)))
        print(Colors.info("Scalping: " + str(SCALP_PERCENT) + "%"))
        print(Colors.info("Executing : " + str(NUMBER_OF_TRADES) + " trades at a time"))

        print(
            Colors.warn("Exchange information")
            + Colors.info("\n\tBase asset: ")
            + Colors.BUY
            + ExchangeInformation.baseAsset
            + Colors.END
            + Colors.info("\n\tBase asset precision: ")
            + str(ExchangeInformation.baseAssetPrecision)
            + Colors.info("\n\tQuote asset: ")
            + Colors.SELL
            + ExchangeInformation.quoteAsset
            + Colors.END
            + Colors.info("\n\tQuote asset precision: ")
            + str(ExchangeInformation.quoteAssetPrecision)
            + Colors.info("\n\tMinimum price: ")
            + str(ExchangeInformation.minPrice)
            + Colors.info("\n\tMaximum price: ")
            + str(ExchangeInformation.maxPrice)
            + Colors.info("\n\tTick size: ")
            + str(ExchangeInformation.tickSize)
            + Colors.info("\n\tStep size: ")
            + str(ExchangeInformation.stepSize)
        )