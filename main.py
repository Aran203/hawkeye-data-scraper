import csv
from data_scrapper import *
from process_data import *

FIELDS = ['p_match', 'inns', 'bat', 'p_bat', 'bat_hand', 'team_bat', 'bowl', 'p_bowl', 'bowl_type', 'team_bowl', 'ball_id', 'score', 
        #   'out' , 'noball', 'wides', 'byes', 'leg_byes', 
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
    fileDat_path = 'matches/ipl-2024.csv'
    hawkeye_ids, match_ids = read_match_ids(fileDat_path)

    with open(FILENAME, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = FIELDS) 
        writer.writeheader()

        for i in range(len(match_ids)):
            hawkID = hawkeye_ids[i]
            matchID = match_ids[i]