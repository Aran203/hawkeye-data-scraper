import csv
from data_scrapper import *
from process_data import *
import numpy as np
import pandas as pd

FIELDS = ['p_match', 'inns', 'bat', 'p_bat', 'bat_hand', 'team_bat', 'bowl', 'p_bowl', 'bowl_style', 'bowl_type', 'team_bowl', 'ball_id', 'score', 
          'out' , 'dismissal', 'noball', 'wides', 'byes', 'leg_byes', 
          'release_speed', 'initial_angle', 'release_x', 'release_y', 'release_z', 'bounce_angle', 'bounce_x', 'bounce_y', 
          'impact_x', 'impact_y', 'impact_z', 'crease_x', 'crease_y', 'crease_z', 'drop_angle', 'stump_x', 'stump_y', 'stump_z',
          'swing', 'deviation', 'swing_dist', 'six_dist', 'ground', 'date']

FILENAME = "data/ipl-2024.csv"

def read_match_ids(path):
    hawkeye_ids = []
    match_ids = []

    # Reading all match IDs from the csv file
    with open(path, mode = 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            hawkeye_ids.append(row[0].strip())
            match_ids.append(row[1].strip())

    return hawkeye_ids, match_ids


def main():
    df = pd.read_csv("t20bbb.csv", dtype = {'line': str, 'length': str, 'shot': str})
    fileDat_path = 'matches/ipl-2024.csv'
    hawkeye_ids, match_ids = read_match_ids(fileDat_path)

    with open(FILENAME, 'a', newline = "") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(FIELDS)

        for i in range(6, 8):
            hawkID = hawkeye_ids[i]
            matchID = match_ids[i]

            for inning in range(1, 3):
                for over in range(1, 21):
                    ball = 1

                    while True:
                        data = fetch_bbb_data(inning, over, ball, hawkID)
                        
                        # No data fetched
                        if not data:
                            result = fetch_bbb_data_csv(inning, over, ball, matchID, df)
                            if result[0]:
                                print(f'{matchID} \t {inning}-{over}-{ball}')
                                writer.writerow(result[1])
                            else:
                                break

                        else:        
                            processedData = processData(df, data, matchID, inning)
                            writer.writerow(processedData)

                        ball += 1
                    
            print(f'{matchID} done')


if __name__ == "__main__":
    main()
