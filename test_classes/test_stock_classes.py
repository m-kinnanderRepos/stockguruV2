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


class TestAdvice2(unittest.TestCase):
    def setUp(self):
        self.stock = Stock(['ABC', '1.23'])

    def test_advice_init(self):
        advice = Advice(4.00, 3.00, 2.87, self.stock, "Think about selling")
        self.assertTrue(advice.stock == self.stock)
        self.assertTrue(advice.currentAsk == 4.00)
        self.assertTrue(advice.averageFourteenDaysAgo == 3.00)
        self.assertTrue(advice.averageTwentyEightDaysAgo == 2.87)
        self.assertTrue(advice.finalDecision == "Think about selling")


if __name__ == '__main__':
    unittest.main()