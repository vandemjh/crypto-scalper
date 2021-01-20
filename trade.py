from typing import List
from order import Order


class Trade:
    """
    A set of orders
    """
    def ___init___(self, numberOfOrders: int = 0, minScalpPercent: float = 0.2):
        self.orders: List[Order] = []