#!/bin/bash
#Bash script that takes an input fasta file of viral protein sequences and searches the query sequences against a database of pVOG profiles. 
#After the search, hits are reported with target profiles scoring above a bitscore of 55 and a significance greater than an evalue of 10e-12
#to run: ./pVOGPipeline <inputFile>
outfile="$1.csv"
databaseName=pVOGDB/pVOGDataBase
queryName=$1
ethresh=10e-10
bitThresh=30
bitThresh2=60
covThresh=60
seqMax=1000
delimiter=,

seqs=$(cat $1 | grep -c ">")



if [ $seqs -lt $seqMax ]
then
	python fastaSplit.py $1
	/local/vol00/shared/bin/hmmscan --tblout $outfile -E $ethresh $databaseName $queryName > junk.txt
	#python outputFilter4Pipeline.py $outfile $bitThresh $delimiter
	python outputFilter.py $outfile $bitThresh $delimiter
	rm junk.txt
	./hmmAlign.sh coverage.txt
	python filteredResultCoverageMerger.py $outfile coverageResult.txt $bitThresh2 $covThresh
	echo "Run successful! Results in $outfile"
else
	echo "Error: size of input is too large. Max number of sequences is $seqMax" > $outfile
	echo "Error: size of input is too large. Max number of sequences is $seqMax"
fi

rm coverageResult.txt
rm *.faaTEMPP
rm coverage.txt
rm temp.txt

