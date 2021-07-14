#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 18:22:22 2021

@author: nickdifiore
"""
import random
import math
from matplotlib import pyplot as plt
import numpy as np

listOfLists = []
with open('QB_Dataset.txt','r') as f:
    for line in f:
        lineOfData = line.split('\t')
        listOfLists.append(lineOfData)



class Quarterback:
    
    def __init__ (self, name, pct, YPA, qbRate, YPG):
        self.name = name
        self.pct = pct
        self.YPA = YPA
        self.qbRate = qbRate
        self.YPG = YPG
        
    def __str__ (self):
        
        return "\nName: " + self.name + "\nCompletion PCT: " + self.pct + "\nYards per Attempt: " + self.YPA + "\nQB Rating: " + self.qbRate + "\nYards per Game: " + self.YPG 
    

# creates dictionary of all Quarterback objects

players = {}      

for line in listOfLists:
    QB1 = Quarterback(line[0],line[1],line[2],line[3],line[4])
    players[line[0]] = QB1
    
# creates lists for each individual statistic

playerName = []
pct = []
YPA = []
qbRate = []
YPG = []

for QBName in players.keys():
    playerName.append(players[QBName].name)
    pct.append(players[QBName].pct)
    YPA.append(players[QBName].YPA)
    qbRate.append(players[QBName].qbRate)
    YPG.append(players[QBName].YPG)

# deletes header values and transforms all statistics into float values
 
allStats = [pct, YPA, qbRate, YPG]
for l in allStats:
    l.pop(0)
    for i in range(0, len(l)):
        try:
            l[i] = float(l[i])
        except:
            print(l[i])

playerName.pop(0)

# creates average values for all statistics
avg_pct = sum(pct)/len(pct)
avg_YPA = sum(YPA)/len(YPA)
#avg_qbRate = sum(qbRate)/len(qbRate)
avg_YPG = sum(YPG)/len(YPG)

SD_pct = np.std(pct)
SD_YPA = np.std(YPA)
#SD_qbRate = np.std(qbRate)
SD_YPG = np.std(YPG)


"""*******************************************

            Plot Points

*******************************************"""

# creates initials of player names for plotting purposes

playerInitials = []

for name in playerName:
    full = name.split(' ')
    first = full[0]
    last = full[1]
    theInitials = first[0] + last[0]
    playerInitials.append(last)
    
'''
plt.plot(YPA, pct,'o')
plt.xlabel('YPA')
plt.ylabel('Completion PCT')
for i in range(len(playerName)):
    plt.annotate(playerInitials[i],(YPA[i],pct[i]))
'''




"""*******************************************

            DBSCAN Algorithm
            
