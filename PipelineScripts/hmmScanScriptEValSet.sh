#!/bin/bash
#For running hmmscan
outfile="result.log" 
databaseName=pVOGDB/pVOGDataBase
queryName=$1
EVal=10e-10

/local/vol00/shared/bin/hmmscan --tblout $outfile -E $EVal $databaseName $queryName > junk.txt
rm junk.txt