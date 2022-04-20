import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.api_classes import HistoryApiConfig, HistoryResponse


class Stock:
  def __init__(self, csvRow):
    self.name = csvRow[0]
    self.price = csvRow[1]

class Advice:
  def __init__(self, historyResponse: HistoryResponse, stock: Stock, averageFiveDaysAgo, diff, finalDecision):
    self.historyResponse = historyResponse
    self.stock = stock
    self.averageFiveDaysAgo = averageFiveDaysAgo
    self.diff = diff
    self.finalDecision = finalDecision

  def returnDecision(self):
    return(f"\nFor {self.stock.name}\n"
        f"Buying price was: {self.stock.price}\n"
        f"High for 5 days ago is : {str(self.historyResponse.high)}\n"
        f"Low for 5 days ago is : {str(self.historyResponse.low)}\n"
        f"Average of the two is : {str(self.averageFiveDaysAgo)}\n"
        f"Diff is : {str(self.diff)}\n"
        f"{self.finalDecision}\n")