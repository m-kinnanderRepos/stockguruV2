import requests

url = "https://finage-currency-data-feed.p.rapidapi.com/last/stock/"

querystring = {"currencies":"USDGBP","apikey":"API_KEYUX0RG2F4BXCV5JJ50P0K3BLFQOS0Q0DP"}

headers = {
    'x-rapidapi-host': "finage-currency-data-feed.p.rapidapi.com",
    'x-rapidapi-key': ""
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)