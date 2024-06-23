import requests
import json
import csv
from main import FIELDS

BASE_URL = "https://polls.iplt20.com/widget/welcome/get_data"
TRAJECTORY_FIELDS = len(FIELDS[19:-2])

def fetch_bbb_data(inning, over, ball, hawkID):
    url = f"{BASE_URL}?path=Delivery_{inning}_{over}_{ball}_{hawkID}.json"

    try:
        response = requests.get(url, timeout = 100)
        data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    if not data:
        return []
    
    return data

def fetch_bbb_data_csv(inning, over, ball, matchID, df):
    ball_id = int(over) - 1 + float(ball) / 100
    row = df.loc[(df['p_match'] == int(matchID)) & (df['ball_id'] == ball_id) & (df['inns'] == inning)]

    if not row.empty:
        rst = row.loc[:, ['p_match', 'inns', 'bat', 'p_bat', 'bat_hand', 'team_bat', 'bowl', 'p_bowl', 'bowl_style', 'bowl_kind', 'team_bowl', 'ball_id', 'score', 'out', 'dismissal', 'noball', 'wide', 'byes', 'legbyes', 'ground', 'date']]

        rst = rst.values[0].tolist()
        rst[9] = rst[9].split()[0]
        rst[-2] = "-".join(rst[-2].replace(",", " ").split())
        rst[5] = "-".join(rst[5].split())
        rst[10] = "-".join(rst[10].split())

        rst[19:19] = [''] * TRAJECTORY_FIELDS

        return (True, rst)
    else:
        return (False, [])

    pass

    


