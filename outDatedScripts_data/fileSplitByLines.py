import sys

inputFile = sys.argv[1]

numFiles = sys.argv[2]
file = open(inputFile,'r')

lines = file.readlines()

file.close()

count = 0
fileCount = 1
switchPoint = int(len(lines)/int(numFiles))
print switchPoint
outFile = open(str(fileCount)+"_"+inputFile,'w')
temp = ""
for x in lines:
    if count == switchPoint:
        outFile.write(temp)
        outFile.close()
        fileCount+=1
        outFile = open(str(fileCount) + "_" + inputFile, 'w')
        count=0
    temp+=x
    count+=1

outFile.write(temp)
outFile.close()

