"""
Test file to determine speed of alignment

"""
import sys

AlignmentFile = sys.argv[1]

file = open(AlignmentFile,'r')

data = file.readlines()

allAlign = []

for x in data:
    temp = x
    if not(temp.startswith('#') or temp.startswith("//") or temp.startswith("\n")):
        allAlign.append(temp.rstrip())

temp = allAlign[0].split()
length = int(temp[0])
alignment = temp[1]
for x in allAlign[1:]:
    temp = x.split()
    alignment+=temp[1]
targetLen = len(alignment)
queryLen = 0
for c in alignment:
    if c.isupper():
        queryLen+=1.0
coverage = queryLen/targetLen
file.close()

sys.exit(int(coverage*100))
