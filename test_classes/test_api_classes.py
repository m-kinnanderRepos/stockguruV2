import unittest
import os
import sys
# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.api_classes import HistoryApiConfig, HistoryResponse

class TestHistoryApiConfig(unittest.TestCase):
    def setUp(self):
        self.config = HistoryApiConfig({'API': {'KEY': 'The_Key', 'DAYSAGO': 0, 'HISTORY_APIURL': 'https://mockendpoint.gg'}})

    def test_historyApiConfig_init(self):
        
        self.assertTrue(self.config.key == "The_Key")
        self.assertTrue(self.config.daysAgo == 0)
        self.assertTrue(self.config.historyApiUrl == "https://mockendpoint.gg")


class TestHistoryResponse(unittest.TestCase):
    def setUp(self):
        self.response = HistoryResponse(
                {'symbol': 'ABC', 'open': 1.00, 'high': 1.9, 'low': 1.00, 'close': 1.8, 'volume': 32, 'from': '2022-01-01'})
    
    def test_hisotryResponse_init(self):
        self.assertTrue(self.response.high == 1.9)
        self.assertTrue(self.response.low == 1.00)


if __name__ == '__main__':
    unittest.main()