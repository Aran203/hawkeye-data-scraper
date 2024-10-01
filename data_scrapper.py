import requests
import pandas as pd
import numpy as np
from main import FIELDS

BASE_URL = "https://polls.iplt20.com/widget/welcome/get_data"

def fetch_bbb_data(inning, over, ball, hawkID):
    url = f"{BASE_URL}?path=Delivery_{inning}_{over}_{ball}_{hawkID}.json"

    try:
        response = requests.get(url, timeout = 100)
        data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    if not data:
        return None
    
    return data

def fill_non_hawkeye_data(ball_data: dict, ball_data_check: pd.DataFrame):
    '''
        Fills non hawkeye data attributes for the ball
    '''

    non_hawkeye_attr = FIELDS[ : FIELDS.index('control') + 1]
    
    for attribute in non_hawkeye_attr:
        
        if attribute == "bowl_type":
            ball_data[attribute] = ball_data_check["bowl_kind"].values[0].split()[0]
        elif attribute == "ground":
            ground = ball_data_check.iloc[0]['ground']
            ball_data[attribute] = "-".join(ground.replace(",", " ").split()).upper()
        elif attribute == "team_bat":
            team_bat = ball_data_check.iloc[0]['team_bat']
            ball_data[attribute] = "-".join(team_bat.split())
        elif attribute == "team_bowl":
            team_bowl = ball_data_check.iloc[0]['team_bowl']
            ball_data[attribute] = "-".join(team_bowl.split())
        else:
            ball_data[attribute] = ball_data_check[attribute].values[0]
        

    


