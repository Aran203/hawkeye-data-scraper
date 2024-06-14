

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

def extractBatBowlData(matchData):
    BatBowlData = []
    
    try:
        batData = matchData['battingTeam']['batsman']
        bowlData = matchData['bowlingTeam']['bowler']
    except:
        return ['NA'] * 8

    if (batData['isRightHanded']):
        batHand = "RHB"
    else:
        batHand = "LHB"

    if (bowlData['isRightHanded']):
        bowlHand = "RHB"
    else:
        bowlHand = "LHB"

    batArr = [batData['name'].title(), batData['id'].title(), batHand, matchData['battingTeam']['name']]
    bowlArr = [bowlData['name'].title(), bowlData['id'].title(), bowlHand, matchData['bowlingTeam']['name']]

    BatBowlData += batArr + bowlArr

    return BatBowlData

def extractTrajectoryData(deliveryData, trajectoryDict):
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


def processData(data, matchID, inning):
    processedData = [matchID, inning]
    matchData = data['match']
    deliveryData = data['match']['delivery']

    batBowlData = extractBatBowlData(matchData)
    trajectoryDict = parseTrajectoryData(matchData['delivery']['trajectory']['trajectoryData'])
    trajectoryData = extractTrajectoryData(deliveryData, trajectoryDict)

    ball_id = deliveryData['deliveryNumber']['over'] - 1 + deliveryData['deliveryNumber']['ball'] / 100
    ground = matchData["name"].split("_")[4]

    if trajectoryDict:
        date = ("-").join(trajectoryDict['Delivery Time and Date'].split()[0].split("/"))[1:]
    else:
        date = -1.0

    processedData += batBowlData + [ball_id, deliveryData['scoringInformation']['score']] + trajectoryData + [ground, date]

    return processedData