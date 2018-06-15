import pickle

fileEndings = [str(20*x)+"_"+str(20*x+19) for x in range(10)]
totalData = []
for x in fileEndings:

    file = open("./FlatThresholdResults/FlatThresholdAnalysisResults"+ x +".txt",'r')
    data = file.readlines()
    data = data[1:]

    data = [[float(y) for y in x.split(",")] for x in data]
    file.close()
    totalData += data
data = totalData

results = []
for qc in range(100):
    results.append([])
    for tc in range(100):
        results[qc].append([])
        for bs in range(200):
            results[qc][tc].append([])

for x in data:
    results[int(x[2])][int(x[3])][int(x[4])] = x[:2]

print results[23][50][76]
outFile = open('FlatThresholdFTPRData.pickle','wb')
pickle.dump(results,outFile, protocol=pickle.HIGHEST_PROTOCOL)

outFile.close()

###TEST

file = open('FlatThresholdFTPRData.pickle','rb')
readInData = pickle.load(file)
print readInData[23][50][76]