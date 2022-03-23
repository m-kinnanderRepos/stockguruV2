class Stock:
  def __init__(self, csvRow):
    self.name = csvRow[0]
    self.price = csvRow[1]