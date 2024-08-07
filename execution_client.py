from typing import Protocol


class ExecutionException(Exception):
    pass


class ExecutionClient(Protocol):


    def __init__(self):
        self.orders = {}

    def buy(self, product_id: str, amount: int, order_type: str, limit_price: int):
        """
        Execute a buy order, throws ExecutionException on failure
        :param product_id: the product to buy
        :param amount: the amount to buy
        :return: None
        """
        if self.should_execute(order_type, limit_price, amount):
            self.orders[product_id] = {
                'type': order_type,
                'amount': amount,
                'limit_price': limit_price,
                'executed': True
            }
        else:
            raise ExecutionException

    def sell(self, product_id: str, amount: int):
        """
        Execute a sell order, throws ExecutionException on failure
        :param product_id: the product to sell
        :param amount: the amount to sell
        :return: None
        """
        order = self.orders.get(product_id)
        if self.should_execute(order['type'], order['limit_price'], amount):
            del self.orders[product_id]
        else:
            raise ExecutionException


    def should_execute(self, order_type, limit_price, price):
        """Check if the order should be executed based on the current price."""
        if order_type == 'buy' and price <= limit_price:
            return True
        if order_type == 'sell' and price >= limit_price:
            return True
        return False