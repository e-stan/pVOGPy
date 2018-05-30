
"""
Filters tabular output of hmmscan, placing data into a delimited file with each row as a query protein and each column
representing the best matches of that query protein to a target pVOG along with the respective evalue, bitscore, and bias.

"""

import sys

inputfile = sys.argv[1]
delimiter = sys.argv[2]
UUID = sys.argv[3]


file = open(inputfile,'r')

data = file.readlines() #get data

arrayData = []

for x in data:
    if x[0] != "#": arrayData.append(x.split()[0:7]) #get uncommented lines
for x in arrayData:
    x[4:] = [float(y) for y in x[4:]] #convert string to float for numeric fields

filteredData = dict()

for x in arrayData:
   # if x[5] >= bitThresh:   #if evalue is less than threshold
    if x[2] in filteredData:
        filteredData[x[2]].append([x[0],x[4:]])
    else:
        filteredData[x[2]] = [[x[0],x[4:]]]


maxHits = 0

for x in filteredData:
    if len(filteredData[x]) > maxHits:
        maxHits=len(filteredData[x])
file.close()

outFile = open(inputfile,'w')
outFile2 = open('coverage.txt'+UUID,'w')
j=0

outFile.write("#Query Name")
for x in range(maxHits):
    outFile.write(delimiter+"Target "+str(x+1)+delimiter+"evalue "+str(x+1)+delimiter+"bitscore "+str(x+1)+delimiter+"bias"+str(x+1))
for x in filteredData: #output filtered data
    outFile.write("\n"+x)
    for y in filteredData[x]:
        temp = ""
        for z in y[1]:
            temp += (delimiter+str(z))
        outFile.write(delimiter+y[0]+temp)
    for y in filteredData[x]:
        outFile2.write(x)
        outFile2.write(delimiter+y[0])
        outFile2.write('\n')
    j+=1

outFile2.write("\nCORRECT")
outFile.write("\nCORRECT")
outFile.close()
outFile2.close()




