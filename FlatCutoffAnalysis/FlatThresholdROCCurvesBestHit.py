# -*- coding: utf-8 -*-
"""
Created on Tue May 08 11:00:40 2018

@author: stancliffe
"""

import pickle
import numpy
import matplotlib.pyplot as plt


import pickle

filename = "_allFastaFiles.faa.csv"#"partialFasta.faa.csv"
filepath ="enhancedpVOGAllSeqResults/"
delimiter = ","

cutoff = dict()
min = 100000
count = 0


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
targetCutoffs = [x for x in range(100)]
BSCutoffs = [x for x in range(200)]
evCutoffs = [(10**-75)*10**x for x in range(75)]


distances = []
TPRs = []
FPRs = []


for TC in targetCutoffs:
     truePosFound = 0
     truePosLost = 0
     FalsePosFound = 0
     FalsePosLost = 0
   
     for x in VOG2FoundProtein:
         for y in VOG2FoundProtein[x]:
              if y[5] > TC:
                  if y[0] in VOG2Protein[x]:
                      truePosFound += 1
                  else:
                      FalsePosLost += 1
              elif y[0] in VOG2Protein[x]:
                  truePosLost += 1
              else:
                  FalsePosFound += 1
            

     TPR = truePosFound/float(truePosFound+truePosLost)
     FPR = 1-(FalsePosFound/float(FalsePosLost+FalsePosFound))
     distances.append(numpy.sqrt((TPR-1)**2 + FPR**2))
     TPRs.append(TPR)
     FPRs.append(FPR)


plt.plot(FPRs,TPRs)
plt.xlabel('FPR')
plt.ylabel('TPR')


TPRs = []
FPRs = []
distances = []

for E in evCutoffs:
    truePosFound = 0
    truePosLost = 0
    FalsePosFound = 0
    FalsePosLost = 0

    for x in VOG2FoundProtein:
        for y in VOG2FoundProtein[x]:
            if y[1] < E:
                if y[0] in VOG2Protein[x]:
                    truePosFound += 1
                else:
                    FalsePosLost += 1
            elif y[0] in VOG2Protein[x]:
                truePosLost += 1
            else:
                FalsePosFound += 1

    TPR = truePosFound / float(truePosFound + truePosLost)
    FPR = 1 - (FalsePosFound / float(FalsePosLost + FalsePosFound))
    distances.append(numpy.sqrt((TPR - 1) ** 2 + FPR ** 2))
    TPRs.append(TPR)
    FPRs.append(FPR)

plt.plot(FPRs, TPRs)
plt.xlabel('FPR')
plt.ylabel('TPR')


TPRs = []
FPRs = []
distances = []

for BS in BSCutoffs:
     truePosFound = 0
     truePosLost = 0
     FalsePosFound = 0
     FalsePosLost = 0
   
     for x in VOG2FoundProtein:
         for y in VOG2FoundProtein[x]:
              if y[2] > BS:
                  if y[0] in VOG2Protein[x]:
                      truePosFound += 1
                  else:
                      FalsePosLost += 1
              elif y[0] in VOG2Protein[x]:
                  truePosLost += 1
              else:
                  FalsePosFound += 1
            

     TPR = truePosFound/float(truePosFound+truePosLost)
     FPR = 1-(FalsePosFound/float(FalsePosLost+FalsePosFound))
     distances.append(numpy.sqrt((TPR-1)**2 + FPR**2))
     TPRs.append(TPR)
     FPRs.append(FPR)

plt.plot(FPRs,TPRs)
plt.xlabel('FPR')
plt.ylabel('TPR')

TPRs = []
FPRs = []
distances = []

for QC in queryCutoffs:
     truePosFound = 0
     truePosLost = 0
     FalsePosFound = 0
     FalsePosLost = 0
   
     for x in VOG2FoundProtein:
         for y in VOG2FoundProtein[x]:
              if y[4] > QC:
                  if y[0] in VOG2Protein[x]:
                      truePosFound += 1
                  else:
                      FalsePosLost += 1
              elif y[0] in VOG2Protein[x]:
                  truePosLost += 1
              else:
                  FalsePosFound += 1
            

     TPR = truePosFound/float(truePosFound+truePosLost)
     FPR = 1-(FalsePosFound/float(FalsePosLost+FalsePosFound))
     distances.append(numpy.sqrt((TPR-1)**2 + FPR**2))
     TPRs.append(TPR)
     FPRs.append(FPR)

plt.plot(FPRs,TPRs)
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title("ROC Curve: Best Hit")
plt.legend(["Target Coverage","Bitscore","Query Coverage"])

file.close()


fileEndings = [str(20*x)+"_"+str(20*x+19) for x in range(10)]
totalData = []
for x in fileEndings:

    file = open("./FlatThresholdResults/FlatThresholdAnalysisResultsBesstHit"+ x +".txt",'r')
    data = file.readlines()
    data = data[1:]

    data = [[float(y) for y in x.split(",")] for x in data]
    data = [x + [((x[0]-1)**2 + x[1]**2)**.5] for x in data]
    file.close()
    totalData += data
data = totalData


min = data[0][-1]
for x in data:
    if x[-1] < min:
        min = x[-1]
fp = 1
for x in data:
    if x[-1] == min and fp > x[1]:
        optimal = x
        fp = x[1]
print optimal
FPRs = [x[1] for x in data]
TPRs = [x[0] for x in data]

plt.scatter(FPRs,TPRs,marker='+',linewidths=.002,c='.60')
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title("ROC Curve: Best Hit")
plt.legend(["Target Coverage","Evalue","Bitscore","Query Coverage","Combined Thresholding"])

plt.show()


# -*- coding: utf-8 -*-

#[0.882204973408, 0.113737851327, 62.0, 62.0, 73.0, 0.16374360175070277] 6/11/18