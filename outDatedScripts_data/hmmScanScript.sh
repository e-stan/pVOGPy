#!/bin/bash
#For running hmmscan
outfile="result.log" 
databaseName=pVOGDB/pVOGDataBase
queryName=$1
ethresh=$2
bitThresh=40

/local/vol00/shared/bin/hmmscan --tblout $outfile -T $bitThresh $databaseName $queryName > junk.txt
#python outputFilter.py $outfile $2
rm junk.txt
