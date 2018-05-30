import sys
import pickle

#blastdbcmdmore

filename = "allFastaFiles.faa"

file = open(filename,'r')
filename = "_"+filename

data = file.readlines()

file.close()

file = open("VOG2ProteinEnhanced.pickle",'rb')
VOG2Protein = pickle.load(file)
file.close()
print len(VOG2Protein)

proteinFasta = dict()
first = True
temp = ""
for x in data:
    if x.startswith('>'):
        if first:
            access = x[1:].rstrip()
            first = False
        else:
            proteinFasta[access] = temp
            temp = ""
            access = x[1:].rstrip()
    else:
        temp += x
proteinFasta[access] = temp
fileEnding = ".faa"
for x in VOG2Protein:
    file = open(x+fileEnding,'w')
    for y in VOG2Protein[x]:
        file.write(">"+y)
        file.write("\n"+proteinFasta[y])
    file.close()

            
        
