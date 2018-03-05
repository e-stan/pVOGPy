#!/bin/bash
#Runs HMMScan multiple times recording the number of hits/query as a function of eval
queryName=$1
./hmmScanScriptBitSet.sh $queryName
for eThresh in `seq -20 1`;
do
		echo 10e$eThresh
		python HPQEVal.py result.log 10e$eThresh
done    
        

