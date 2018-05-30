# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 15:14:57 2018

@author: stancliffe
"""

# -*- coding: utf-8 -*-

import pickle

filename = "_allFastaFiles.faa.csv"#"partialFasta.faa.csv"
numFiles = 297
splitData = []

for filenum in [y+1 for y in range(numFiles)]:

    file = open(str(filenum)+filename,'r')

    data = file.readlines()

    delimiter = ","

    for x in data[1:]:
        temp = x.split(delimiter)
        protein = temp[0]
        temp=temp[1:]
        numHits = 1#len(temp)/6
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
foundCount = 0
for x in splitData:
    if len(protein2VOG[x[0]]) == 0:
        if (x[2] < 10e-20 and x[-2] > 75 and x[-1] > 75):#possbly also have the bitscore > than the the minimum scoring hit in the VOG
            foundCount +=1 
            VOG2Protein[x[1]].append(x[0])

file = open("EnhancedPVogs.txt",'w')

file.write("pVOG, protein1, protein2, ... ")
for x in VOG2Protein:
    file.write("\n"+x)
    for y in VOG2Protein[x]:
        file.write(delimiter+y)
file.close()
VOGProteinFile = open('VOG2ProteinEnhanced.pickle','wb')
pickle.dump(VOG2Protein,VOGProteinFile,protocol=pickle.HIGHEST_PROTOCOL)
    
           