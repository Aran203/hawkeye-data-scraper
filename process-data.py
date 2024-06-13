

def processTrajectoryData(dat: str):
    ''' Dat is the value of a key value pair (key is trajectoryData)
        Function converts it to a dictionary for easy access of attributes '''
    
    arr = dat.split("\n\n")
    arr = [i.strip().split("\n") for i in arr]
    arr = [[i[0][1:-1], i[1]] for i in arr]
    myDict = {i[0]: i[1] for i in arr}
    del myDict["Software Version"]
    return myDict