import json
import csv
from classes.stock_classes import Stock


def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def read_csv_to_list_of_Stocks(file_path):
    listOfStocks: list[Stock] = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, skipinitialspace=True)
        for row in reader:
            # Should make sure type in each column is correct.
            listOfStocks.append(Stock(row))
    return listOfStocks