#!/bin/bash
base=_allFastaFiles.faa
for i in `seq 1 30`;
do 
	./pVOGPipeline.sh trustedCutoffWithEnhanced/$i$base 2 &
	#echo $i$base
done