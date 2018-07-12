import pickle
import numpy
import matplotlib.pyplot as plt


filename = "_allFastaFiles.faa.csv"#"partialFasta.faa.csv"
numFiles = 297
splitData = []
delimiter = ","

file = open('TrustedCuttoffs.dat','r')
TC = file.readlines()
file.close()

cutoff = dict()
min = 100000
for x in TC:
    temp = [y.rstrip() for y in x.split(delimiter)]
    if temp[1] == 'NA':
        cutoff[temp[0]] = float("inf")
    else:
        cutoff[temp[0]] = float(temp[1])
        if float(temp[1]) < min:
            min = float(temp[1])
print min
#print max([cutoff[x] for x in cutoff])

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

queryCutoffs = [x for x in range(100)]
targetCutoffs = [69]
distances = []
params =[]
TPRs = []
FPRs = []

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
        TPRs.append(TPR)
        FPRs.append(FPR)
        params.append([QC,TC])
print"Query Coverage"

plt.plot([x[0] for x in params],distances)
plt.xlabel('Query Coverage Threshold')
plt.ylabel('Distance from Optimality')
plt.figure()
plt.plot(FPRs,TPRs)
plt.xlabel('FPR')
plt.ylabel('TPR')
print min(distances)
print "[QC,TC] = "
print params[distances.index(min(distances))]
print "TPR FPR = "
print TPRs[distances.index(min(distances))]
print FPRs[distances.index(min(distances))]

queryCutoffs = [81]
targetCutoffs = [x*1 for x in range(100)]
distances = []
params =[]
TPRs = []
FPRs = []

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
        TPRs.append(TPR)
        FPRs.append(FPR)
        params.append([QC,TC])
print"Target Coverage"
plt.figure()
plt.plot([x[1] for x in params],distances)
plt.xlabel('Target Coverage Threshold')
plt.ylabel('Distance from Optimality')
plt.figure()
plt.plot(FPRs,TPRs)
plt.xlabel('FPR')
plt.ylabel('TPR')
print min(distances)
print "[QC,TC] = "
print params[distances.index(min(distances))]
print "TPR FPR = "
print TPRs[distances.index(min(distances))]
print FPRs[distances.index(min(distances))]


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
print TPR
print FPR

plt.show()


###Final Output

#0.269950914817
# [QC,TC] =
# [81, 66]
# Using Trusted Cutoffs:
# 0.473138361281

#Full analysis
# inf
# Query Coverage
# 0.12620159309
# [QC,TC] =
# [61, 58]
# Target Coverage
# 0.152687135537
# [QC,TC] =
# [81, 44]
# Using Trusted Cutoffs:
# 0.485297494724

