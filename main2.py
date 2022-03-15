import requests

def get_data(symbol):

    # url = "https://finage-currency-data-feed.p.rapidapi.com/last"
    url = "https://api.finage.co.uk/history/stock/open-close?stock=AAPL&date=2021-02-03&apikey=API_KEY40P8BNOQNI6R81C73VG1VM7M7KDQ43HE"

    # querystring = {"currencies":"USDGBP","apikey":"API_KEYUX0RG2F4BXCV5JJ50P0K3BLFQOS0Q0DP"}

    # headers = {
    #     'x-rapidapi-host': "finage-currency-data-feed.p.rapidapi.com",
    #     'x-rapidapi-key': ""
    #     }

    # response = requests.request("GET", url, headers=headers, params=querystring)
    response = requests.request("GET", url)

    print(response.text)

if __name__ == "__main__":
  get_data("API")