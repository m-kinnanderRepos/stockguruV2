import requests
import unittest
from unittest import mock
import os
import sys
# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stocks import *
from classes.stock_classes import Stock, Advice
from classes.api_classes import HistoryApiConfig, HistoryResponse

# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            singleQuotesToDoubleQuotes = json.dumps(text)
            self.text = singleQuotesToDoubleQuotes
            self.status_code = status_code

        def json(self):
            return self.json_data
   
    if args[1] == 'https://mockendpoint.gg':
        return MockResponse({"symbol": "ABC", "open": 75.00, "high": 100.00, "low": 50.00, "close": 75.00, "volume": 32, "from": "2022-01-01"}, 200)
    elif args[1] == 'ERROR':
        return MockResponse(None,400)

    return MockResponse(None, 404)
    

class TestStockMethods(unittest.TestCase):
    def setUp(self):
        self.response46OrMore = HistoryResponse(
                {'symbol': 'ABC', 'open': 75.00, 'high': 100.00, 'low': 50.00, 'close': 75.00, 'volume': 32, 'from': '2022-01-01'})
        self.responseLessThan46 = HistoryResponse(
                {'symbol': 'ABC', 'open': 75.00, 'high': 75.00, 'low': 50.00, 'close': 75.00, 'volume': 32, 'from': '2022-01-01'})
        self.responseNegative = HistoryResponse(
                {'symbol': 'ABC', 'open': 75.00, 'high': 25.00, 'low': 0.00, 'close': 75.00, 'volume': 32, 'from': '2022-01-01'})        
        self.stock = Stock(['ABC', '50.00'])
        self.config = HistoryApiConfig({'API': {'KEY': 'The_Key', 'DAYSAGO': 0, 'HISTORY_APIURL': 'https://mockendpoint.gg'}})
        self.config_HISTORY_APIURL = HistoryApiConfig({'API': {'KEY': 'The_Key', 'DAYSAGO': 0, 'HISTORY_APIURL': 'ERROR'}})
        self.advice46OrMore = Advice(self.response46OrMore, self.stock, 75.00, 50.00, "Is greater than 46 percent")
        self.adviceLessThan46 = Advice(self.responseLessThan46, self.stock, 62.5, 25.00, "Is less than 46 percent")
        self.adviceNegative = Advice(self.responseNegative, self.stock, 12.5, -75.0, "Price is less than buy price")

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('stocks.requests.request', side_effect=mocked_requests_get)
    def test_get_data_json_200(self, mock_get):
        data = get_data([self.stock], self.config)
        self.assertTrue(data[0][0].high == self.response46OrMore.high)
        self.assertTrue(data[0][0].low == self.response46OrMore.low)
        self.assertTrue(data[0][1].name == self.stock.name)
        self.assertTrue(data[0][1].price == self.stock.price)

    @mock.patch('stocks.requests.request', side_effect=mocked_requests_get)
    def test_get_data_json_Error(self, mock_get):
        data = get_data([self.stock], self.config_HISTORY_APIURL)
        self.assertTrue(data == [])

    def test_stockDecisionMaking_46PercentOrMore(self):
        decisions = stockDecisionMaking([(self.response46OrMore, self.stock)])
        self.assertTrue(decisions[0].historyResponse == self.advice46OrMore.historyResponse)
        self.assertTrue(decisions[0].stock == self.advice46OrMore.stock)
        self.assertTrue(decisions[0].averageFiveDaysAgo == self.advice46OrMore.averageFiveDaysAgo)
        self.assertTrue(decisions[0].diff == self.advice46OrMore.diff)
        self.assertTrue(decisions[0].finalDecision == self.advice46OrMore.finalDecision)

    def test_stockDecisionMaking_LessThan46(self):
        decisions = stockDecisionMaking([(self.responseLessThan46, self.stock)])
        self.assertTrue(decisions[0].historyResponse == self.adviceLessThan46.historyResponse)
        self.assertTrue(decisions[0].stock == self.adviceLessThan46.stock)
        self.assertTrue(decisions[0].averageFiveDaysAgo == self.adviceLessThan46.averageFiveDaysAgo)
        self.assertTrue(decisions[0].diff == self.adviceLessThan46.diff)
        self.assertTrue(decisions[0].finalDecision == self.adviceLessThan46.finalDecision)

    def test_stockDecisionMaking_Negative(self):
        decisions = stockDecisionMaking([(self.responseNegative, self.stock)])
        self.assertTrue(decisions[0].historyResponse == self.adviceNegative.historyResponse)
        self.assertTrue(decisions[0].stock == self.adviceNegative.stock)
        self.assertTrue(decisions[0].averageFiveDaysAgo == self.adviceNegative.averageFiveDaysAgo)
        self.assertTrue(decisions[0].diff == self.adviceNegative.diff)
        self.assertTrue(decisions[0].finalDecision == self.adviceNegative.finalDecision)




if __name__ == '__main__':
    unittest.main()