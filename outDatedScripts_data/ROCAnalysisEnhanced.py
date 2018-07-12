# -*- coding: utf-8 -*-

import pickle
import numpy

file = open('TrustedCuttoffsFinal.dat','r')
TC = file.readlines()
file.close()
delimiter = ","
cutoff = dict()
min = 100000
count = 0
for x in TC:
    temp = [y.rstrip() for y in x.split(delimiter)]
    if temp[1] == 'NA':
        cutoff[temp[0]] = float("inf")
        count += 1
    else:
        cutoff[temp[0]] = float(temp[1])
        if float(temp[1]) < min:
            min = float(temp[1])


print min
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
        numHits = 2#len(temp)/6
        realNum = len(temp) / 6
        if realNum < numHits: numHits = realNum
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

VOG2FoundProtein = dict(VOG2Protein)

for x in VOG2FoundProtein:
    VOG2FoundProtein[x] = []
print len(splitData)
for x in splitData:
    VOG2FoundProtein[x[1]].append([x[0]]+x[2:])

queryCutoffs = [x for x in range(100)]
targetCutoffs = [69]
distances = []
params =[]
TPRs = []
FPRs = []


print "Using Trusted Cutoffs: "
truePosFound = 0
truePosLost = 0
FalsePosFound = 0
FalsePosLost = 0



for x in VOG2FoundProtein:
    for y in VOG2FoundProtein[x]:
        if (y[2] > cutoff[x]):
            if y[0] in VOG2Protein[x]:
                truePosFound += 1
            else:
                FalsePosLost += 1
        else:
            if y[0] in VOG2Protein[x]:
                truePosLost += 1
            else:
                FalsePosFound += 1

TPR = truePosFound / float(truePosFound + truePosLost)
FPR = 1 - (FalsePosFound / float(FalsePosLost + FalsePosFound))
distances.append(numpy.sqrt((TPR - 1) ** 2 + FPR ** 2))

print distances[-1]
print TPR
print FPR

