import requests
import json


def get_token_data():
    token_list_url = "https://raw.githubusercontent.com/gnosis/dex-js/master/src/tokenList.json"
    r = requests.get(token_list_url)
    return r.json()
