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

def are_two_Advice_instances_the_same(instance1, instance2):
    return (instance1.historyResponse == instance2.historyResponse and 
            instance1.stock == instance2.stock and
            instance1.averageFiveDaysAgo == instance2.averageFiveDaysAgo and
            instance1.diff == instance2.diff and
            instance1.finalDecision == instance2.finalDecision)
    

class TestStockMethods(unittest.TestCase):
    def setUp(self):
        self.response46OrMore = HistoryResponse(
                {'symbol': 'ABC', 'open': 75.00, 'high': 100.00, 'low': 50.00, 'close': 75.00, 'volume': 32, 'from': '2022-01-01'})
        self.responseLessThan46 = HistoryResponse(
                {'symbol': 'ABC', 'open': 75.00, 'high': 75.00, 'low': 50.00, 'close': 75.00, 'volume': 32, 'from': '2022-01-01'})
        self.responseNegative = HistoryResponse(
                {'symbol': 'ABC', 'open': 75.00, 'high': 25.00, 'low': 0.00, 'close': 75.00, 'volume': 32, 'from': '2022-01-01'})        
        self.responseZero = HistoryResponse(
                {'symbol': 'ABC', 'open': 50.00, 'high': 50.00, 'low': 50.00, 'close': 50.00, 'volume': 32, 'from': '2022-01-01'}) 

        self.stock = Stock(['ABC', '50.00'])

        self.config = HistoryApiConfig({'API': {'KEY': 'The_Key', 'DAYSAGOFOURTEEN': 14, 'HISTORY_APIURL': 'https://mockendpoint.gg',"DAYSAGOTWENTYEIGHT": 28}})
        self.config_HISTORY_APIURL = HistoryApiConfig({'API': {'KEY': 'The_Key', 'DAYSAGOFOURTEEN': 14, 'HISTORY_APIURL': 'ERROR',"DAYSAGOTWENTYEIGHT": 28}})
        
        self.advice46OrMore = Advice(self.response46OrMore, self.stock, 75.00, 50.00, "Is greater than 46 percent")
        self.adviceLessThan46 = Advice(self.responseLessThan46, self.stock, 62.5, 25.00, "Is less than 46 percent")
        self.adviceNegative = Advice(self.responseNegative, self.stock, 12.5, -75.0, "Price is less than buy price")
        self.adviceZero = Advice(self.responseZero, self.stock, 50.00, 0.00, "Is less than 46 percent")

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
        self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.advice46OrMore))

    def test_stockDecisionMaking_LessThan46(self):
        decisions = stockDecisionMaking([(self.responseLessThan46, self.stock)])
        self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.adviceLessThan46))

    def test_stockDecisionMaking_Negative(self):
        decisions = stockDecisionMaking([(self.responseNegative, self.stock)])
        self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.adviceNegative))

    def test_stockDecisionMaking_Zero(self):
        decisions = stockDecisionMaking([(self.responseZero, self.stock)])
        self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.adviceZero))

    def test_returnDecisionAsString_is_string_46PercentOrMore(self):
        self.assertTrue(isinstance(self.advice46OrMore.returnDecisionAsString(), str))

    def test_returnDecisionAsString_is_string_Negative(self):
        self.assertTrue(isinstance(self.adviceNegative.returnDecisionAsString(), str))




if __name__ == '__main__':
    unittest.main()