# -*- coding: utf-8 -*-

import pickle

filename = "_allFastaFiles.faa.csv"#"partialFasta.faa.csv"
numFiles = 297
splitData = []

for filenum in [y+1 for y in range(numFiles)]:

    file = open(str(filenum)+filename,'r')

    data = file.readlines()

    delimiter = ","

    for x in data[1:]:
        temp = x.split(delimiter)
        protein = temp[0]
        temp=temp[1:]
        numHits = 1#len(temp)/6
       # print x
        for x in range(numHits):
            newData = [protein]+temp[x*6:x*6+6]
            newData = newData[:2] + [float(z) for z in newData[2:]]
            splitData.append(newData)
    file.close

file = open("protein2VOG.pickle",'rb')
protein2VOG = pickle.load(file)
file.close()

file = open("VOG2Protein.pickle",'rb')
VOG2Protein = pickle.load(file)

file.close()

file = open('TrustedCuttoffsNoDuplicatesBestHit.dat','w')

VOG2FoundProtein = dict(VOG2Protein)

for x in VOG2FoundProtein:
    VOG2FoundProtein[x] = []

for x in splitData:
    duplicate = False
    for y in VOG2FoundProtein[x[1]]:
        if y[1:-1] == x[2:]:
            if (not y[-1]) and x[1] in protein2VOG[x[0]]:
                VOG2FoundProtein[x[1]].remove(y)
                duplicate = False
            else:
                duplicate = True
    if not duplicate:
        VOG2FoundProtein[x[1]].append([x[0]]+x[2:])
        if x[1] in protein2VOG[x[0]]:
            VOG2FoundProtein[x[1]][-1].append(True)
        else:
            VOG2FoundProtein[x[1]][-1].append(False)

for x in VOG2FoundProtein:
    VOG2FoundProtein[x].sort(key = lambda x: x[2],reverse = True)
    file.write(x)
    for y in VOG2FoundProtein[x]:
        if not(y[0] in VOG2Protein[x]):
            if y == VOG2FoundProtein[x][0]:
                file.write(delimiter+"NA")
                file.write(delimiter+str(y[2]))
            else:
                file.write(delimiter+str(VOG2FoundProtein[x][VOG2FoundProtein[x].index(y)-1][2]))
                file.write(delimiter+str(y[2]))
            break
        if y == VOG2FoundProtein[x][-1]:
            file.write(delimiter+str(y[2]))
            file.write(delimiter + "1.0")
    if len(VOG2FoundProtein[x]) == 0:
        file.write(delimiter + "NA")
        file.write(delimiter + "NA")

    file.write("\n")
