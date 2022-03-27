import unittest
import os
import sys
# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.stock_classes import Stock, Advice
from classes.api_classes import HistoryApiConfig, HistoryResponse

class TestStock(unittest.TestCase):

    def test_stock_init(self):
        stock = Stock(['ABC', '1.23'])
        self.assertTrue(stock.name == "ABC")
        self.assertTrue(stock.price == "1.23")

class TestAdvice(unittest.TestCase):
    def setUp(self):
        self.response = HistoryResponse(
                {'symbol': 'ABC', 'open': 1.00, 'high': 1.9, 'low': 1.00, 'close': 1.8, 'volume': 32, 'from': '2022-01-01'})
        self.stock = Stock(['ABC', '1.23'])

    def test_advice_init(self):
        advice = Advice(self.response, self.stock, 9.99, 0.74, "Is greater than 46 percent")
        self.assertTrue(advice.historyResponse == self.response)
        self.assertTrue(advice.stock == self.stock)
        self.assertTrue(advice.averageFiveDaysAgo == 9.99)
        self.assertTrue(advice.diff == 0.74)
        self.assertTrue(advice.finalDecision == "Is greater than 46 percent")


if __name__ == '__main__':
    unittest.main()