#!/bin/bash
#Bash script that takes an input fasta file of viral protein sequences and searches the query sequences against a database of pVOG profiles. 
#After the search, hits are reported with target profiles scoring above a bitscore of 55 and a significance greater than an evalue of 10e-12
#to run: ./pVOGPipeline <inputFile>
databaseName=pVOGDB/pVOGDataBase/AllvogHMMprofiles
inFile=$1
delimiter=,
echo "#Query Name,Target,Coverage" >> coverageResult.txt
while read line
do
	arr=( ${line//,/ })
	/local/vol00/shared/bin/hmmalign -o temp.txt pVOGDB/AllvogHMMprofiles/${arr[1]}.hmm ${arr[0]}.faaTEMPP
	python testAlignmentProcessor.py temp.txt
	queryCov=$?
	python targetCoverageCalculator.py temp.txt
	targetCov=$?
	echo "${arr[0]}$delimiter${arr[1]}$delimiter$queryCov$delimiter$targetCov" >> coverageResult.txt
done < $inFile




