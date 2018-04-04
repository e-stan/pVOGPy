import pickle
import numpy

filename = "_allFastaFiles.faa.csv"#"partialFasta.faa.csv"
numFiles = 297
splitData = []
delimiter = ","

file = open('TrustedCuttoffs.dat','r')
TC = file.readlines()
file.close()

cutoff = dict()
for x in TC:
    temp = [y.rstrip() for y in x.split(delimiter)]
    if temp[1] == 'NA':
        cutoff[temp[0]] = float("inf")
    else:
        cutoff[temp[0]] = float(temp[1])

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
VOG2FoundProtein = dict(VOG2Protein)

for x in VOG2FoundProtein:
    VOG2FoundProtein[x] = []

for x in splitData:
    VOG2FoundProtein[x[1]].append([x[0]]+x[2:])

queryCutoffs = range(100)
targetCutoffs = range(100)
distances = []
params =[]

for QC in queryCutoffs:
    for TC in targetCutoffs:
        truePosFound = 0
        truePosLost = 0
        FalsePosFound = 0
        FalsePosLost = 0

        for x in VOG2FoundProtein:
            for y in VOG2FoundProtein[x]:
                if(y[2]>cutoff[x]):
                    if y[0] in VOG2Protein[x]:
                        truePosFound+=1
                    else:
                        FalsePosLost+=1
                else:
                    if y[4] > QC and y[5] > TC:
                        if y[0] in VOG2Protein[x]:
                            truePosFound += 1
                        else:
                            FalsePosLost += 1
                    else:
                        if y[0] in VOG2Protein[x]:
                            truePosLost+=1
                        else:
                            FalsePosFound+=1

        TPR = truePosFound/float(truePosFound+truePosLost)
        FPR = 1-(FalsePosFound/float(FalsePosLost+FalsePosFound))
        distances.append(numpy.sqrt((TPR-1)**2 + FPR**2))
        params.append([QC,TC])

print min(distances)
print "[QC,TC] = "
print params[distances.index(min(distances))]
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
params.append([QC, TC])

print distances[-1]

