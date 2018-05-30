#!/bin/bash
#Bash script that takes an input fasta file of viral protein sequences and searches the query sequences against a database of pVOG profiles. 
#After the search, hits are reported with target profiles. If reporting code = 1, then only hits above the trusted cutoff are reported. If the
#reporting code = 2, then custom query and target coverages are used. For reporting code =3, then no filtering is applied.
#to run: ./pVOGPipeline <inputFile> <reportingCode>


#generate UUID

UUID=$(cat /proc/sys/kernel/random/uuid)

#PARAMETERS
outfile="$1.csv" #outputfile name is <inputFilename>.csv
databaseName=pVOGDB/EnhancedpVOG/EnhancedProfilesFlattened #path to profile database
hmmPath=/local/vol00/shared/bin
queryName=$1  #input filename
#ethresh=10e-8 #evalue threshold
if [ $2 -eq 2 ]
then
    queryCovThresh=$3 #query coverage threshold for reporting
    tarCovThresh=$4 #target coverage threshold for reporting
    bitThresh=$5
    ethresh=$6
else
    queryCovThresh=0 #query coverage threshold for reporting
    tarCovThresh=0 #target coverage threshold for reporting
    bitThresh=0
    ethresh=1000
fi
seqMax=11001 #max number of sequences allowed in input fasta file
delimiter=, #delimiter for output file
validCode=77
seqs=$(cat $1 | grep -c ">") #calculate number of sequences in input file
logFile="$1.log$UUID" #log file


if [ $seqs -lt $seqMax ] #if number of sequences < seqMax
then
    $hmmPath/hmmscan --tblout $outfile $databaseName $queryName > junk.txt$UUID
     if [ $? -eq 0 ] #check exit code of hmmscan
     then
        python outputFilter.py $outfile $delimiter $UUID
        rm junk.txt$UUID
        if [ "$(tail -n 1 $outfile)" = "CORRECT" ]   #check that the python script can to completion
        then
            sed -i '$ d' coverage.txt$UUID #remove last 2 lines of file
            sed -i '$ d' coverage.txt$UUID
            sed -i '$ d' $outfile #remove last line of file
            python fastaSplit.py $1 $UUID #split all fasta files in input into separate files
            if [ $validCode -eq $? ]
	        then
                ./hmmAlign.sh coverage.txt$UUID $UUID
                if [ $? -eq 0 ] #check that coverages were calculated
                then
                    python filteredResultCoverageMerger.py $outfile coverageResult.txt$UUID $queryCovThresh $tarCovThresh $bitThresh $ethresh $2
                    if [ "$(tail -n 1 $outfile)" = "CORRECT" ] #check that the python script ran until completion
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
                echo "Error in splitting fasta files, check input filetype. Only FASTA format files are allowed as valid input" > $outfile
                echo "Error in splitting input file, check input filetype. Only FASTA format files are allowed as valid input" > $logFile
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
	echo "Error: size of input is too large. Max number of sequences is $seqMax" > $outfile
	echo "Error: size of input is too large. Max number of sequences is $seqMax" > $logFile
fi

##remove temporary files
rm coverageResult.txt$UUID
rm *.faaTEMPP$UUID
rm coverage.txt$UUID
rm temp.txt$UUID
rm access2id.txt$UUID

