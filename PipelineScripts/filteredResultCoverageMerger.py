"""
This script filters the output of hmmalign and hmmscan and formats the final output report. This script takes as input the coverage, bitscore, and evalue thresholds,
as well as the reporting code options chosen. Based on the filtering options selected, the FPR and TPR is also estimated if the option is within a bitscore domain of 0-200
and the evalue is greater than 1e-70. For query proteins with no hits, "NO REPORTABLE HITS" is listed.
"""

import sys
import pickle
import math
covThresh = int(sys.argv[3])
covThreshTarget = int(sys.argv[4])
bitThresh = float(sys.argv[5])
ethresh = float(sys.argv[6])
reportingCode = int(sys.argv[7])
UUID = sys.argv[8]

###READ IN TRUSTED CUTOFF DATA
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

### DEFINITION OF REPORTABLE HIT FUNCTION.
def goodHit(sample):
    newSample = list(sample)
    if reportingCode == 1: #TRUSTED CUTOFF
        for y in sample:
            if float(y[1][1]) < cutoff[y[0]]:
                newSample.remove(y)
    if reportingCode == 2: #CUSTOM CUTOFFS (strictly greater than is used in the filter)
        for y in sample:
            if float(y[1][1]) <= bitThresh or float(y[1][3]) <= covThresh or float(y[1][4]) <= covThreshTarget or float(y[1][0]) >= ethresh:
                newSample.remove(y)
    return newSample

def eVal2Bit(eval):#Evalue to bitscore conversion formula for FPR and TPR Prediction
    if eval > 1e-70 and eval < 1.3e-7:return -1.408*math.log(eval)+8.0871
    if eval < 1e-70: return 235.0


#Read in unfiltered results
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

#save results in datastructure
for x in dataOriginal[1:]:
    temp = x.split(delimiter)
    numHits = (len(temp)-1)/4
    originalData[temp[0]] = []
    for x in range(numHits):
        originalData[temp[0]].append([temp[1+(x*4)],temp[(2+(x*4)):(5+(x*4))]])
#Read in coverage data
file1 = open(inputCoverage,'r')
coverageData = file1.readlines()
temp = []
for x in coverageData: temp.append(x.rstrip())
coverageData = temp
file1.close()

#Open final output file
file1 = open(inputCSV,'w')

#Calcualte and report FPR and TPR
if reportingCode == 1:
    file1.write("#BEGIN REPORT:\n#Predicted False Positive Rate: 0.0"+delimiter+"Predicted True Positive Rate: 0.75078\n")
elif reportingCode == 3:
    file1.write("#BEGIN REPORT:\n#Predicted False Positive Rate: 1.00"+delimiter+"Predicted True Positive Rate: 1.00\n")
else:
    file3 = open('FlatThresholdFTPRData.pickle','rb')
    readInData = pickle.load(file3) #load precomputed reuslts
    file3.close()
    tempBit = int(bitThresh)
    if eVal2Bit(ethresh) > bitThresh: tempBit = int(eVal2Bit(ethresh))
    try:
        [TPR,FPR] = readInData[covThresh][covThreshTarget][tempBit] #calculate if within range
        file1.write("#BEGIN REPORT:\n#Predicted False Positive Rate: "+str(FPR)+delimiter+"Predicted True Positive Rate: " + str(TPR)+"\n")
    except: #write error if the cutoffs are not within range
        file1.write("#BEGIN REPORT:\n#False Postive and True Positive Rates cannot be predicted due to choice of cutoffs. See HHpVOG help.\n")

#pair up hmmscan results with coverages
for x in coverageData[1:]:
    temp = x.split(delimiter)
    for y in originalData[temp[0]]:
        if y[0] == temp[1]:
            y[1].append(temp[2])
            y[1].append(temp[3])

#filter data
tempData = dict(originalData)
originalData = dict()
maxHits = 0
for x in tempData:
    temp = goodHit(tempData[x])
    if not len(temp) == 0:
        originalData[x] = temp
        if len(temp) > maxHits:
            maxHits = len(temp)

#output results
file1.write("#Query Name")
for x in range(2):
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
accessions = []
for x in file2.readlines():
    temp = x.split()
    accessions.append(temp[0])
for x in accessions:
    if not x in originalData:
     file1.write("\n"+x+delimiter+"NO REPORTABLE HITS FOUND")
file2.close()
file1.write("\n#End of Report")
file1.close()



