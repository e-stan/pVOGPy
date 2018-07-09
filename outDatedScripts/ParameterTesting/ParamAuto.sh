#!/bin/bash

baseQuery=$1
numSamps=$2
rm HitsPerQueryEval.dat
rm HitsPerQueryBS.dat
for samp in `seq 1 $numSamps`;
do
		echo $samp
		#./EValSweep.sh $baseQuery$samp.fasta
		BSSweep.sh $baseQuery$samp.fasta
done    
        