*******************************************"""

# PARAMETERS

n = 0.7
minPts = 4

distances = []
clusters = []
noises = []

corePoints = []
nonCorePoints = []
borderPoints = []
noisePoints = []

visitedPoints = []

noise = False

# will use this list when calling the clustering function    
r = list(range(35))
random.shuffle(r)

namesAndRandomNums = {}

for i in range(0,35):
    namesAndRandomNums[playerName[i]] = r[i]
    




def removeVisitedElement(l_arg, index):
    new_list = l_arg
    new_list.pop(index)
    return new_list


    
def isCore(l_players, dict_Players):
    
    numNeighbors = 0
    thePlayer = random.choice(l_players)
    distances = []
    l_zYPA = []
    l_zPct = []
    
    for comparePlayer in l_players:
        
        zYPA_thePlayer = (float(dict_Players[thePlayer].YPA) - avg_YPA)/SD_YPA
        zYPA_comparePlayer = (float(dict_Players[comparePlayer].YPA) - avg_YPA)/SD_YPA 
        l_zYPA.append(zYPA_comparePlayer)     
               
        zPct_thePlayer = (float(dict_Players[thePlayer].pct) - avg_pct)/SD_pct
        zPct_comparePlayer = (float(dict_Players[comparePlayer].pct) - avg_pct)/SD_pct
        l_zPct.append(zPct_comparePlayer)
        
        dist = math.sqrt(((zYPA_thePlayer - zYPA_comparePlayer)**2) + (zPct_thePlayer - zPct_comparePlayer)**2)
        
        '''dist = math.sqrt(((float(dict_Players[thePlayer].YPA)\
                           - float(dict_Players[comparePlayer].YPA))/avg_YPA)**2\
    + ((float(dict_Players[thePlayer].pct)\
        - float(dict_Players[comparePlayer].pct))/avg_pct)**2)'''
    
        distances.append(dist)
        if (dist <= n) and (dist != 0):
            numNeighbors += 1
            
    visitedPoints.append(l_players.index(thePlayer)) 
    
    l_notVisited = removeVisitedElement(l_players,l_players.index(thePlayer))
    
    if (numNeighbors >= 3):
        corePoints.append(thePlayer)
    else:
        nonCorePoints.append(thePlayer)
    
    if len(l_notVisited) > 0:
        return isCore(l_notVisited,players),distances,l_zYPA,l_zPct
    else:
        return "DONE",distances,l_zYPA,l_zPct
        #return "Core",l_notVisited,thePlayer
    
    #return "Non Core",l_notVisited,thePlayer

def isBorderOrNoise(l_nonCore,l_Core,dict_Players):
    '''
    Will take every non-core point and loop through the list of core points, gathering the distance 
    of the non-core point to each core point.
    
    For each non-core point, the shortest distance to a core point will be extracted
    
    If shortest distance < n, the non-core point will be added to that core point's cluster
    
    If shortest distance > n, the non-core point will be considered noise
    '''
    
    
    for nonCorePoint in l_nonCore:
        zYPA_nonCore = (float(dict_Players[nonCorePoint].YPA) - avg_YPA) / SD_YPA
        zPct_nonCore = (float(dict_Players[nonCorePoint].pct) - avg_pct) / SD_pct
        
        for corePoint in l_Core:
            distances = []
            zYPA_core = (float(dict_Players[corePoint].YPA) - avg_YPA) / SD_YPA
            zPct_core = (float(dict_Players[corePoint].pct) - avg_pct) / SD_pct
            
            dist = math.sqrt((zYPA_nonCore - zYPA_core)**2 + (zPct_nonCore - zPct_core)**2)
            distances.append(dist)
            
        shortestDistance = min(distances)
        print(shortestDistance,n)
        
        if shortestDistance <= n:
            borderPoints.append(nonCorePoint)
        else:
            noisePoints.append(nonCorePoint)
            
            
def assignBorderToCore():
    return 

def findNeighborhoodPoints(num, dict_Players):
    
    neighborhood = []
    thePlayer = playerName[num]
    
    for comparePlayer in playerName:
        dist = math.sqrt(((float(dict_Players[thePlayer].YPA)\
                           - float(dict_Players[comparePlayer].YPA))/avg_YPA)**2\
    + ((float(dict_Players[thePlayer].pct)\
        - float(dict_Players[comparePlayer].pct))/avg_pct)**2)
    
        if (dist <= n) and (dist != 0):
            neighborhood.append(playerName.index(comparePlayer))
     
    return neighborhood

def main():
    
    isCoreReturn = isCore(playerName,players)
    isBorderOrNoise(nonCorePoints,corePoints,players)
    
    plt.figure()
    plt.plot(isCoreReturn[2], isCoreReturn[3],'o')
    plt.xlabel('YPA')
    plt.ylabel('Completion PCT')
    for i in range(len(isCoreReturn[2])):
        plt.annotate(playerInitials[i],(isCoreReturn[2][i],isCoreReturn[3][i]))

    
    print(isCoreReturn[1])
    print(sum(isCoreReturn[1])/len(isCoreReturn[1]))
    print('Core Points: ', corePoints)
    print('Border Points: ', borderPoints)
    print('Noise Points: ', noisePoints)
   
        
    
if __name__ == "__main__":
    main()





