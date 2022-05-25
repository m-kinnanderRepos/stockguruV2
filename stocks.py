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
def stockDecisionMaking(threeResponsesStockData: list):
    # Percentage Increase = [ (Final Value - Starting Value) / |Starting Value| ] × 100
    adviceList = []
    for dataSet in threeResponsesStockData:
        averageFourteenDaysAgo = (dataSet[1].high + dataSet[1].low) / 2
        averageTwentyEightDaysAgo = (dataSet[2].high + dataSet[2].low) / 2
        # diff = float(dataSet[1].price) / averageFiveDaysAgo
        diffToday = ((dataSet[0].ask - float(dataSet[3].price)) / float(dataSet[3].price)) * 100
        diffFourteenDaysAgo = ((averageFourteenDaysAgo - float(dataSet[3].price)) / float(dataSet[3].price)) * 100
        diffTwentyEightDaysAgo = ((averageTwentyEightDaysAgo - float(dataSet[3].price)) / float(dataSet[3].price)) * 100
    
        finalDecision = ""
        
        if(diffFourteenDaysAgo > 46 and diffTwentyEightDaysAgo > 46):
            finalDecision += "could be trending DOWN. Check tomorrow."
        else:
            finalDecision += "do not sell."

        adviceList.append(Advice(dataSet[0].ask, averageFourteenDaysAgo, averageTwentyEightDaysAgo, dataSet[3], finalDecision))

    return adviceList
