#!/bin/bash

for ((i=0; i<200; i+=20));
do
	python ROCFlatCutoffEnhanced.py $i &
done

for ((i=0; i<200; i+=20));
do
	python ROCFlatCutoffEnhancedBestHit.py $i &
done