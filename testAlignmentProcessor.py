"""
Test file to determine speed of alignment

"""
import sys

AlignmentFile = sys.argv[1]

file = open(AlignmentFile,'r')

data = file.readlines()

alignment = ""

for x in data:
    if not(x.startswith('#') or x.startswith("//")):
        alignment+=x
temp = alignment.split()
length = int(temp[0])
alignment = temp[1]
targetLen = len(alignment)
queryLen = 0
for c in alignment:
    if c.isalpha():
        queryLen+=1.0
coverage = queryLen/length
file.close()

sys.exit(int(coverage*100))
