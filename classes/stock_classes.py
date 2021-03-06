import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.api_classes import HistoryApiConfig, HistoryResponse


class Stock:
  def __init__(self, csvRow):
    self.name = csvRow[0]
    self.price = csvRow[1]

class Advice:
  def __init__(self, currentAsk, averageFourteenDaysAgo, averageTwentyEightDaysAgo, stock: Stock, finalDecision):
    self.currentAsk = currentAsk
    self.averageFourteenDaysAgo = averageFourteenDaysAgo
    self.averageTwentyEightDaysAgo = averageTwentyEightDaysAgo
    self.stock = stock
    self.finalDecision = finalDecision

  def returnDecisionAsString(self):
    return(f"\nFor {self.stock.name} - {self.finalDecision}\n")