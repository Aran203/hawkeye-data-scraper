import requests
import json
import csv

BASE_URL = "https://polls.iplt20.com/widget/welcome/get_data"

def fetch_bbb_data(inning, over, ball, hawkID, matchID):
    url = f"{BASE_URL}?path=Delivery_{inning}_{over}_{ball}_{hawkID}.json"

    try:
        response = requests.get(url)
        data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    if not data:
        return []
    
    return data

    


