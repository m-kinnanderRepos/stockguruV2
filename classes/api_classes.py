class HistoryResponse:
  def __init__(self, jsonLoads):
    self.high = jsonLoads["high"]
    self.low = jsonLoads["low"]


class HistoryApiConfig: 
  def __init__(self, configFile):
    self.key = configFile["API"]["KEY"]
    self.daysAgoFourteen = configFile["API"]["DAYSAGOFOURTEEN"]
    self.historyApiUrl = configFile["API"]["HISTORY_APIURL"]
    self.daysAgoTwentyEight = configFile["API"]["DAYSAGOTWENTYEIGHT"]

class LastQuoteResponse:
  def __init__(self, jsonLoads):
    self.ask = jsonLoads["ask"]
    self.bid = jsonLoads["bid"]