import requests
import json
from datetime import date, timedelta
import sys
import csv





def get_data(listOfStocks, config):
  
  today = date.today()
  fiveDaysAgo = today - timedelta(days=config["API"]["DAYSAGO"])
  url = "https://api.finage.co.uk/history/stock/open-close"
  for row in listOfStocks:
    querystringFiveDaysAgo = {"stock":row[0],"date":fiveDaysAgo.strftime("%Y-%m-%d"),"apikey":config["API"]["KEY"]}
    response = requests.request("GET", url, params=querystringFiveDaysAgo)

    print(response)

    if(response.status_code == 200):
        array = json.loads(response.text)
        print("For " + row[0] + " high for 5 days ago is : " + str(array["high"]))
        print("For " + row[0] + " low for 5 days ago is : " + str(array["low"]))

        averageFiveDaysAgo = (array["high"] + array["low"]) / 2
        print("For " + row[0] + " Average of the two is : " + str(averageFiveDaysAgo))

        diff = float(row[1]) / averageFiveDaysAgo
        print("For " + row[0] + " diff is : " + str(diff))
        percent = 0
        if(diff < 1):
            percent = diff * 100
        
            if(percent > 46):
                print("For " + row[0] + " greater than 46 percent")

            else:
                print("For " + row[0] + "l ess than 46 percent")
        
        else:
            print("For " + row[0] + " price is less than buy price")

    else:
        print("Error in call to api.")

    
  # print(array)
  # print(array["low"])

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def read_csv(file_path):
    stockList = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, skipinitialspace=True)
        for row in reader:
            stockList.append(row)
    return stockList

          
if __name__ == "__main__":
    configFile = read_json("config.json")
    listOfStocks = read_csv("stocks.csv")
    # # for row in listOfStocks:
    # #     print(row)
    # # print(listOfStocks[0][1])
    # stockSymbol = input("Enter stock symbol: ")
    # print("Stock symbol is " + stockSymbol)
    # price = float(input("Enter buy price: "))
    # print("Buy price is " + str(price))
    get_data(listOfStocks, configFile)
    # # print(configFile["API"]["KEY"])
    
    