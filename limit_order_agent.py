from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        self.execution_client = execution_client
        self.ibm_limit_price = 100
        self.ibm_order_placed = False
        super().__init__()

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        if product_id == "IBM" and price < self.ibm_limit_price and not self.ibm_order_placed:
            self.execution_client.execute_order("BUY", "IBM", 1000)
            self.ibm_order_placed = True
