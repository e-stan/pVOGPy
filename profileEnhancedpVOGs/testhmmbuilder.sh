#!/bin/bash
masterInfile=$1
msaFileEnding="_MSA.faa"
hmmFileEnding=".hmm"
while read -r infile
do
    infile2=${infile::-4}
    echo $infile2
	VOGName=$(echo $infile2 | cut -f 2 -d'/')
    outfileMuscle=$infile2$msaFileEnding
    outfileHmm=$infile2$hmmFileEnding

    /local/vol00/shared/bin/muscle -in $infile -out $outfileMuscle
    /local/vol00/shared/bin/hmmbuild -n $VOGName --cpu 1 $outfileHmm $outfileMuscle
done < "$masterInfile"

