#!/bin/bash
#Runs HMMScan multiple times recording the number of hits/query as a function of bitscore
queryName=$1
rm HitsPerQueryEval.dat
./hmmScanScript.sh $queryName $bitThresh
for eThresh in `seq -20 1`;
do
		echo 10e$eThresh
		python outputFilter.py result.log 10e$eThresh
done    
        

