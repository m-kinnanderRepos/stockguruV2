Run this project in its own virtual environment. Look into venv or pyenv.

You need to pip install requests.

You will need to create a config-history_api.json file with following key and insert your values:
`{ "API": { "KEY": "Your_API_key", "DAYSAGO": 5 } }`

You will also need to create a file called stocks.csv. This exists of a tab dilimitter pair exisitng of the name of a stock
and the price at which you purchased it at. (Right now I have the free version of the api end point. You can only make
one request per 15 seconds. You should only have one row in the csv file.)

Running project:

- In a terminal run `python main.py`
