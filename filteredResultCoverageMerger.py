# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 17:30:57 2018

@author: stancliffe
"""

import pandas as pd

inputCSV = "t7genome.csv"
inputCoverage = "coverageResult.txt"
delimiter = ","

file1 = open(inputCSV,'r')

dataOriginal = file1.readlines()
[x.strip() for x in dataOriginal]
headers = dataOriginal[0]

file1.close()
originalData = dict()


for x in dataOriginal[1:]:
    temp = x.split(delimiter)
    numHits = (len(temp)-1)/3
    originalData[temp[0]] = []
    for x in range(numHits):
        originalData[temp[0]].append([temp[1+(x*4)],temp[(2+(x*4)):(5+(x*4))]])

file1 = open(inputCoverage,'r')
coverageData = file1.readlines()
[x.strip() for x in coverageData]


for x in coverageData[1:]:
    temp = x.split(delimiter)
    for y in originalData[temp[0]]:
        if y[0] == temp[1]:
            y[1].append(temp[2])
          
file1.close()

file1 = open("Trial"+inputCSV,'w')
maxHits = (len(headers.split(delimiter))-1)/3
file1.write("#Query Name")
for x in range(maxHits):
    file1.write(delimiter+"Target "+str(x+1)+delimiter+"evalue "+str(x+1)+delimiter+"bitscore "+str(x+1)+delimiter+"bias"+str(x+1)+delimiter+"coverage"+str(x+1))
for x in originalData:
    file1.write("\n"+x)
    for y in originalData[x]:
        temp = ""
        print y
        for z in y[1]:
            #print z
            temp+=(delimiter+z)
        file1.write(delimiter+y[0]+temp)
file1.close()


