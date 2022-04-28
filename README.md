# stockGuru

stockGuru is a program to help monitor your stocks.

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
    "DAYSAGO": 5,
    "HISTORY_APIURL": "https://api.finage.co.uk/history/stock/open-close"
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

or

```bash
python tests/test_stocks.py
```

## Notes

The `main` branch is for users to get started and can be used by anyone with the free subscription to the api from [Finage](https://finage.co.uk/#pricing). The `main` branch is based off of the free subscription because of the limitations the free subscription tier has (mainly 15 second delay between calls). It's also nice to not have to pay to try this project out. I have more logic I would like for decision making that I will eventually add into a branch based off of main.

## [Finage API documentation](https://finage.co.uk/docs/api/us-stock-historical-end-of-day-data)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

# Testing
