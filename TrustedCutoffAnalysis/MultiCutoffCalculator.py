# -*- coding: utf-8 -*-

import pickle

filename = "_allFastaFiles.faa.csv"#"partialFasta.faa.csv"
numFiles = 297
splitData = []

for filenum in [y+1 for y in range(numFiles)]:

    file = open(str(filenum)+filename,'r')

    data = file.readlines()

    delimiter = ","

    for x in data[1:]:
        temp = x.split(delimiter)
        protein = temp[0]
        temp=temp[1:]
        numHits = 1#len(temp)/6
       # print x
        for x in range(numHits):
            newData = [protein]+temp[x*6:x*6+6]
            newData = newData[:2] + [float(z) for z in newData[2:]]
            splitData.append(newData)
    file.close

file = open("protein2VOG.pickle",'rb')
protein2VOG = pickle.load(file)
file.close()

file = open("VOG2Protein.pickle",'rb')
VOG2Protein = pickle.load(file)

file.close()

file = open('TrustedCuttoffsMulti.dat','w')

VOG2FoundProtein = dict(VOG2Protein)

for x in VOG2FoundProtein:
    VOG2FoundProtein[x] = []

for x in splitData:
    duplicate = False
    for y in VOG2FoundProtein[x[1]]:
        if y[1:-1] == x[2:]:
            if (not y[-1]) and x[1] in protein2VOG[x[0]]:
                VOG2FoundProtein[x[1]].remove(y)
                duplicate = False
            else:    
                duplicate = True
    if not duplicate:
        VOG2FoundProtein[x[1]].append([x[0]]+x[2:])
        if x[1] in protein2VOG[x[0]]:
            VOG2FoundProtein[x[1]][-1].append(True)
        else:
            VOG2FoundProtein[x[1]][-1].append(False)


for x in VOG2FoundProtein:
    VOG2FoundProtein[x].sort(key = lambda x: x[2],reverse = True)
    file.write(x)
    noTC1 = True
    for y in VOG2FoundProtein[x]:
        if not(y[-1]):
            if y == VOG2FoundProtein[x][0]:
                file.write(delimiter+"inf")
                noTC1 = True
            else:
                file.write(delimiter+str(VOG2FoundProtein[x][VOG2FoundProtein[x].index(y)-1][2]))
                TC1 = VOG2FoundProtein[x][VOG2FoundProtein[x].index(y)]
                noTC1 = False
            break
        if y == VOG2FoundProtein[x][-1]:
            file.write(delimiter+"1.0")
            TC1 = 1.0
            noTC1 = True

    VOG2FoundProtein[x].sort(key=lambda x: x[2],reverse = False)
    noNC1 = True
    for y in VOG2FoundProtein[x]:
        if (y[-1]):
            if not y == VOG2FoundProtein[x][0]:
                file.write(delimiter + str(VOG2FoundProtein[x][VOG2FoundProtein[x].index(y)-1][2]))
                NC1 = VOG2FoundProtein[x][VOG2FoundProtein[x].index(y)]
                noNC1 = False
            else:
                NC1 = -1
                file.write(delimiter+str(1.0))
                noNC1 = False
            break
        if y == VOG2FoundProtein[x][-1]:
            file.write(delimiter+"inf")
            noNC1 = True
            
            
    if not(noNC1 or noTC1):
        VOG2FoundProtein[x].sort(key=lambda x: x[2], reverse=True)
        if NC1 == -1:temp = VOG2FoundProtein[x][VOG2FoundProtein[x].index(TC1):]
        else: temp = VOG2FoundProtein[x][VOG2FoundProtein[x].index(TC1):VOG2FoundProtein[x].index(NC1)+1]
        temp.sort(key=lambda x:x[4],reverse = True)
        noTC2 = True
        if len(temp) > 1:
            for y in temp:
                if not (y[-1]):
                    if y == VOG2FoundProtein[x][0]:
                        file.write(delimiter + "inf")
                        noTC2 = True
                        # file.write(delimiter+str(y[2]))
                    else:
                        file.write(delimiter + str(temp[temp.index(y)-1][4]))
                        TC2 = y
                        noTC2 = False
                    break
                if y == temp[-1]:
                    file.write(delimiter + "1.0")
                    TC2 = 1.0
                    noTC2 = True
            
            temp.sort(key=lambda x: x[4], reverse=False)
            noNC2 = True
            for y in temp:
                if (y[-1]):
                    if not y == temp[0]:
                        file.write(delimiter + str(temp[temp.index(y)-1][4]))
                        NC2 = temp[temp.index(y)]
                        noNC2 = False
                    else:
                        NC2 = -1
                        file.write(delimiter+str(1.0))
                        noNC2 = False
                    break
                if y == temp[-1]:
                    file.write(delimiter + "inf")
                    print VOG2FoundProtein[x]
                    print y
                    print temp
                    print NC1
                    noNC2 = True
            if not(noNC2 or noTC2):
                temp.sort(key=lambda x: x[4], reverse=True)
                if NC2 == -1:temp = temp[temp.index(TC2):]
                else: temp = temp[temp.index(TC2):temp.index(NC2)+1]
                if len(temp) > 1:
                    temp.sort(key=lambda x: x[5], reverse=True)
                    noTC3 = False
                    for y in temp:
                        if not (y[0] in VOG2Protein[x]):
                            if y == VOG2FoundProtein[x][0]:
                                file.write(delimiter + "inf")
                                noTC3 = True
                            else:
                                file.write(delimiter + str(temp[temp.index(y) - 1][5]))
                                TC3 = temp[temp.index(y)]
                            break
                        if y == temp[-1]:
                            file.write(delimiter + "1.0")
                            TC3 = 1.0
                            noTC3 = True

                    temp.sort(key=lambda x: x[5], reverse=False)
                    NoNC3 = False
                    for y in temp:
                        if (y[-1]):
                            if not y == temp[0]:
                                file.write(delimiter + str(temp[temp.index(y) - 1][5]))
                                NC3 = temp[temp.index(y) - 1]
                            else:
                                NC3 = -1
                                file.write(delimiter+str(1.0))
                            break
                        if y == temp[-1]:
                            file.write(delimiter + "inf")
                            noNC3 = True

    if len(VOG2FoundProtein[x]) == 0:
        file.write(delimiter + "NA")
        file.write(delimiter + "NA")

    file.write("\n")
