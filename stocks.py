import requests
import json
from datetime import date, timedelta
import sys
import csv
from classes.api_classes import HistoryResponse, HistoryApiConfig
from classes.stock_classes import Stock, Advice



def get_data(listOfStocks: list, config: HistoryApiConfig):
    today = date.today()
    fiveDaysAgo = today - timedelta(days=config.daysAgo)
    url = config.historyApiUrl

    tupleList = []
    for stock in listOfStocks:
        querystringFiveDaysAgo = {"stock":stock.name,"date":fiveDaysAgo.strftime("%Y-%m-%d"),"apikey":config.key}
        response = requests.request("GET", url, params=querystringFiveDaysAgo)
        
        if(response.status_code == 200):
            tupleList.append((HistoryResponse(json.loads(response.text)), stock)) 

        else:
            print(f"Error in call to api for {stock.name}.")
    
    return tupleList



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
        if(diff > 0):        
            if(diff > 46):
                finalDecision += "Is greater than 46 percent"
            else:
                finalDecision += "Is less than 46 percent"
        
        else:
            finalDecision += "Price is less than buy price"

        adviceList.append(Advice(dataSet[0], dataSet[1], averageFiveDaysAgo, diff, finalDecision))

    return adviceList
