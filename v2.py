import json
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import unirest
from matplotlib import rcParams




RAPIDAPI_KEY  = "4b76ce3031mshc0abcd2f11a8749p10bb4cjsn1571e685dddf" 
RAPIDAPI_HOST = "yh-finance.p.rapidapi.com"
symbol_string = ""
# headers = {'Content-Type': 'application/json',
#            'Authorization': 'Bearer {0}'.format(api_token)}


def get_ssh_keys(symbol):
  
    # api_url = '{0}account/keys'.format(api_url_base)

    response = requests.get("https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts?region=US&lang=en&symbol=" + symbol + "&interval=1d&range=3mo",
      headers={
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "Content-Type": "application/json"
      }
     )
    print(response)
    print(response.content)
    print(response.__dict__)
    if response.ok:
      print ('OK!')
    else:
      print ('Boo!')
          
if __name__ == "__main__":
  get_ssh_keys("API")


