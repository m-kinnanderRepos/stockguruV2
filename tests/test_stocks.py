import requests
import unittest
from unittest import mock
import os
import sys
# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stocks import *
from classes.stock_classes import Stock, Advice
from classes.api_classes import HistoryApiConfig, HistoryResponse, LastQuoteResponse

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
        return MockResponse({"symbol": "ABC", "open": 10.00, "high": 10.00, "low": 10.00, "close": 10.00, "volume": 32, "from": "2022-01-01"}, 200)
    elif args[1] == 'https://mockendpoint2.gg/ABC':
        return MockResponse({"symbol":"AMC", "ask":10.00, "bid":10.00, "asize":3, "bsize":1, "timestamp":1604710766331}, 200)
    elif args[1] == 'ERROR':
        return MockResponse(None,400)

    return MockResponse(None, 404)

def are_two_Advice_instances_the_same(instance1, instance2):
    return (instance1.currentAsk == instance2.currentAsk and
            instance1.averageFourteenDaysAgo == instance2.averageFourteenDaysAgo and
            instance1.averageTwentyEightDaysAgo == instance2.averageTwentyEightDaysAgo and
            instance1.stock == instance2.stock and
            instance1.finalDecision == instance2.finalDecision)
    

class TestStockMethods2(unittest.TestCase):
    def setUp(self):
        self.todayResponse = LastQuoteResponse(
                {"symbol":"ABC", "ask":10.00, "bid":10.00, "asize":3, "bsize":1, "timestamp":1604710766331})
        self.fourteenDayResponse = HistoryResponse(
                {'symbol': 'ABC', 'open': 10.00, 'high': 10.00, 'low': 10.00, 'close': 10.00, 'volume': 32, 'from': '2022-01-01'})
        self.twentyEightDayResponse = HistoryResponse(
                {'symbol': 'ABC', 'open': 10.00, 'high': 10.00, 'low': 10.00, 'close': 10.00, 'volume': 32, 'from': '2022-01-01'})        
        
        self.stock = Stock(['ABC', '10.00'])

        self.config = HistoryApiConfig({'API': {'KEY': 'The_Key', 'DAYSAGOFOURTEEN': 14, "DAYSAGOTWENTYEIGHT": 28, 'HISTORY_APIURL': 'https://mockendpoint.gg', 'LASTQUOTE_APIURL': 'https://mockendpoint2.gg/'}})
        self.config_API_url_error = HistoryApiConfig({'API': {'KEY': 'The_Key', 'DAYSAGOFOURTEEN': 14, "DAYSAGOTWENTYEIGHT": 28, 'HISTORY_APIURL': 'ERROR', 'LASTQUOTE_APIURL': 'ERROR'}})
        
        self.advice = Advice(10.00, 10.00, 10.00, self.stock, "")

        self.decisionNotSellAMC = "do not sell."
        self.decisionCheckTomorrowAMC = "could be trending DOWN. Check tomorrow."
        self.decisionCheckNextWekkAMC = "could be trending UP. Check next week."
        self.decisionSellAMC = "think about selling!"

        
    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('stocks.requests.request', side_effect=mocked_requests_get)
    def test_get_data_json_200(self, mock_get):
        data = get_data([self.stock], self.config)
        self.assertTrue(data[0][0].ask == self.todayResponse.ask)
        self.assertTrue(data[0][1].high == self.fourteenDayResponse.high)
        self.assertTrue(data[0][2].low == self.twentyEightDayResponse.low)
        self.assertTrue(data[0][3].name == self.stock.name)
        self.assertTrue(data[0][3].price == self.stock.price)

    @mock.patch('stocks.requests.request', side_effect=mocked_requests_get)
    def test_get_data_json_Error(self, mock_get):
        data = get_data([self.stock], self.config_API_url_error)
        self.assertTrue(data == [])


    # Descision Making: [0, 14, 28]
    # 000 Answer: Do not sell
    # 001 Answer: Do not sell
    # 010 Answer: Do not sell
    # 011 Answer: Check tomorrow. Could be trending down.
    # 100 Answer: Do not sell
    # 101 Answer: Do not sell
    # 110 Answer: Check next wekk. Could be trending up.
    # 111 Answer: Think about selling

# List((LastQuoteResponse, HistoryResponse, HistoryResponse, stock))
    def test_stockDecisionMaking_000(self):
        decisions = stockDecisionMaking([(self.todayResponse, self.fourteenDayResponse, self.twentyEightDayResponse, self.stock)])
        self.advice.finalDecision = self.decisionNotSellAMC
        self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.advice))

    def test_stockDecisionMaking_001(self):
        self.twentyEightDayResponse.high = 20.00
        self.twentyEightDayResponse.low = 20.00
        decisions = stockDecisionMaking([(self.todayResponse, self.fourteenDayResponse, self.twentyEightDayResponse, self.stock)])
        self.advice.finalDecision = self.decisionNotSellAMC
        self.advice.averageTwentyEightDaysAgo = 20.00
        self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.advice))

    def test_stockDecisionMaking_010(self):
        self.fourteenDayResponse.high = 20.00
        self.fourteenDayResponse.low = 20.00
        decisions = stockDecisionMaking([(self.todayResponse, self.fourteenDayResponse, self.twentyEightDayResponse, self.stock)])
        self.advice.finalDecision = self.decisionNotSellAMC
        self.advice.averageFourteenDaysAgo = 20.00
        self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.advice))

    def test_stockDecisionMaking_011(self):
        self.fourteenDayResponse.high = 20.00
        self.fourteenDayResponse.low = 20.00
        self.twentyEightDayResponse.high = 20.00
        self.twentyEightDayResponse.low = 20.00
        decisions = stockDecisionMaking([(self.todayResponse, self.fourteenDayResponse, self.twentyEightDayResponse, self.stock)])
        self.advice.finalDecision = self.decisionCheckTomorrowAMC
        self.advice.averageFourteenDaysAgo = 20.00
        self.advice.averageTwentyEightDaysAgo = 20.00
        self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.advice))

    def test_stockDecisionMaking_100(self):
        self.todayResponse.ask = 20.00
        decisions = stockDecisionMaking([(self.todayResponse, self.fourteenDayResponse, self.twentyEightDayResponse, self.stock)])
        self.advice.finalDecision = self.decisionNotSellAMC
        self.advice.currentAsk = 20.00
        self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.advice))

    # def test_stockDecisionMaking_101(self):
        # decisions = stockDecisionMaking([(self.todayResponse, self.fourteenDayResponse, self.twentyEightDayResponse, self.stock)])
         # self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.advice))
        # self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.advice))
                  
    # def test_stockDecisionMaking_110(self):
        # decisions = stockDecisionMaking([(self.todayResponse, self.fourteenDayResponse, self.twentyEightDayResponse, self.stock)])
        # self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.advice))
            
    # def test_stockDecisionMaking_111(self):
        # decisions = stockDecisionMaking([(self.todayResponse, self.fourteenDayResponse, self.twentyEightDayResponse, self.stock)])
        # self.assertTrue(are_two_Advice_instances_the_same(decisions[0], self.advice))
        

if __name__ == '__main__':
    unittest.main()