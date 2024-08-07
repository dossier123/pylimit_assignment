import unittest
from unittest.mock import MagicMock
from limit.limit_order_agent import LimitOrderAgent

class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.mock_execution_client = MagicMock()
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_buy_ibm_when_price_drops(self):
        # Simulate IBM price tick
        self.agent.price_tick("IBM", 99)
        
        # Check if an order was placed
        self.mock_execution_client.execute_order.assert_called_once_with("BUY", "IBM", 1000)

    def test_add_order_and_execute(self):
        # Add a custom buy order for Apple when price <= 150
        self.agent.add_order("BUY", "AAPL", 50, 150)
        
        # Simulate price tick
        self.agent.price_tick("AAPL", 149)
        
        # Check if the order was executed
        self.mock_execution_client.execute_order.assert_called_once_with("BUY", "AAPL", 50)

    def test_no_order_execution_if_conditions_not_met(self):
        # Add a custom sell order for Google at a higher price
        self.agent.add_order("SELL", "GOOGL", 20, 3000)
        
        # Simulate a price tick that's below the limit
        self.agent.price_tick("GOOGL", 2999)
        
        # Check if the order was NOT executed
        self.mock_execution_client.execute_order.assert_not_called()

if __name__ == "__main__":
    unittest.main()
