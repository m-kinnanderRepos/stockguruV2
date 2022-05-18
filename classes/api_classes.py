class HistoryResponse:
  def __init__(self, jsonLoads):
    self.high = jsonLoads["high"]
    self.low = jsonLoads["low"]


class HistoryApiConfig: 
  def __init__(self, configFile):
    self.key = configFile["API"]["KEY"]
    self.daysAgoFive = configFile["API"]["DAYSAGOFIVE"]
    self.historyApiUrl = configFile["API"]["HISTORY_APIURL"]
    self.daysAgoTwentyOne = configFile["API"]["DAYSAGOTWENTYONE"]
    self.daysAgoThirty = configFile["API"]["DAYSAGOTHIRTY"]

