#!/bin/bash
#Runs HMMScan multiple times recording the number of hits/query as a function of bitscore
queryName="sequenceSamples.fasta"
rm HitsPerQuery.dat
for bitThresh in `seq 20 50`;
do
		echo $bitThresh
		./hmmScanScript.sh $queryName $bitThresh
done    
        

