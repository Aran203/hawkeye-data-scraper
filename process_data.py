

def parse_trajectory_data(dat: str):
    ''' Dat is the value of a key value pair (key is trajectoryData)
        Function converts it to a dictionary for easy access of attributes '''
    
    if not dat:
        return {}

    arr = dat.split("\n\n")
    arr = [i.strip().split("\n") for i in arr]
    arr = [[i[0][1:-1], i[1]] for i in arr]
    myDict = {i[0]: i[1] for i in arr}
    del myDict["Software Version"]
    return myDict

def fill_batbowl_data(row, matchData):
    BatBowlData = []
    
    try:
        batData = matchData['battingTeam']['batsman']
        bowlData = matchData['bowlingTeam']['bowler']
    except:
        return [''] * 8

    if (batData['isRightHanded']):
        batHand = "RHB"
    else:
        batHand = "LHB"
    
    if (matchData['delivery']['deliveryType'] == "Seam"):
        bowlType = "pace"
    else:
        bowlType = "spin"
    
    batTeam = matchData['battingTeam']['name'].title()
    bowlTeam = matchData['bowlingTeam']['name'].title()

    if "Bangalore" in batTeam:
        batTeamArr = batTeam.split("-")
        batTeamArr.append(batTeamArr.pop(0))
        batTeam = "-".join(batTeamArr)
    
    if "Bangalore" in bowlTeam:
        bowlTeamArr = bowlTeam.split("-")
        bowlTeamArr.append(bowlTeamArr.pop(0))
        bowlTeam = "-".join(bowlTeamArr)

    
    bowlStyle = row['bowl_style'].values[0]
    batID = row['p_bat'].values[0]
    bowlID = row['p_bowl'].values[0]


    batArr = [batData['name'].title(), batID, batHand, batTeam]
    bowlArr = [bowlData['name'].title(), bowlID, bowlStyle, bowlType, bowlTeam]

    BatBowlData += batArr + bowlArr

    return BatBowlData

def fill_trajectory_data(ball_data, delivery_data, trajectory_dict):
    ''' 
    Extracts features related to the trajectory of the delivery - coords of releasing, bouncing, crease & stump interception etc
    '''

    trajectory_data = delivery_data['trajectory']

    release_data = trajectory_data['releasePosition']
    crease_pos = trajectory_data['creasePosition']
    stump_pos = trajectory_data['stumpPosition']
    impact_pos = trajectory_data['impactPosition']
        

    ball_data_traj = {'release_speed': trajectory_data['releaseSpeed'], 'initial_angle': trajectory_data['initialAngle'], 
                      'release_x': release_data['x'], 'release_y': release_data['y'], "release_z" : release_data['z'],
                      'bounce_angle': trajectory_data['bounceAngle'], 
                      'bounce_x': trajectory_data['bouncePosition']['x'], 'bounce_y': trajectory_data['bouncePosition']['y'], 
                      'crease_x': crease_pos['x'], 'crease_y' : crease_pos['y'],
                      'crease_z' : crease_pos['z'], 'drop_angle' : trajectory_data['dropAngle'], 
                      'impact_x': impact_pos['x'], 'impact_y' : impact_pos['y'], 'impact_z' : impact_pos['z'], 
                      'stump_x' : stump_pos['x'], 'stump_y' : stump_pos['y'], 'stump_z' : stump_pos['z'],
                      'swing' : trajectory_data['swing'], 'deviation' : trajectory_data['deviation'],
                      'swing_dist' : trajectory_dict.get('Swing Distance (m)', -1.0), 'six_dist' : trajectory_dict.get('Distance Of Six (m)', -1.0),
                      }
    
    if trajectory_dict:
        pre_bounce_acc = trajectory_dict['Acceleration'].split()
        post_bounce_acc = trajectory_dict['Post Bounce Acceleration'].split()
        pre_bounce_vel = trajectory_dict['Pre Bounce Velocity'].split()
        post_bounce_vel = trajectory_dict['Post Bounce Velocity'].split()

        motion_data = {
                        'pre_bounce_ax': float(pre_bounce_acc[0]), 'pre_bounce_ay' : float(pre_bounce_acc[1]), 'pre_bounce_az' : float(pre_bounce_acc[2]),
                        'post_bounce_ax' : float(post_bounce_acc[0]), 'post_bounce_ay' : float(post_bounce_acc[1]), 'post_bounce_az' : float(post_bounce_acc[2]),
                        'pre_bounce_vx' : float(pre_bounce_vel[0]), 'pre_bounce_vy' : float(pre_bounce_vel[1]), 'pre_bounce_vz' : float(pre_bounce_vel[2]),
                        'post_bounce_vx' : float(post_bounce_vel[0]), 'post_bounce_vy' : float(post_bounce_vel[1]), 'post_bounce_vz' : float(post_bounce_vel[1])
                  
                    }
        
        ball_data.update(motion_data)
        
    


    ball_data.update(ball_data_traj)


def validateData(extracted_data, validation_criteria):

    if extracted_data[2] != validation_criteria[2] or extracted_data[6] != validation_criteria[6]:
        extracted_data[2] = validation_criteria[2]
        extracted_data[6] = validation_criteria[6]
        return True
    
    return False
    
def processData(ball_data, response):

    match_data = response['match']
    delivery_data = response['match']['delivery']
    trajectory_dict = parse_trajectory_data(match_data['delivery']['trajectory']['trajectoryData'])

    # Extracting ground and date data
    ground = match_data["name"].split("_")[4]
    ball_data['ground'] = ground

    if trajectory_dict:
        date = ("-").join(trajectory_dict['Delivery Time and Date'].split()[0].split("/"))[1:]
    else:
        date = -1.0

    ball_data['date'] = date


    batTeam = match_data['battingTeam']['name'].title()
    bowlTeam = match_data['bowlingTeam']['name'].title()

    if "Bangalore" in batTeam:
        batTeamArr = batTeam.split("-")
        batTeamArr.append(batTeamArr.pop(0))
        batTeam = "-".join(batTeamArr)
    
    if "Bangalore" in bowlTeam:
        bowlTeamArr = bowlTeam.split("-")
        bowlTeamArr.append(bowlTeamArr.pop(0))
        bowlTeam = "-".join(bowlTeamArr)

    ball_data['team_bat'] = batTeam
    ball_data['team_bowl'] = bowlTeam



    # fill_batbowl_data(ball_data_check, matchData)
    fill_trajectory_data(ball_data, delivery_data, trajectory_dict)

    