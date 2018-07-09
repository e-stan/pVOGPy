import sys

#blastdbcmdmore

filename = sys.argv[1]

file = open(filename,'r')
filename = "_"+filename

data = file.readlines()

seqPerFile = 1000

seqNum = 0

fileNum = 1

seqAcc = []
outFile = open("1"+filename,'w')
seqAccFile = open("seqAcc.txt",'w')


for x in data:
    if x.startswith('>'):
        if(seqNum == seqPerFile):
            outFile.close()
            fileNum+=1
            outFile = open(str(fileNum) + filename,'w')
            seqNum = 0
            outFile.write(x)
        else:
            outFile.write(x)
            seqNum+=1
        temp = x.split()
        seqAccFile.write(temp[0][1:-2]+'\n')
    else:
        outFile.write(x)
