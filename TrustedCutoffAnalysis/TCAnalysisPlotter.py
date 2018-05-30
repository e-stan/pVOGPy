import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.pylab import *# plb

filename = "TrustedCuttoffsEnhanced.dat"

file = open(filename,'r')

data = file.readlines()
delimiter = ","
cutoffs = dict()
error = 0
print len(data)
for x in data:
    temp = [z.rstrip() for z in x.split(delimiter)]
    if not('NA' in temp[1:]):
        cutoffs[temp[0]] = [float(y) for y in temp[1:]]
    else:
        error+=1
nums = range(len(cutoffs))
print min([len(cutoffs[x]) for x in cutoffs])
TC1 = [cutoffs[x][0] for x in cutoffs]
NC1 = [cutoffs[x][1] for x in cutoffs]
container = np.percentile(TC1,90)
print container

TC = [cutoffs[x][0] for x in cutoffs if cutoffs[x][0] < container]
NC = [cutoffs[x][1] for x in cutoffs if cutoffs[x][0] < container]
TCNC = [[x,y] for x,y in zip(TC,NC)]
mini = min([x for sublist in TCNC for x in sublist ])
maxi = max([x for sublist in TCNC for x in sublist ])
plt.hist(TC,1000)
plt.xlabel("Trusted Cutoff")
plt.ylabel("# of VOGs")

plt.figure()

plt.hist(NC,1000)
plt.xlabel("Noise Cutoff")
plt.ylabel("# of VOGs")
plt.figure()
axis = 10**np.linspace(np.log10(mini),np.log10(maxi),100)#logspace(np.min(TC+NC),np.max(TC+NC),1000)
counts,_,_= np.histogram2d([x[0] for x in TCNC],[x[1] for x in TCNC],bins = (axis,axis))
counts1 = counts.T
#fig,ax = plt.subplots()
plt.pcolormesh(axis,axis,counts.T,norm=matplotlib.colors.LogNorm())
#hist2d([x[0] for x in TCNC],[x[1] for x in TCNC],bins = (axis,axis), norm=matplotlib.colors.LogNorm())
xscale('log')
yscale('log')

plt.xlabel("Trusted Cutoff")
plt.ylabel("Noise Cutoff")
plt.colorbar()
print("Error Count = ")
print(error)
print("Median TC: "+str(np.median(TC1)))
print("Median NC: "+str(np.median(NC1)))
print("STD of TC: "+str(np.std(TC1)))
print("STD of NC: "+str(np.std(NC1)))
error = 0
for x,y in zip(TC1,NC1):
    if x < y:
        error += 1
print error
plt.figure()
#plt.boxplot([TC1,NC1],sym="",labels=["Trusted Cutoff","Noise Cutoff"])
TC2 = TC1
NC2 = NC1
#####################
filename = "TrustedCuttoffsEnhancedBestHit.dat"

file = open(filename,'r')

data = file.readlines()
delimiter = ","
cutoffs = dict()
error = 0
print len(data)
for x in data:
    temp = [z.rstrip() for z in x.split(delimiter)]
    if not('NA' in temp[1:]):
        cutoffs[temp[0]] = [float(y) for y in temp[1:]]
    else:
        error+=1
nums = range(len(cutoffs))
print min([len(cutoffs[x]) for x in cutoffs])
TC1 = [cutoffs[x][0] for x in cutoffs]
NC1 = [cutoffs[x][1] for x in cutoffs]
container = np.percentile(TC1,90)
print container

TC = [cutoffs[x][0] for x in cutoffs if cutoffs[x][0] < container]
NC = [cutoffs[x][1] for x in cutoffs if cutoffs[x][0] < container]
TCNC = [[x,y] for x,y in zip(TC,NC)]
mini = min([x for sublist in TCNC for x in sublist ])
maxi = max([x for sublist in TCNC for x in sublist ])
counts,_,_= np.histogram2d([x[0] for x in TCNC],[x[1] for x in TCNC],bins = (axis,axis))

################

plt.boxplot([TC2,NC2,TC1,NC1],sym="",labels=["Trusted Cutoff","Noise Cutoff","Trusted Cutoff BH","Noise Cutoff BH"])
plt.figure()
cMap = matplotlib.colors.ListedColormap(['b','w','y'])
plt.pcolormesh(axis,axis,counts.T-counts1)#,cmap=plt.cm.get_cmap('Dark2'))#,norm=matplotlib.colors.LogNorm())
xscale('log')
yscale('log')
plt.colorbar()
plt.xlabel("Trusted Cutoff")
plt.ylabel("Noise Cutoff")
plt.show()