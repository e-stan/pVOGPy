"""Script to separate an input fasta file into individual files for each sequence in the file. The new files will contain the same sequence as in the original
but the data line will contain the sequence length (i.e. ><seqLength>) for use in calculating coverages. Run with python fastaSplit.py <inputFile> """

import sys

filename = sys.argv[1]

file = open(filename,'r')

data = file.readlines()

first = 0
for x in data:
    if x.startswith('>'):
        if not first == 0:
            outFile.close()
            outFile = open(temp+".faaTEMPP",'r')
            seqData = outFile.readlines()
            outFile.close()
            outFile = open(temp+".faaTEMPP",'w')
            sequence = ""
            for r in seqData: sequence += r
            length = len(sequence)
            outFile.write('>'+str(length)+'\n')
            for r in seqData:
                outFile.write(r)
            outFile.close()
        temp = x.split()
        temp = temp[0][1:]
        outFile = open(temp+".faaTEMPP",'w')
        first+=1
    else:
        outFile.write(x)
outFile.close()
outFile = open(temp+".faaTEMPP",'r')
seqData = outFile.readlines()
outFile.close()
outFile = open(temp+".faaTEMPP",'w')
sequence = ""
for r in seqData: sequence += r
length = len(sequence)
outFile.write('>'+str(length)+'\n')
for r in seqData:
    outFile.write(r)
outFile.close()
exit(77)
