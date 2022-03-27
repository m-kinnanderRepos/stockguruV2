from read import *
from stocks import *
          
if __name__ == "__main__":
    configFile: HistoryApiConfig = HistoryApiConfig(read_json("config-history_api.json"))
    listOfStocks: list = read_csv_to_list_of_Stocks("stocks.csv")
    
    data = get_data(listOfStocks, configFile)
    decisionMakingAdvice = stockDecisionMaking(data)
    for pieceOfAdvice in decisionMakingAdvice:
        printDecision(pieceOfAdvice)