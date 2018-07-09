import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.pylab import *# plb

#Open DataFile
filename = "TrustedCuttoffsEnhanced.dat"

file = open(filename,'r')

data = file.readlines()
delimiter = ","
cutoffs = dict()
error = 0
print len(data)

#gather TC when both TC and NC could be calculated
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

#set all point to be valid
container = np.percentile(TC1,100)+10
print container

#format data
TC = [cutoffs[x][0] for x in cutoffs if cutoffs[x][0] < container]
NC = [cutoffs[x][1] for x in cutoffs if cutoffs[x][0] < container]
TCNC = [[x,y] for x,y in zip(TC,NC)]
mini = min([x for sublist in TCNC for x in sublist ])
maxi = max([x for sublist in TCNC for x in sublist ])

#make 1d histograms
plt.hist(TC,1000)
plt.xlabel("Trusted Cutoff")
plt.ylabel("# of VOGs")

plt.figure()

plt.hist(NC,1000)
plt.xlabel("Noise Cutoff")
plt.ylabel("# of VOGs")

#make 2d heatmap
fig,ax = plt.subplots()
axis = 10**np.linspace(np.log10(mini),np.log10(maxi),100)
counts,_,_= np.histogram2d([x[0] for x in TCNC],[x[1] for x in TCNC],bins = (axis,axis))
counts1 = counts.T
counts1 = np.ma.masked_where(counts1 == 0, counts1)
cmap = plt.cm.ocean
cmap.set_bad(color = "white")
plt.pcolormesh(axis,axis,counts1,cMap=cmap)
xscale('log')
yscale('log')
ax.set_xticks([mini,1e2,1e3,maxi])
ax.set_xticklabels([str(mini),"1e2","1e3",str(maxi)])
ax.set_yticks([mini,1e2,1e3,maxi])
ax.set_yticklabels([str(mini),"1e2","1e3",str(maxi)])
plt.xlabel("Trusted Cutoff")
plt.ylabel("Noise Cutoff")
plt.colorbar()

#make zoomed in heatmap

#gather 90% of data
container = np.percentile(TC1,90)
print container

TC = [cutoffs[x][0] for x in cutoffs if cutoffs[x][0] < container]
NC = [cutoffs[x][1] for x in cutoffs if cutoffs[x][0] < container]
TCNC = [[x,y] for x,y in zip(TC,NC)]
mini = min([x for sublist in TCNC for x in sublist ])
maxi = max([x for sublist in TCNC for x in sublist ])

#make heatmap
fig,ax = plt.subplots()
axis = 10**np.linspace(np.log10(mini),np.log10(maxi),100)
counts,_,_= np.histogram2d([x[0] for x in TCNC],[x[1] for x in TCNC],bins = (axis,axis))
counts1 = counts.T
counts1 = np.ma.masked_where(counts1 == 0, counts1)
cmap = plt.cm.ocean
cmap.set_bad(color = "white")
plt.pcolormesh(axis,axis,counts1,cMap=cmap)
xscale('log')
yscale('log')
ax.set_xticks([mini,1e2,maxi])
ax.set_xticklabels([str(mini),"1e2",str(maxi)])
ax.set_yticks([mini,1e2,maxi])
ax.set_yticklabels([str(mini),"1e2",str(maxi)])
plt.xlabel("Trusted Cutoff")
plt.ylabel("Noise Cutoff")
plt.colorbar()

#Analysis
print("Error Count = ")
print(error)
print("Median TC: "+str(np.median(TC1)))
print("Median NC: "+str(np.median(NC1)))
print("STD of TC: "+str(np.std(TC1)))
print("STD of NC: "+str(np.std(NC1)))




#####################
TC2 = TC1
NC2 = NC1


#open best hit file and read in data
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

#seperate data
nums = range(len(cutoffs))
print min([len(cutoffs[x]) for x in cutoffs])
TC1 = [cutoffs[x][0] for x in cutoffs]
NC1 = [cutoffs[x][1] for x in cutoffs]

#threshold based on all hit data
container = np.percentile(TC2,90)
print container


#make difference plot of best hit vs all hit
fig,ax = plt.subplots()
TC = [cutoffs[x][0] for x in cutoffs if cutoffs[x][0] < container]
NC = [cutoffs[x][1] for x in cutoffs if cutoffs[x][0] < container]
TCNC = [[x,y] for x,y in zip(TC,NC)]
mini = min([x for sublist in TCNC for x in sublist ])
maxi = max([x for sublist in TCNC for x in sublist ])
counts,_,_= np.histogram2d([x[0] for x in TCNC],[x[1] for x in TCNC],bins = (axis,axis))
counts1 = np.ma.masked_where(counts.T - counts1 == 0, counts.T-counts1)
plt.pcolormesh(axis,axis,counts1,cMap = cmap)
xscale('log')
yscale('log')
ax.set_xticks([mini,1e2,maxi])
ax.set_xticklabels([str(mini),"1e2",str(maxi)])
ax.set_yticks([mini,1e2,maxi])
ax.set_yticklabels([str(mini),"1e2",str(maxi)])
plt.colorbar()
plt.xlabel("Trusted Cutoff")
plt.ylabel("Noise Cutoff")

#make boxplot
plt.figure()
plt.boxplot([TC2,NC2,TC1,NC1],sym="",labels=["Trusted Cutoff","Noise Cutoff","Trusted Cutoff BH","Noise Cutoff BH"])


plt.show()
