import requests
import json
import csv

# Reading all match IDs from the csv file
with open('matches/ipl-2024.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    header = next(reader)
    hawkeye_ids = [row[0].strip() for row in reader]
    match_ids = [row[1].strip() for row in reader]

def processTrajectoryData(dat: str):
    ''' 
        Dat is the value of a key value pair (key is trajectoryData)
        Function converts it to a dictionary for easy access of attributes
    '''
    arr = dat.split("\n\n")
    arr = [i.strip().split("\n") for i in arr]
    arr = [[i[0][1:-1], i[1]] for i in arr]
    myDict = {i[0]: i[1] for i in arr}
    del myDict["Software Version"]
    return myDict


fields = ['p_match', 'inns', 'bat', 'p_bat', 'bat_hand', 'team_bat', 'bowl', 'p_bowl', 'bowl_type', 'team_bowl', 'ball_id', 'score', 
          'noball', 'wides', 'byes', 'leg_byes', 'six_dist', 'release_speed', 'release_x', 'release_y', 'release_z', 'bounce_angle', 
          'bounce_x', 'bounce_y', 'crease_x', 'crease_y', 'crease_z', 'drop_angle', 'impact_x', 'impact_y', 'impact_z', 'swing', 
          'deviation', 'swing_dist', 'ground', 'date']

