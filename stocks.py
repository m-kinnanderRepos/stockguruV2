import requests
import json
from datetime import date, timedelta
import sys
import csv
from classes.api_classes import HistoryResponse, HistoryApiConfig
from classes.stock_classes import Stock, Advice



def get_data(listOfStocks: list, config: HistoryApiConfig):
    today = date.today()
    fiveDaysAgo = today - timedelta(days=config.daysAgoFourteen)
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


# I could keep this funcionality as is. But there are some options
#   1) I could keep as is and in function above, manipulate data as the high and low are averages from
#       the data of the three calls.
#   2) I could redo everything. Make the first call of three weeks ago be some decision and 
#       print out if three is not above 45 and keep going if it is to 5 days ago.
#   3) I could make the api call reusable to take in certain day. So I would keep calling get_data
#       with 21 days then 5 then 30. Then decision making between all three calls when necessary. 
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




#Get data for all of 21 days ago
#If isn't above 45% leave it at that.
#If greater than 45% then call api for 5 days ago. 
# If isn't above 45% leave it at that.
# If current time is when Stock exchange is open, call today. 

# Could do 28, 14, then today.


# Add day to Advice. 


# Get the data for all three days (28, 14, and today).
# Do advice from the three sets.
#   1) If 28 isn't above 45% than saw so plus is 14 days above 45%?
#   2) If 28 Is above 45%, then is 14?
#   3) If 28 and 14 are above 45%, then buy. 

# Decision Making: [28, 14, 0]
# [00*] Answer: Do not sell
# [010] Answer: Do not sell
# [011] Answer: Check Next week. Could be trending up.
# [100] Answer: Do not sell
# [101] Answer: Do not sell
# [110] Answer: Check tomorrow. Could be trending down.
# [111] Anser: Think about selling