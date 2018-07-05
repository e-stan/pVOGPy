import pickle

fileEndings = [str(10*x)+"_"+str(10*x+9) for x in range(20)]
totalData = []
for x in fileEndings:

    file = open("./FlatThresholdResults/FlatThresholdAnalysisResultsTopTwo"+ x +".txt",'r')
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

min = 2
minParams = []
for x in data:
    results[int(x[2])][int(x[3])][int(x[4])] = x[:2]
    if ((1-x[0])**2+x[1]**2)**.5 < min:
        min = ((1-x[0])**2+x[1]**2)**.5
        minParams = x[2:]

print results[23][50][76]
print min
print minParams
print results[int(minParams[0])][int(minParams[1])][int(minParams[2])]
outFile = open('FlatThresholdFTPRData.pickle','wb')
pickle.dump(results,outFile, protocol=pickle.HIGHEST_PROTOCOL)

outFile.close()

###TEST

file = open('FlatThresholdFTPRData.pickle','rb')
readInData = pickle.load(file)
print readInData[23][50][76]

#Result 7/1/18
# 0.150539302741
# [61.0, 53.0, 73.0]
# [0.899258114871, 0.111862211002]