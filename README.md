# stockGuruV2

stockGuruV2 is a program to help monitor your stocks.

## Installation

Run this project in its own virtual environment. Look into venv or pyenv.

You need to pip install requests.

```bash
pip install -r requirements.txt
```

## Creation

You will need to create a config-history_api.json file in root directory with following keys and insert your values:

```json
{
  "API": {
    "KEY": "Your_API_key",
    "DAYSAGOFOURTEEN": 14,
    "DAYSAGOTWENTYEIGHT": 28,
    "HISTORY_APIURL": "https://api.finage.co.uk/history/stock/open-close",
    "LASTQUOTE_APIURL": "https://api.finage.co.uk/last/stock/"
  }
}
```

You will also need to create a file called stocks.csv in root directory. This consists of a tab dilimitter pair exisitng of: the name of a stock and the price at which you purchased it at. (Right now I have the free version of the api end point. You can only make one request per 15 seconds. You should only have one row in the csv file.)

## Running project

- In a terminal run

```bash
python main.py
```

## Running tests

- In a terminal run

```bash
python tests/test_read.py
```

or to run all tests

```bash
python3 -m unittest discover -v
```

## Notes

The `main` branch is for users to get started and can be used by users with a paid subscription to the api from [Finage](https://finage.co.uk/#pricing). Visit [stockGuru](https://github.com/m-kinnanderRepos/stockguru) if you only have a free subscription. This application uses the advatages the paid subscription offers. For every stock, the application retreives historical data from 28 days ago and 14 days ago. It also retreives data for today's asking price. Using the data from these three api calls, the application calculates advice on what to do with the stock.

## [Finage API documentation historical data](https://finage.co.uk/docs/api/us-stock-historical-end-of-day-data)

## [Finage API documentation last quote data](https://finage.co.uk/docs/api/stock-last-quote)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
