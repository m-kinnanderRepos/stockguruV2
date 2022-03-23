import requests
import json
from datetime import date, timedelta
import sys
import csv
from classes.api_classes import HistoryResponse, HistoryApiConfig
from classes.stock_classes import Stock
from read import *





def get_data(listOfStocks: list, config: HistoryApiConfig):
  today = date.today()
  fiveDaysAgo = today - timedelta(days=config.daysAgo)
  url = config.historyApiUrl

  for stock in listOfStocks:
    stockName = stock.name
    querystringFiveDaysAgo = {"stock":stockName,"date":fiveDaysAgo.strftime("%Y-%m-%d"),"apikey":config.key}
    response = requests.request("GET", url, params=querystringFiveDaysAgo)

    if(response.status_code == 200):
        stockDecisionMaking(HistoryResponse(json.loads(response.text)), stockName, stock.price)

    else:
        print("Error in call to api.")



def stockDecisionMaking(historyAPIResponse: HistoryResponse, stockName: str, stockPrice: float):
    print("For " + stockName)
    print("Buying price was: " + stockPrice)
    print("High for 5 days ago is : " + historyAPIResponse.highToString())
    print("Low for 5 days ago is : " + historyAPIResponse.lowToString())

    averageFiveDaysAgo = (historyAPIResponse.high + historyAPIResponse.low) / 2
    print("Average of the two is : " + str(averageFiveDaysAgo))

    diff = float(stockPrice) / averageFiveDaysAgo
    print("Diff is : " + str(diff))
    
    percent = 0
    if(diff < 1):
        percent = diff * 100
    
        if(percent > 46):
            print("Is greater than 46 percent")

        else:
            print("Is less than 46 percent")
    
    else:
        print("Price is less than buy price")


          
if __name__ == "__main__":
    configFile: HistoryApiConfig = HistoryApiConfig(read_json("config-history_api.json"))
    listOfStocks: list = read_csv_to_list_of_Stocks("stocks.csv")
    
    get_data(listOfStocks, configFile)