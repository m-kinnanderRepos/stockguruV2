import requests
import json
from datetime import date, timedelta
import sys
import csv
from classes.api_classes import HistoryResponse, HistoryApiConfig
from classes.stock_classes import Stock, Advice


# 
def get_data(listOfStocks: list, config: HistoryApiConfig):
    today = date.today()
    fiveDaysAgo = today - timedelta(days=config.daysAgoFourteen)
    url = config.historyApiUrl

    tupleList = []
    for stock in listOfStocks:
        # We should be making three calls now.
        # Making sure each one is successful.
        querystringFiveDaysAgo = {"stock":stock.name,"date":fiveDaysAgo.strftime("%Y-%m-%d"),"apikey":config.key}
        response = requests.request("GET", url, params=querystringFiveDaysAgo)
        
        if(response.status_code == 200):
            # What should be returned now is a list of (LastQuoteResponse, HistoryResponse, HistoryResponse, stock)
            # That would be response from Last Quote of today, history quote from 14 days ago, history quote from 28 days ago, and stock
            tupleList.append((HistoryResponse(json.loads(response.text)), stock)) 

        else:
            print(f"Error in call to api for {stock.name}.")
    # Should now return List((LastQuoteResponse, HistoryResponse, HistoryResponse, stock))
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
