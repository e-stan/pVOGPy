#!/bin/bash

for ((i=0; i<200; i+=10));
do
	python ROCFlatCutoffEnhancedTopTwo.py $i &
done