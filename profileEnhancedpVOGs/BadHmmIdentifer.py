# -*- coding: utf-8 -*-

file=open('shouldBeMadeHMM.txt','r')

want =  [x.rstrip() for x in file.readlines()]

file.close()

file = open('madeHMM.txt','r')

have = [x.rstrip() for x in file.readlines()]

file.close()

file = open("pVOGs2Delete.txt",'w')

count = 0
for x in have:
    if not x in want:
        count += 1
        file.write(x+"\n")        
print count

file.close()
