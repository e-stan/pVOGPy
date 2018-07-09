# -*- coding: utf-8 -*-
"""
Created on Thu Feb 01 17:27:27 2018
Analysis Script for Data Processing of Hits/Query as a function of bit score
@author: stancliffe
"""
import numpy as np
import matplotlib.pyplot as plt

numQuery = 9960.0
filename = "HitsPerQueryEval.dat"

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
eval = []
deviations = []

for x in res:
    if x < 11:
        eval.append(x)
        #print res[x]
        means.append(np.mean(np.array(res[x])))
        deviations.append(np.std(res[x])/np.sqrt(len(res[x])))
eval.sort()
means = [np.mean(np.array(res[x])) for x in eval]
deviations = [np.std(res[x])/np.sqrt(len(res[x])) for x in eval]
lengths = [100*len(res[x])/numQuery for x in eval]
plt.errorbar(eval,means,deviations)
plt.xlabel("Evalue")
plt.semilogx(eval,means)
plt.ylabel("Mean Hits/Query")
plt.title("Bitscore 40")

plt.figure()

plt.semilogx(eval,lengths)
plt.xlabel("Evalue")
plt.ylabel("%OfQuerysWithTargets")
plt.show()



