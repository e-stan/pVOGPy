# -*- coding: utf-8 -*-
"""

"""

import sys
import pickle
covThresh = float(sys.argv[3])
covThreshTarget = float(sys.argv[4])
bitThresh = float(sys.argv[5])
ethresh = float(sys.argv[6])
reportingCode = int(sys.argv[7])
UUID = sys.argv[8]

file = open('TrustedCuttoffs.dat','r')
TC = file.readlines()
file.close()

cutoff = dict()
for x in TC:
    temp = [y.rstrip() for y in x.split(",")]
    if temp[1] == 'NA':
        cutoff[temp[0]] = float("inf")
    else:
        cutoff[temp[0]] = float(temp[1])


def goodHit(sample):
    newSample = list(sample)
    if reportingCode == 1:
        for y in sample:
            if float(y[1][1]) < cutoff[y[0]]:
                newSample.remove(y)
    else:
        for y in sample:
            if float(y[1][1]) < bitThresh or float(y[1][3]) < covThresh or float(y[1][4]) < covThreshTarget or float(y[1][0]) > ethresh:
                newSample.remove(y)
    return newSample

def eVal2Bit(eval):
    return eval*10+3 #TODO replace with actual formula
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
file1.close()

file1 = open(inputCSV,'w')
if reportingCode == 1:
    file1.write("#BEGIN REPORT:\tPredicted False Positive Rate: 0.0\tPredicted True Positive Rate: .7845\n")
else:
    file3 = open('FlatThresholdFTPRData.pickle','rb')
    readInData = pickle.load(file3)
    file3.close()
    tempBit = int(bitThresh)
    if eVal2Bit(ethresh) > bitThresh: tempBit = int(eVal2Bit(ethresh))
    try:
        [TPR,FPR] = readInData[covThresh][covThreshTarget][tempBit]
        file1.write("#BEGIN REPORT:\tPredicted False Positive Rate: "+str(FPR)+"\tPredicted True Positive Rate: " + str(TPR)+"\n")
    except:
        file1.write("#BEGIN REPORT:\tFalse Postive and True Positive Rates cannot be predicted due to choice of cutoffs. See HHpVOG help.\n")


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
    i = 0
    file1.write("\n"+x)
    for y in originalData[x]:
        if i < 2:
            temp = ""
            for z in y[1]:
                temp+=(delimiter+z)
            file1.write(delimiter+y[0]+temp)
        i+=1

file2 = open("access2id.txt"+UUID,'r')
accessions = [x.split()[0] for x in file.readlines]
for x in accessions:
    if not x in originalData:
     file1.write("\n"+x+delimiter+"NO REPORTABLE HITS FOUND")
file2.close()
file1.write("\n#End of Report")
file1.close()



