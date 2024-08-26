import sys
sys.path.append("..")
import unittest
from unittest.mock import MagicMock
from limit.limit_order_agent import LimitOrderAgent

class TestLimitOrderAgent(unittest.TestCase):
    def setUp(self):
        self.execution_client = MagicMock()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_buy_order_executes(self):
        self.agent.add_order('TATA', 'buy', 1000, 100)
        self.agent.on_price_tick('TATA', 99)  # Price drops below $100

        self.execution_client.buy.assert_called_with('IBM', amount=1000)

    def test_sell_order_executes(self):
        self.agent.add_order('RELIANCE', 'sell', 500, 150)
        self.agent.price_tick('RELIANCE', 151)  # Price rises above $150

        self.execution_client.sell.assert_called_with('RELIANCE', 500)

    def test_order_not_executed_if_price_is_not_met(self):
        self.agent.add_order('IBM', 'buy', 1000, 100)
        self.agent.price_tick('IBM', 101)  # Price does not drop below $100

        self.execution_client.buy.assert_not_called()

if __name__ == '__main__':
    unittest.main()
