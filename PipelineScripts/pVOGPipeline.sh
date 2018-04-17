#!/bin/bash
#Bash script that takes an input fasta file of viral protein sequences and searches the query sequences against a database of pVOG profiles. 
#After the search, hits are reported with target profiles. If reporting code = 1, then only hits above the trusted cutoff are reported. If the
#reporting code = 2, then optimized query and target coverages are used as additionally reporting thresholds when the bitscore is below the trusted cutoff
#to run: ./pVOGPipeline <inputFile> <reportingCode>

#PARAMETERS
outfile="$1.csv" #outputfile name is <inputFilename>.csv
databaseName=pVOGDB/pVOGDataBase #path to profile database
hmmPath=/local/vol00/shared/bin
queryName=$1  #input filename
ethresh=10e-8 #evalue threshold
if [ $2 -eq 2 ]
then
    queryCovThresh=50 #query coverage threshold for reporting
    tarCovThresh=50 #target coverage threshold for reporting
else
    queryCovThresh=0 #query coverage threshold for reporting
    tarCovThresh=0 #target coverage threshold for reporting
fi
seqMax=1001 #max number of sequences allowed in input fasta file
delimiter=, #delimiter for output file
validCode=77
seqs=$(cat $1 | grep -c ">") #calculate number of sequences in input file
logFile="$1.log" #log file
rm $logFile


if [ $seqs -lt $seqMax ] #if number of sequences < seqMax
then
	python fastaSplit.py $1 #split all fasta files in input into separate files
	if [ $validCode -eq $? ]
	then
        $hmmPath/hmmscan --tblout $outfile -E $ethresh $databaseName $queryName > junk.txt
		 if [ $? -eq 0 ] #check exit code of hmmscan
		 then 
            python outputFilter.py $outfile $delimiter
            rm junk.txt
            if [ "$(tail -n 1 $outfile)" = "CORRECT" ]   #check that the python script can to completion
            then
                sed -i '$ d' coverage.txt #remove last 2 lines of file
                sed -i '$ d' coverage.txt
                sed -i '$ d' $outfile #remove last line of file
                ./hmmAlign.sh coverage.txt
                if [ $(ls -lR *.faaTEMPP | wc -l) -eq $seqs ] #check that the number of alignments is the same as the number of sequences
                then
                    python filteredResultCoverageMerger.py $outfile coverageResult.txt $queryCovThresh $tarCovThresh
                    if [ "$(tail -n 1 $outfile)" = "CORRECT" ] #check that the python script can until completion
                    then
                        echo "Run successful! Results in $outfile"
                        sed -i '$ d' $outfile #remove last line of file
                    else
                        rm $outfile
                        echo "Error in performing final post processing" > $outfile
                        echo "Error in performing final post processing" > $logFile
                    fi
                else
                    rm $outfile
                    echo "Error in performing alignments, check hmmer installation and HMMAlign as well as pVOG .hmm profiles" > $outfile
                fi
            else
                rm $outfile
                echo "Post Processing Error" > $outfile
                echo "Post Processing Error" > $logFile
            fi
        else
            echo "Error in running hmmscan, check hmmer installation, database files, and fasta input format" > $outfile
            echo "Error in running hmmscan, check hmmer installation, database files, and fasta input format" > $logFile
        fi
    else
        echo "Error in splitting fasta files, check input filetype. Only FASTA format files are allowed as valid input" > $outfile
        echo "Error in splitting input file, check input filetype. Only FASTA format files are allowed as valid input" > $logFile
    fi
else
	echo "Error: size of input is too large. Max number of sequences is $seqMax" > $outfile
	echo "Error: size of input is too large. Max number of sequences is $seqMax" > $logFile
fi

##remove temporary files
rm coverageResult.txt
rm *.faaTEMPP
rm coverage.txt
rm temp.txt

