# -*- coding: utf-8 -*-
"""
Created on Thu Feb 01 17:27:27 2018
Analysis Script for Data Processing of Hits/Query as a function of bit score
@author: stancliffe
"""
import numpy as np
import matplotlib.pyplot as plt


filename = "HitsPerQueryEVal.dat"

file = open(filename,'r')

data = file.readlines()

res = {}

for x in data:
    temp=x.split()
    if float(temp[0]) in res:
        res[float(temp[0])].append(int(temp[1]))
    else:
        res[float(temp[0])] = [int(temp[1])]

means = []
bitscore = []
deviations = []

for x in res:
    if x < 11:
        bitscore.append(x)
        #print res[x]
        means.append(np.mean(np.array(res[x])))
        deviations.append(np.std(res[x]))
bitscore.sort()
means = [np.mean(np.array(res[x])) for x in bitscore]
plt.scatter(bitscore,means)
plt.xlabel("Evalue")
plt.semilogx(bitscore,means)
plt.ylabel("Mean Hits/Query")
plt.title("Bitscore 40")

plt.show()



