# -*- coding: utf-8 -*-
"""
Created on Fri Feb 1st 
Extracts proteins from FamilyOfProteinsFile and output a test file of accession

@author: stancliffe
"""

filename = "AllFamilyproteinList.tsv"

file = open(filename,'r')

data = file.readlines()

accession = []

for x in data[2:]:
    if x.startswith('#V'):
        temp = x.split()
        accession+=temp[2].split(',')
file.close()

file = open('Accession.dat','w')

for x in accession:
    if(x[-2:] == '.1'):
        index = x.index('-')
        file.write(x[index+1:]+'\n')
file.close()


