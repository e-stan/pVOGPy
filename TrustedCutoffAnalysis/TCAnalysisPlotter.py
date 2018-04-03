import matplotlib.pyplot as plt
import matplotlib
import numpy as np

filename = "TrustedCuttoffs.dat"

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
TC = [cutoffs[x][0] for x in cutoffs]
NC = [cutoffs[x][1] for x in cutoffs]
TCNC = [[cutoffs[x][0],cutoffs[x][1]] for x in cutoffs]
#print TCNC
plt.hist(TC,1000)
plt.xlabel("Trusted Cutoff")
plt.ylabel("# of VOGs")

plt.figure()

plt.hist(NC,1000)
plt.xlabel("Noise Cutoff")
plt.ylabel("# of VOGs")

plt.figure()

plt.hist2d([x[0] for x in TCNC],[x[1] for x in TCNC],bins = (70,70), norm=matplotlib.colors.LogNorm())

plt.xlabel("Trusted Cutoff")
plt.ylabel("Noise Cutoff")
plt.colorbar()
print("Error Count = ")
print(error)
print("Mean TC: "+str(np.mean(TC)))
print("Mean NC: "+str(np.mean(NC)))
print("STD of TC: "+str(np.std(TC)))
print("STD of NC: "+str(np.std(NC)))

plt.show()