# -*- coding: utf-8 -*-
from sklearn import svm
import pickle
import random
import matplotlib.pyplot as plt
import math
import numpy

filename = "_allFastaFiles.faa.csv"  # "partialFasta.faa.csv"
filepath = "enhancedpVOGAllSeqResults/"
numFiles = 30
splitData = []

for filenum in [y + 1 for y in range(numFiles)]:

    file = open(filepath + str(filenum) + filename, 'r')

    data = file.readlines()

    delimiter = ","

    for x in data[1:]:
        temp = x.split(delimiter)
        protein = temp[0]
        temp = temp[1:]
        numHits = len(temp)/6
        # print x
        if numHits > 2: numHits = 2
        for x in range(numHits):
            newData = [protein] + temp[x * 6:x * 6 + 6]
            newData = newData[:2] + [float(z) for z in newData[2:]]
            splitData.append(newData)
            if (len(newData) != 7): splitData.remove(newData)
    file.close


file = open("VOG2ProteinEnhanced.pickle", 'rb')
VOG2Protein = pickle.load(file)
file.close()

print len(splitData)

for x in splitData:
    if (x[0] in VOG2Protein[x[1]]):
        x.append(True)
    else:
        x.append(False)
for x in splitData:
    if x[2] == 0.0:
        x[2] = numpy.finfo(numpy.float64).min
    else:
        x[2] = math.log10(x[2])
maxes = []
for i in range(5):
    maxes.append(max([x[2+i] for x in splitData]))
for x in splitData:
    for i in range(5):
        x[i+2] = x[i+2]/maxes[i]

random.shuffle(splitData)

def partition(lst, n):
    division = len(lst) / float(n)
    return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in xrange(n) ]

splitData = partition(splitData,10)
results = []

for i in range(10):
    testData = splitData[i]
    tempData = list(splitData)
    tempData.remove(testData)

    flatList = []
    for x in tempData:
        for y in x:
            flatList.append(y)


    VOG2FoundProtein = dict(VOG2Protein)

    for x in VOG2FoundProtein:
        VOG2FoundProtein[x] = []


    for x in flatList:
        VOG2FoundProtein[x[1]].append([x[0]] + x[2:])


    SVMDict = dict()

    for x in VOG2FoundProtein:
        numHits = len(VOG2FoundProtein[x])
        sumPos = sum(y[-1] for y in VOG2FoundProtein[x])
        if not(sumPos == 0 or sumPos == numHits):
            clf = svm.SVC()
            weight = 10
            clf.set_params(class_weight = {True:1,False:weight})
            clf.fit([y[1:-1] for y in VOG2FoundProtein[x]],[y[-1] for y in VOG2FoundProtein[x]])
            SVMDict[x] = clf
        elif sumPos == 0:
            SVMDict[x] = "ALLFALSE"
        else:
            SVMDict[x] = "ALLTRUE"

    FPFound = 0
    FPLost = 0
    TPLost = 0
    TPFound = 0

    for x in testData:
        if SVMDict[x[1]] == "ALLFALSE":
            predict = False
        elif SVMDict[x[1]] == "ALLTRUE":
            predict = True
        else:
            predict = SVMDict[x[1]].predict([x[2:-1]])
        if predict and x[-1]:
            TPFound+=1
        elif not(predict or x[-1]):
            FPFound+=1
        elif predict or x[-1]:
            if predict: FPLost+=1
            if x[-1]: TPLost+=1

    print "##############"
    print "TPR: "+str(TPFound/float(TPLost+TPFound))
    print "FPR: " +str(FPLost/float(FPLost+FPFound))
    print weight
    print "##############"

    results.append([TPFound/float(TPLost+TPFound),FPLost/float(FPLost+FPFound),weight]) #true postive, false positive

print results

#plt.boxplot([results[:][0],results[:][1]])
plt.scatter([x[-1] for x in results],[x[0] for x in results])
plt.scatter([x[-1] for x in results],[x[1] for x in results])
plt.legend(["True Postive Rate","False Positve Rate"])
plt.show()



# -*- coding: utf-8 -*-

