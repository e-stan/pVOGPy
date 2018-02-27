"""
Test file to determine speed of alignment

"""
import sys

AlignmentFile = sys.argv[1]

file = open(AlignmentFile,'r')

data = file.readlines()

allAlign = []

for x in data:
    if not(x.startswith('#') or x.startswith("//")):
        allAlign.append(x)


temp = allAlign[0].split()
length = int(temp[0])
alignment = temp[1]
for x in allAlign[1:]:
    temp = x.split()
    alignment+=temp[1]
targetLen = len(alignment)
queryLen = 0
for c in alignment:
    if c.isalpha():
        queryLen+=1.0
coverage = queryLen/length
file.close()

sys.exit(int(coverage*100))
