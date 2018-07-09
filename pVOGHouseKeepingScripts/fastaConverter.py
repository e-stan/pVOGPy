
filename = "allgenomes_2993.faa"

file = open(filename,'r')

outFile = open("allFastaFiles.faa",'w')
seqIDs = open("allIDs.txt",'w')
data = file.readlines()

for x in data:
    if x.startswith(">"):
        temp = x.split("|")
        ID = temp[1]
        outFile.write(">"+ID+"\n")
        seqIDs.write(ID+'\n')
    else:
        outFile.write(x)

