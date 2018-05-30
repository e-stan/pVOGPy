import pickle

file = open("VOG2Protein.pickle",'rb')
VOG2Protein = pickle.load(file)

file.close()
file = open("VOG2ProteinEnhanced.pickle",'rb')
VOG2ProteinEnhanced = pickle.load(file)
file.close()

ToMake = []
for x in VOG2Protein:
    if VOG2Protein[x] != VOG2ProteinEnhanced[x]:
        ToMake.append(x)
print len(ToMake)
file = open("madeVOGs.txt",'r')
data=[x.rstrip()[:-4] for x in file.readlines()]
for x in data:
    if x in ToMake:
        ToMake.remove(x)

file.close()
file = open('pVOGSToBuild.txt','w')
[file.write("pVOGFasta/"+x+".faa\n") for x in ToMake]
file.close()

print len(data)+len(ToMake)

