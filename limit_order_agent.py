import sys, os
sys.path.append("..")
from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        # self.ibm_limit_price = 100
        # self.ibm_order_placed = False
        self.execution_client = execution_client
        self.orders = []
        super().__init__()

    def add_order(self, product_id, order_operation, amount, price_limit):
        if order_operation not in {"buy","sell"}:
            raise Exception("Wrong Order Added, Please Check!")

        if amount < 0 or price_limit < 0:
            raise ValueError("Amount/Limit should be greater than zero.")

        if not isinstance(amount, (int)) and not isinstance(price_limit, (int)):
            raise ValueError("Amount/Limit should be integer.")

        self.orders.append({
            'order_operation': order_operation,
            'product_id': product_id,
            'amount': amount,
            'price_limit': price_limit
        })

    def on_price_tick(self, product_id, price):
        # see PriceListener protocol and readme file
        for order in self.orders[:]:

            if order['product_id'] == product_id:
                if order['order_operation'] == 'buy' and price <= order['price_limit']:
                    self.execution_client.buy(product_id, order['amount'])

                    self.orders.remove(order)

                if order['order_operation'] == 'sell' and price >= order['price_limit']:
                    self.execution_client.sell(product_id, order['amount'])

                    self.orders.remove(order)

    # def price_tick(self, product_id, price):
    #     if product_id == 'IBM' and price < self.ibm_limit_price and not self.ibm_order_placed:
    #         self.execution_client.buy('IBM', 1000)
    #         self.ibm_order_placed = True

class MockingExecutionClient(ExecutionClient):
    pass


order_obj = MockingExecutionClient(_exec)
order_obj.add_order("product_x","buy", 500,100)
order_obj.add_order("product_y","buy", 1000,10)
order_obj.add_order("product_z","sell", 950,150)
order_obj.on_price_tick("product_x",90)
order_obj.on_price_tick("product_y",90)
order_obj.on_price_tick("product_z",200)
