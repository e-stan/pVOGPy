import pickle
import numpy
import matplotlib.pyplot as plt


import pickle

filename = "_allFastaFiles.faa.csv"#"partialFasta.faa.csv"
filepath ="enhancedpVOGAllSeqResults/"
file = open('TrustedCuttoffsEnhancedBestHit.dat','r')
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
    
    
queryCutoffs = [x*3+37 for x in range(21)]
targetCutoffs = [x*3+37 for x in range(21)]
BSCutoffs = [x*4+30 for x in range(15)]

distances = []
params =[]
TPRs = []
FPRs = []


for QC in queryCutoffs:
     print QC
     for TC in targetCutoffs:
         for BS in BSCutoffs:     
             truePosFound = 0
             truePosLost = 0
             FalsePosFound = 0
             FalsePosLost = 0
       
             for x in VOG2FoundProtein:
                 for y in VOG2FoundProtein[x]:
                      if y[4] > QC and y[5] > TC and y[2] > BS:
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
             params.append([QC,TC,BS])



file = open("FlatThresholdBestHitAnalysisResults.txt",'w')
file.write("TPR,FPR,Query Coverage,Target Coverage,Bitscore\n")
for TPR,FPR,param in zip(TPRs,FPRs,params):
    file.write(str(TPR)+delimiter+str(FPR))
    [file.write(delimiter+str(x) ) for x in param]
    file.write("\n")
file.close()
print FPRs
minFPR = 1;
maxTPR = 0;
for x in range(len(FPRs)):
    if FPRs[x]  <= minFPR:
        minFPR = FPRs[x]
        
for x in range(len(FPRs)):
    if TPRs[x] > maxTPR and abs(FPRs[x]-minFPR) < 1e-6:
        maxTPR = TPRs[x]
        paramOptimal = params[x]


print minFPR
print maxTPR
print paramOptimal   

        
       
# RESULT 5/25/18
#
# 0.00882584712372
# 0.106190776307
# [97, 97, 30]

   
#plt.plot([x[0] for x in params],distances)
#plt.xlabel('Query Coverage Threshold')
#plt.ylabel('Distance from Optimality')
#plt.figure()
#plt.plot(FPRs,TPRs)
#plt.xlabel('FPR')
#plt.ylabel('TPR')
#print min(distances)
#print "[QC,TC] = "
#print params[distances.index(min(distances))]
#print "TPR FPR = "
#print TPRs[distances.index(min(distances))]
#print FPRs[distances.index(min(distances))]
#
#queryCutoffs = [81]
#targetCutoffs = [x*1 for x in range(100)]
#distances = []
#params =[]
#TPRs = []
#FPRs = []



# -*- coding: utf-8 -*-

