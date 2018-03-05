# -*- coding: utf-8 -*-
"""
Created on Mon Mar 05 12:55:25 2018

@author: stancliffe
"""
import numpy as np

filename = "paramSweep5.fasta.csv"

file = open(filename,'r')

data = file.readlines()

delimiter = ","
lengths = []

for x in data:
    temp = x.split(delimiter)
    lengths.append((len(temp)-1)/5)

print(np.sum(lengths)/1000.)