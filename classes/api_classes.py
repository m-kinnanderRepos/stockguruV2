class HistoryResponse:
  def __init__(self, jsonLoads):
    self.high = jsonLoads["high"]
    self.low = jsonLoads["low"]


class HistoryApiConfig: 
  def __init__(self, configFile):
    self.key = configFile["API"]["KEY"]
    self.daysAgo = configFile["API"]["DAYSAGO"]
    self.historyApiUrl = configFile["API"]["HISTORY_APIURL"]

