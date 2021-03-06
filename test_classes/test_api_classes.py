import unittest
import os
import sys
# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.api_classes import HistoryApiConfig, HistoryResponse, LastQuoteResponse

class TestHistoryApiConfig(unittest.TestCase):
    def setUp(self):
        self.config = HistoryApiConfig(
            {'API': {'KEY': 'The_Key', 'DAYSAGOFOURTEEN': 14,"DAYSAGOTWENTYEIGHT": 28, 'HISTORY_APIURL': 'https://mockendpoint.gg', 'LASTQUOTE_APIURL': 'https://mockendpoint2.gg'}})

    def test_historyApiConfig_init(self):
        
        self.assertTrue(self.config.key == "The_Key")
        self.assertTrue(self.config.daysAgoFourteen == 14)
        self.assertTrue(self.config.daysAgoTwentyEight == 28)
        self.assertTrue(self.config.historyApiUrl == "https://mockendpoint.gg")
        self.assertTrue(self.config.lastQuoteApiUrl == "https://mockendpoint2.gg")


class TestHistoryResponse(unittest.TestCase):
    def setUp(self):
        self.response = HistoryResponse(
                {'symbol': 'ABC', 'open': 1.00, 'high': 1.9, 'low': 1.00, 'close': 1.8, 'volume': 32, 'from': '2022-01-01'})
    
    def test_hisotryResponse_init(self):
        self.assertTrue(self.response.high == 1.9)
        self.assertTrue(self.response.low == 1.00)

class TestLastQuoteResponse(unittest.TestCase):
    def setUp(self):
        self.response = LastQuoteResponse({"symbol":"ABC", "ask":10.00, "bid":10.00, "asize":3, "bsize":1, "timestamp":1604710766331})

    def test_lastQuoteResponse_init(self):
        self.assertTrue(self.response.ask == 10.00)    
        self.assertTrue(self.response.bid == 10.00)


if __name__ == '__main__':
    unittest.main()