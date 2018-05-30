#!/bin/bash
base=_pVOGSToBuild.txt
for i in `seq 1 26`;
do 
	./testhmmbuilder.sh $i$base &
done