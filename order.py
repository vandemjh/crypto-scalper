from logging import debug
import time
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL
from colors import colors, phrases
from settings import DEBUG


class order:
    symbol: str
    side: SIDE_BUY or SIDE_SELL
    price: float = 0
    quantity: float = 0

    orderId: str
    clientOrderId: str

    filled: bool = False

    def __init__(
        self, symbol: str, client: Client, side: str, price: int, quantity: int
    ) -> None:
        self.side = side
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return (
            phrases.debug()
            + phrases.filledOrPlaced(self.filled)
            + phrases.buyOrSell(self.side)
            + "@ "
            + str(self.price)
            + " totaling "
            + str(self.quantity)
            + "."
        )

    def fill(self, price: float, quantity: float):
        """
        Fill this order
        """
        self.filled = True
        self.price = price
        self.quantity = quantity
        self.printStatus()

    def waitForOrder(self) -> dict:
        """
        Waits for the order to fill, returns filled order dict
        """
        # getOrder = client.get_order(
        #     symbol=SYMBOL,
        #     orderId=self.orderId,
        #     origClientOrderId=self.clientOrderId,
        # )
        getOrder = {"price": 123, "quantity": 123}
        while not self.filled:
            print(colors.INFO + "\tAwaiting order fill..." + colors.END)
            time.sleep(1)
            # order = client.get_order(
            #     symbol=SYMBOL,
            #     orderId=buyOrderId,
            #     origClientOrderId=buyClientOrderId,
            # )
            self.fill(getOrder["price"], getOrder["quantity"])

        return getOrder

    def place(self):
        """
        Place the order
        """
        if self.side == SIDE_BUY:
            pass
            # client.order_limit_buy(
            # symbol=SYMBOL,
            # quantity=toBuyQuantity,
            # price='0.00001')
        elif self.side == SIDE_SELL:
            # client.order_limit_sell(
            # symbol=SYMBOL,
            # quantity=toBuyQuantity,
            # price='0.00001')
            pass
        self.printStatus()

    def printStatus(self) -> None:
        print(
            phrases.filledOrPlaced(self.filled)
            + phrases.buyOrSell(self.side)
            + ": order @ "
            + str(self.price)
            + " totaling "
            + str(self.quantity)
        )