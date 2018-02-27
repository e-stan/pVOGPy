# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 15:36:40 2018

@author: stancliffe
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 07 11:57:23 2018

@author: stancliffe
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 11:09:38 2018
Filters tabular output of hmmscan, for bit value of the target profile

@author: stancliffe
"""
import sys

inputfile = sys.argv[1]
bitThresh = float(sys.argv[2])
delimiter = sys.argv[3]


file = open(inputfile,'r')

data = file.readlines() #get data

arrayData = []

for x in data:
    if x[0] != "#": arrayData.append(x.split()[0:7]) #get uncommented lines
for x in arrayData:
    x[4:] = [float(y) for y in x[4:]] #convert string to float for numeric fields

filteredData = dict()

for x in arrayData:
    if x[5] >= bitThresh:   #if evalue is less than threshold
        if x[2] in filteredData:
            filteredData[x[2]].append([x[0],x[4:]])
        else:
            filteredData[x[2]] = [[x[0],x[4:]]]


maxHits = 0

for x in filteredData:
    if len(filteredData[x]) > maxHits:
        maxHits=len(filteredData[x])
file.close()

outFile = open(inputfile,'w')
outFile2 = open('coverage.txt','w')
j=0

outFile.write("#Query Name")
for x in range(2):
    outFile.write(delimiter+"Target "+str(x+1)+delimiter+"evalue "+str(x+1)+delimiter+"bitscore "+str(x+1)+delimiter+"bias"+str(x+1))
for x in filteredData: #output filtered data
    outFile.write("\n"+x)
    for y in filteredData[x][:2]:
        temp = ""
        for z in y[1]:
            temp += (delimiter+str(z))
        outFile.write(delimiter+y[0]+temp)
    for y in filteredData[x][:2]:
        outFile2.write(x)
        outFile2.write(delimiter+y[0])
        #if j+1 < len(filteredData):
        outFile2.write('\n')
    j+=1
    

outFile.close()
outFile2.close()



