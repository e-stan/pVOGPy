import sys
import os

line=sys.argv[1]
databaseName = sys.argv[2]
UUID = sys.argv[3]

line = line.split(",")

pVOG = line[1]
protein = line[0]

file = open("access2id.txt"+UUID,'r')

data = file.readlines()
acc2id = dict()

for x in data:
    temp = x.split()
    temp = [y.rstrip() for y in temp]
    acc2id[temp[0]] = temp[1]
file.close()

os.system("/local/vol00/shared/bin/hmmalign -o temp.txt"+UUID+" "+databaseName+pVOG+".hmm"+" "+ acc2id[protein]+".faaTEMPP"+UUID)



