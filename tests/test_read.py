import unittest
import os
import sys
# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from read import *
from classes.stock_classes import Stock

class TestReadMethods(unittest.TestCase):
    def setUp(self):
        self.json_file_path = "tests/test_files/test-config-history_api.json"
        self.csv_file_path = "tests/test_files/test-stocks.csv"

    def test_read_json(self):
        json = read_json(self.json_file_path)
        self.assertTrue(json["A"]["B"] == "1")

    def test_read_csv_to_list_of_Stocks(self):
        listOfStock = read_csv_to_list_of_Stocks(self.csv_file_path)
        self.assertTrue(listOfStock[0].name == "ABC")
        self.assertTrue(listOfStock[1].price == "17.38")



if __name__ == '__main__':
    unittest.main()