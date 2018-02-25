# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 11:09:38 2018
Filters tabular output of hmmscan, for bit value of the target profile

@author: stancliffe
"""
import sys

inputfile = sys.argv[1]
bitThresh = float(sys.argv[2])

print bitThresh  #bit score threshold #CHANGE LATER


file = open(inputfile,'r')

data = file.readlines() #get data

arrayData = []

for x in data:
    if x[0] != "#": arrayData.append(x.split()[0:7]) #get uncommented lines
for x in arrayData:
    x[4:] = [float(y) for y in x[4:]] #convert string to float for numeric fields

filteredData = dict()

for x in arrayData:
    if x[4] <= bitThresh:   #if bit score is greater than bitThresh
        if x[2] in filteredData:
            filteredData[x[2]].append([x[0],x[4:]])
        else:
            filteredData[x[2]] = [[x[0],x[4:]]]

print("Query Name\n[Target Name , evalue, bit score, bias] , ...\n")

for x in filteredData: #output filtered data
    print(x+'\t')
    print(filteredData[x])
    print('\n')
    
    
file.close()

"""FOR PARAMETER TESTING"""
file = open('HitsPerQuery.dat','a')
for x in filteredData:
    file.write(str(bitThresh)+'\t'+str(len(filteredData[x]))+'\n')
file.close()
    