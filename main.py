import csv
from data_scrapper import *
from process_data import *
import numpy as np
import pandas as pd

FIELDS = ['p_match', 'inns', 'bat', 'p_bat', 'bat_hand', 'team_bat', 'bowl', 'p_bowl', 'bowl_style', 'bowl_type', 'team_bowl', 
          'ball_id', 'score', 'batruns', 'out' , 'dismissal', 'noball', 'wide', 'byes', 'legbyes', 'cur_bat_runs', 'cur_bat_bf', 'cur_bowl_ovr', 
          'cur_bowl_wkts', 'cur_bowl_runs', 'inns_runs', 'inns_wkts', 'inns_rr', 'inns_rrr', 'target', 'max_balls', 'wagonZone', 'shot', 
          'control',

          'release_speed', 'initial_angle', 'release_x', 'release_y', 'release_z', 'pre_bounce_ax', 'pre_bounce_ay', 'pre_bounce_az', 
          'pre_bounce_vx', 'pre_bounce_vy', 'pre_bounce_vz', 'bounce_angle', 'bounce_x', 'bounce_y', 'post_bounce_ax', 'post_bounce_ay',
          'post_bounce_az', 'post_bounce_vx', 'post_bounce_vy', 'post_bounce_vz', 'impact_x', 'impact_y', 'impact_z', 'crease_x', 
          'crease_y', 'crease_z', 'drop_angle', 'stump_x', 'stump_y', 'stump_z', 'swing', 'deviation', 'swing_dist', 'six_dist', 
          'ground', 'date', 'season']

OUT_FILENAME = "data/ipl-hawkeye-data.csv"

def read_match_ids(path):
    hawkeye_ids = []
    match_ids = []
    seasons = []

    # Reading all match IDs from the csv file
    with open(path, mode = 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            hawkeye_ids.append(row[0].strip())
            match_ids.append(row[1].strip())
            seasons.append(row[2].strip())

    return hawkeye_ids, match_ids, seasons


def main():
    # Reading t20bbb for validation since we don't know the max number of balls (extras + legal balls) in an over 
    t20bbb = pd.read_csv("t20bbb.csv", dtype = {'line': str, 'length': str, 'shot': str})
    MATCH_INFO_FILENAME = 'matches/hawkeye-keydata.csv'
    hawkeye_ids, match_ids, seasons = read_match_ids(MATCH_INFO_FILENAME)
    
    ball_data_all = []

    # iterate over the matches
    for i in range(10):
        hawkID = hawkeye_ids[i]
        matchID = match_ids[i]
        season = seasons[i]
        count = 0

        for inning in range(1, 3):
            for over in range(1, 21):
                ball = 1

                while True:
                    # initialize ball_data dictionary to add values for keys for FIELDS above
                    ball_data = {key: np.nan for key in FIELDS}
                    ball_data['season'] = seasons[i]

                    # fetch data from api and data from 2nd dataset for checking attributes
                    data = fetch_bbb_data(inning, over, ball, hawkID)
                    ball_id = int(over) - 1 + float(ball) / 100
                    ball_data_checks = t20bbb.loc[(t20bbb['p_match'] == int(matchID)) & (t20bbb['ball_id'] == ball_id) & (t20bbb['inns'] == inning)]


                    # no data fetched
                    if not data:
                        # either no data OR api is not available for that delivery (imputation)
                        if ball_data_checks.empty:
                            break
                        else:
                            # Fill attributes not associated with hawkeye
                            fill_non_hawkeye_data(ball_data, ball_data_checks)
                            print(f'IMPUTATION DONE - {matchID} {inning} {over} {ball}')
                    else:
                        # Fill non hawkeye and hawkeye attributes
                        fill_non_hawkeye_data(ball_data, ball_data_checks)
                        processData(ball_data, data)


                    ball_data_all.append(ball_data)

                    ball += 1
                    count += 1
                
        print(f'{matchID} {count} done')


    hawkeye_data = pd.DataFrame(ball_data_all)
    hawkeye_data.to_csv(OUT_FILENAME, index = False)




if __name__ == "__main__":
    main()
