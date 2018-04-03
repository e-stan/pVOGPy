# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 17:30:57 2018

@author: stancliffe
"""

import sys
bitthresh = sys.argv[3]
covThresh = sys.argv[4]
covThreshTarget = sys.argv[5]
def goodHit(sample):
    newSample = list(sample)

    #for y in sample:
        #if not((float((y[1][1])) >= bitthresh and float(y[1][-2]) >= covThresh/2. and float(y[1][-1]) >=covThreshTarget/2.) or float(y[1][-2]) >= covThresh or float(y[1][-1]) >= covThreshTarget):
            #newSample.remove(y)
    return newSample

import sys

inputCSV = sys.argv[1]
inputCoverage = sys.argv[2]
delimiter = ","

file1 = open(inputCSV,'r')

dataOriginal = file1.readlines()
temp = []
for x in dataOriginal: temp.append(x.rstrip())
dataOriginal = temp
headers = dataOriginal[0]

file1.close()
originalData = dict()


for x in dataOriginal[1:]:
    temp = x.split(delimiter)
    numHits = (len(temp)-1)/4
    originalData[temp[0]] = []
    for x in range(numHits):
        originalData[temp[0]].append([temp[1+(x*4)],temp[(2+(x*4)):(5+(x*4))]])

file1 = open(inputCoverage,'r')
coverageData = file1.readlines()
temp = []
for x in coverageData: temp.append(x.rstrip())
coverageData = temp


for x in coverageData[1:]:
    temp = x.split(delimiter)
    for y in originalData[temp[0]]:
        if y[0] == temp[1]:
            y[1].append(temp[2])
            y[1].append(temp[3])
          
file1.close()

file1 = open(inputCSV,'w')
tempData = dict(originalData)
originalData = dict()
maxHits = 0
for x in tempData:
    temp = goodHit(tempData[x])
    if not len(temp) == 0:
        originalData[x] = temp
        if len(temp) > maxHits:
            maxHits = len(temp)

file1.write("#Query Name")
for x in range(maxHits):
    file1.write(delimiter+"Target "+str(x+1)+delimiter+"evalue "+str(x+1)+delimiter+"bitscore "+str(x+1)+delimiter+"bias"+str(x+1)+delimiter+"QueryCoverage"+str(x+1)+delimiter+"TargetCoverage"+str(x+1))
for x in originalData:
    file1.write("\n"+x)
    for y in originalData[x]:
        temp = ""
        for z in y[1]:
            temp+=(delimiter+z)
        file1.write(delimiter+y[0]+temp)
file1.close()



