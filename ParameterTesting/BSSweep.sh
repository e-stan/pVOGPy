#!/bin/bash
#Runs HMMScan multiple times recording the number of hits/query as a function of bitscore
queryName=$1
./hmmScanScriptEValSet.sh $queryName 
for bitThresh in `seq 20 100`;
do
		python HPQBitScore.py result.log $bitThresh
done    
        

