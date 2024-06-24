

def parseTrajectoryData(dat: str):
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

def extractBatBowlData(row, matchID, inning, ballID, matchData):
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

def extractTrajectoryData(deliveryData, trajectoryDict):
    ''' Extracts features related to the trajectory of the delivery - coords of releasing, bouncing, crease & stump interception etc'''
    trajectoryData = []

    allData = deliveryData['trajectory']

    releaseData = [allData['releaseSpeed'], allData['initialAngle']] + [allData['releasePosition'][i] for i in allData['releasePosition']]
    bounceData = [allData['bounceAngle'], allData['bouncePosition']['x'], allData['bouncePosition']['y']]
    creasePos = [allData['creasePosition']['x'], allData['creasePosition']['y'], allData['creasePosition']['z']]
    stumpPos = [allData['stumpPosition']['x'], allData['stumpPosition']['y'], allData['stumpPosition']['z']]
    impactPos = [allData['impactPosition']['x'], allData['impactPosition']['y'], allData['impactPosition']['z']]
    dropAngle = [allData['dropAngle']]
    deviationData = [allData['swing'], allData['deviation']]

    if trajectoryDict:
        deviationData += [float(trajectoryDict['Swing Distance (m)']), float(trajectoryDict['Distance Of Six (m)'])]
    else:
        deviationData += [-1.0, -1.0]

    trajectoryData += releaseData + bounceData + impactPos + creasePos + dropAngle + stumpPos + deviationData

    return trajectoryData

def validateData(extracted_data, validation_criteria):

    if extracted_data[2] != validation_criteria[2]:
        extracted_data[2] = validation_criteria[2]
    
    if extracted_data[6] != validation_criteria[6]:
        extracted_data[6] = validation_criteria[6]

    
def processData(row, data, matchID, inning):
    processedData = [matchID, inning]
    matchData = data['match']
    deliveryData = data['match']['delivery']
    trajectoryDict = parseTrajectoryData(matchData['delivery']['trajectory']['trajectoryData'])

    # Extracting ball ID, ground and date data
    ball_id = deliveryData['deliveryNumber']['over'] - 1 + deliveryData['deliveryNumber']['ball'] / 100
    ground = matchData["name"].split("_")[4]

    if trajectoryDict:
        date = ("-").join(trajectoryDict['Delivery Time and Date'].split()[0].split("/"))[1:]
    else:
        date = -1.0

    batBowlData = extractBatBowlData(row, matchID, inning, ball_id, matchData)
    trajectoryData = extractTrajectoryData(deliveryData, trajectoryDict)

    # Extracting extras info
    attrs = row.loc[:, ['out', 'dismissal', 'noball', 'wide', 'byes', 'legbyes']]
    extras = attrs.values.flatten().tolist()

    processedData += batBowlData + [ball_id, deliveryData['scoringInformation']['score']] + extras + trajectoryData + [ground, date]

    return processedData