# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 16:34:38 2018

@author: stancliffe
"""

filename = "AllFamilyProteinList.tsv"

import pickle

file = open(filename,'r')

data = file.readlines()

data = data[2:]

proteinVOGs = dict()
VOGProtein = dict()

for x in data:
    if x.startswith("#VOG"):
        temp = x.rstrip().split()
        VOG = temp[0][1:]
        temp2 = temp[-1].split(",")
        if not(VOG in VOGProtein):
            VOGProtein[VOG] = temp2
        for y in temp2:
            #index = y.index("-")
            protein = y#[index+1:]
            if protein in proteinVOGs:
                proteinVOGs[protein].add(VOG)
            else:
                proteinVOGs[protein] = set()
                proteinVOGs[protein].add(VOG)


file.close()
file = open('allIDs.txt','r')
data = file.readlines()

for x in data:
    temp = x.rstrip()
    if not(temp in proteinVOGs):
        proteinVOGs[temp] = set()

#print len(VOGProtein)
#print len(proteinVOGs)


proteinVOGsFile = open('protein2VOG.pickle','wb')
pickle.dump(proteinVOGs,proteinVOGsFile, protocol=pickle.HIGHEST_PROTOCOL)
VOGProteinFile = open('VOG2Protein.pickle','wb')
pickle.dump(VOGProtein,VOGProteinFile,protocol=pickle.HIGHEST_PROTOCOL)


