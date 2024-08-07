from typing import Protocol
from execution_client import ExecutionClient as execution_client 


class PriceListener(Protocol):

    def on_price_tick(self, product_id: str, price: float):
        """
        invoked on market data change
        :param product_id: id of the product that has a price change
        :param price: the current market price of hte product
        :return: None
        """
        order = execution_client.orders.get(product_id)
        if order['product_id'] == product_id and not order['executed']:
                if (order['type'] == "BUY" and price <= order['limit']) or \
                   (order['type'] == "SELL" and price >= order['limit']):
                    execution_client.execute_order(order['type'], product_id, order['amount'])
                    order['executed'] = True
