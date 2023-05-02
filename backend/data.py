import pandas as pd
import numpy as np
from os.path import expanduser as ospath

#the method that does EVERYTHING ----------------------------------------------------------------------------------------
#returns a prob trans matrix
def genProbMatrix(path):
    
    #gets csv and formats
    data = pd.read_csv(ospath(path))
    #data = pd.read_csv(ospath('~/Desktop/Capstone Project/STS2007.csv'))
    #data.info()

    data[1:76]

    df = pd.DataFrame(data=data[0:54])
    df.columns = df.iloc[0]
    ndf = df.drop([0,1], axis="index")


    ndf = ndf.loc[:, ndf.columns.notna()]
    ndf = ndf.drop(['District of Columbia ', "Puerto Rico"], axis=1)
    ndf = ndf.drop([10, 41], axis=0)

    #print(ndf)
    
#block 2: calculates sum of all movement for each column----------------------------------------------------------------------------------------
    popstuff = 0
    totals = {}
    
    cols = 0
    
    for state in ndf.columns.tolist():
        if state == "butts":
            continue
        cols = cols+1
        for i in range(2,53):
            if i == 10:
                continue
            if i == 41:
                continue
            thing = ndf[state].loc[i].replace(",","")
            #print (thing)
            popstuff = popstuff + int(thing)
        totals[state] = popstuff
        popstuff = 0
    #print(cols)

    #print(totals)
    print()
    
#block 3: compiles probabilities for movement between states----------------------------------------------------------------------------------------
    prob1 = 0        

    temprobs = []
    actprobs = []

    for state in ndf.columns.tolist():
        if state == "butts":
            continue
        for i in range(2,54):
            if i == 10:
                continue
            if i == 41:
                continue
            thing = ndf[state].loc[i].replace(",","")
            #print (thing)
            prob = int(thing)/(totals[state])
            temprobs.append(prob)
            prob1 = prob1 + prob
        #print(prob1)
        prob1 = 0        
        actprobs.append(temprobs)
        temprobs = []
    
    #block 4: creates matrix
    name = np.matrix(actprobs)
    return name

#Rows: CURRENT, Cols: FUTURE
def main():
    norm = genProbMatrix('backend/STS2007copy.csv')
    #print(norm)
    #print(norm[17,17]) #Lou,Lou
    #print(norm[0,17])
    #print(norm[:,17]) # : does cols
    #print()

    katrina = genProbMatrix('backend/STS2006copy.csv')
    #print(katrina)
    #print(katrina[0,17])
    #print(ndf.columns.tolist())

    #print(data)
    #print (data['Moved from:'].loc[1])

    #popstuff = 0

    #for i in range(0,5):
        #print (data['Alabama'].loc[i])
        #popstuff = popstuff + data['Alabama'].loc[i]
        
    #print(popstuff)

#creating norm year matrices: 1, 5 and 10----------------------------------------------------------------------------------------

    def getGood1(state): 
        return norm[state]

    futuregoodstate1yr = getGood1(17)

    def getGood5(state): 
        futuregood2 = np.matmul(norm,norm)
        futuregood3 = np.matmul(futuregood2,norm)
        futuregood4 = np.matmul(futuregood3,norm)
        return futuregood4[state]

    futuregoodstate5yr = getGood5(17)
    
    def getGood10(state): 
        futuregood2 = np.matmul(norm,norm)
        futuregood3 = np.matmul(futuregood2,norm)
        futuregood4 = np.matmul(futuregood3,norm)
        futuregood5 = np.matmul(futuregood4,norm)
        futuregood6 = np.matmul(futuregood5,norm)
        futuregood7 = np.matmul(futuregood6,norm)
        futuregood8 = np.matmul(futuregood7,norm)
        futuregood9 = np.matmul(futuregood8,norm)
        return futuregood9[state]

    futuregoodstate10yr = getGood10(17)

#creating severe year matrices: 1, 5, and 10----------------------------------------------------------------------------------------

    def getBad1(state):
        return katrina[state]
    #Lou=17 to Lou=17
    futurebadstate1yr = getBad1(17)

    def getBad5(state):
        futurebad2 = np.matmul(katrina,katrina)
        futurebad3 = np.matmul(futurebad2,katrina)
        futurebad4 = np.matmul(futurebad3,katrina)
        return futurebad4[state]
    #Lou=17 to Lou=17
    futurebadstate5yr = getBad5(17)
    #futurebadstate5yr = np.reshape(futurebadstate5yr,-1)
   
    def getBad10(state):
        futurebad2 = np.matmul(katrina,katrina)
        futurebad3 = np.matmul(futurebad2,katrina)
        futurebad4 = np.matmul(futurebad3,katrina)
        futurebad5 = np.matmul(futurebad4,katrina)
        futurebad6 = np.matmul(futurebad5,katrina)
        futurebad7 = np.matmul(futurebad6,katrina)
        futurebad8 = np.matmul(futurebad7,katrina)
        futurebad9 = np.matmul(futurebad8,katrina)
        return futurebad9[state]
    #Lou=17 to Lou=17

    futurebadstate10yr = getBad10(17)


    #creating dictionaries for years-----------------------------------------------------------------------------------------------------
    stateNames = ["Alabama", "Alaska", "Arizona", "Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin", "Wyoming"]

    oneyearDict = {}
    fiveyearDict = {}
    tenyearDict = {}
    finalDict = {}

    for x in range(len(stateNames)):
        
        oneyearDict[stateNames[x]] = {
            "norm" : futuregoodstate1yr[0,x],
            "severe" : futurebadstate1yr[0,x]
        }

        fiveyearDict[stateNames[x]] = {
            "norm" : futuregoodstate5yr[0,x],
            "severe" : futurebadstate5yr[0,x]
        }

        tenyearDict[stateNames[x]] = {
            "norm" : futuregoodstate10yr[0,x],
            "severe" : futurebadstate10yr[0,x]
        }

    finalDict["oneyear"]= oneyearDict
    finalDict["fiveyear"]= fiveyearDict
    finalDict["tenyear"]= tenyearDict

    return(finalDict)



def formatData():
    stateNames = ["Alabama", "Alaska", "Arizona", "Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin", "Wyoming"]

    oneyearDict = {}
    for x in stateNames:
        oneyearDict 




