import requests
import json
from datetime import date, timedelta
import sys
import csv
from classes.api_classes import HistoryResponse, HistoryApiConfig, LastQuoteResponse
from classes.stock_classes import Stock, Advice

def get_api_call(url, queryString):
    return requests.request("GET", url, params=queryString)


def get_data(listOfStocks: list, config: HistoryApiConfig):
    today = date.today()
    fourteenDaysAgo = today - timedelta(days=config.daysAgoFourteen)
    twentyEightDaysAgo = today - timedelta(days=config.daysAgoTwentyEight)
    url = config.historyApiUrl

    tupleList = []
    for stock in listOfStocks:
        todaysResponse = get_api_call(config.lastQuoteApiUrl + stock.name, {"apikey":config.key})
        fourteenDaysResponse = get_api_call(config.historyApiUrl, 
            {"stock":stock.name,"date":fourteenDaysAgo.strftime("%Y-%m-%d"),"apikey":config.key})
        twentyEightDaysResponse = get_api_call(config.historyApiUrl, 
            {"stock":stock.name,"date":twentyEightDaysAgo.strftime("%Y-%m-%d"),"apikey":config.key})
        

        if(twentyEightDaysResponse.status_code == 200 and fourteenDaysResponse.status_code == 200
         and todaysResponse.status_code == 200):
            # What should be returned now is a list of (LastQuoteResponse, HistoryResponse, HistoryResponse, stock)
            todaysResponseClass = LastQuoteResponse(json.loads(todaysResponse.text))
            fourteenDaysResponseClass = HistoryResponse(json.loads(fourteenDaysResponse.text))
            twentyEightDaysResponseClass = HistoryResponse(json.loads(twentyEightDaysResponse.text))
            tupleList.append((todaysResponseClass, fourteenDaysResponseClass, twentyEightDaysResponseClass, stock))

        else:
            print(f"Error in call to api for {stock.name}.")
    return tupleList


# Takes in List((LastQuoteResponse, HistoryResponse, HistoryResponse, stock))
def stockDecisionMaking(historyResponseStockTupleData: list):
    # Percentage Increase = [ (Final Value - Starting Value) / |Starting Value| ] × 100
    adviceList = []
    for dataSet in historyResponseStockTupleData:
        averageFiveDaysAgo = (dataSet[0].high + dataSet[0].low) / 2
        # diff = float(dataSet[1].price) / averageFiveDaysAgo
        diff = ((averageFiveDaysAgo - float(dataSet[1].price)) / float(dataSet[1].price)) * 100
    
        finalDecision = ""
        # I feel that stock increase and decrease are two important seperators. I am keeping this check in top level if/else.
        # Maybe in the future, these can be broken into two new functions and handled to give helpful feedback
        # for decrease price too. 
        if(diff >= 0):        
            if(diff > 46):
                finalDecision += "Is greater than 46 percent"
            else:
                finalDecision += "Is less than 46 percent"

        else:
            finalDecision += "Price is less than buy price"

        adviceList.append(Advice(dataSet[0], dataSet[1], averageFiveDaysAgo, diff, finalDecision))

    return adviceList
