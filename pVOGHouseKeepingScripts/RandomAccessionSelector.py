# -*- coding: utf-8 -*-
"""
Created on Thu Feb 01 11:33:21 2018
Pulls numSeqs random accession numbers out of the file Accession.dat which is 
created by proteinAccessionExtrator and contains all protein accessions within
the pVOG database. Script outputs a .dat file randomAccessions.dat 
@author: stancliffe
"""

import random
print random.random()
file = open('Accession.dat','r')

accessions = file.readlines()

numSeqs = 300

randAcc = []

randAcc = random.sample(accessions,numSeqs)

file.close()

file = open('randomAccessions.dat','w')

for x in randAcc:
    file.write(x)
file.close()

