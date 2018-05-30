#!/bin/bash
#Bash script to perform alignment of sequences given individually in fasta format named by the accessions in inFile followed by .faaTEMPP. 
#The script uses hmmalign to align each protein to the corresponding hmm given in inFile. Then the python scripts queryCoverageCalculator 
#and targetCoverageCalculator calculate the respective coverages of that alignment. This information is then written the file 
#coverageResult.txt 
databaseName=pVOGDB/EnhancedpVOG/AllvogHMMprofiles/
inFile=$1
UUID=$2
delimiter=,
echo "#Query Name,Target,Coverage" >> coverageResult.txt$UUID
while read line
do
	arr=( ${line//,/ })
	python hmmAlignHelper.py $line $databaseName $UUID
	python queryCoverageCalculator.py temp.txt$UUID
	queryCov=$?
	python targetCoverageCalculator.py temp.txt$UUID
	targetCov=$?
	echo "${arr[0]}$delimiter${arr[1]}$delimiter$queryCov$delimiter$targetCov" >> coverageResult.txt$UUID
done < $inFile




