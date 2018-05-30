# -*- coding: utf-8 -*-

import pickle

filename = "_allFastaFiles.faa.csv"#"partialFasta.faa.csv"
filepath ="enhancedpVOGAllSeqResults/"
numFiles = 30
splitData = []

for filenum in [y+1 for y in range(numFiles)]:

    file = open(filepath+str(filenum)+filename,'r')

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
            if (len(newData) != 7):splitData.remove(newData)
    file.close
# file = open("protein2VOG.pickle",'rb')
# protein2VOG = pickle.load(file)
# file.close()

file = open("VOG2ProteinEnhanced.pickle",'rb')
VOG2Protein = pickle.load(file)

file.close()

file = open('TrustedCuttoffsBestHit.dat','w')

VOG2FoundProtein = dict(VOG2Protein)

for x in VOG2FoundProtein:
    VOG2FoundProtein[x] = []
print len(splitData)
for x in splitData:
    VOG2FoundProtein[x[1]].append([x[0]]+x[2:])
noFPcount = 0
firstFPCount = 0
noHitFound = 0
#print VOG2FoundProtein["VOG0006"]
for x in VOG2FoundProtein:
    VOG2FoundProtein[x].sort(key = lambda x: x[2],reverse = True)
    #print VOG2FoundProtein[x]
    file.write(x)
    for y in VOG2FoundProtein[x]:
        #print y
       # print y[0]
       # print VOG2Protein[x][0]
        if not(y[0] in VOG2Protein[x]):
            if y == VOG2FoundProtein[x][0]:
                file.write(delimiter+"NA")
                file.write(delimiter+str(y[2]))
                firstFPCount += 1
            else:
                file.write(delimiter+str(VOG2FoundProtein[x][VOG2FoundProtein[x].index(y)-1][2]))
                file.write(delimiter+str(y[2]))
           # print x + "First = " + delimiter+str(y[2])
            break
        if y == VOG2FoundProtein[x][-1]:
            file.write(delimiter+str(y[2]))
            file.write(delimiter + "NA")
            noFPcount += 1
    if len(VOG2FoundProtein[x]) == 0:
        file.write(delimiter + "NA")
        file.write(delimiter + "NA")
        noHitFound += 1
    file.write("\n")
    
    
print noFPcount
print firstFPCount
print noHitFound
file.close()
# -*- coding: utf-8 -*-

