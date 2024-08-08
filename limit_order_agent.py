from trading_framework.execution_client import ExecutionClient, ExecutionException
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

    def add_order(self, order_type: str, product_id: str, amount: int, limit_price: float):
        """Add an order to the list of orders."""
        if order_type not in {'buy', 'sell'}:
            raise ExecutionException("Order side must be 'buy' or 'sell'.")
        if amount <= 0:
            raise ExecutionException("Amount must be greater than 0.")
        if limit_price <= 0:
            raise ExecutionException("Limit price must be greater than 0.")

        ExecutionClient.orders[product_id] = {
                'type': order_type,
                'amount': amount,
                'limit_price': limit_price,
                'executed': True
        }
