import unittest
import os
import sys
# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.stock_classes import Stock

class TestStock(unittest.TestCase):

    def test_stock_init(self):
        stock = Stock(['ABC', '1.23'])
        self.assertTrue(stock.name == "ABC")
        self.assertTrue(stock.price == "1.23")


if __name__ == '__main__':
    unittest.main()