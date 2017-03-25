ngs
===

Tools for handeling and analysing High throughput sequencing data


Usage:		pairSeq.py <inFile_1> <inFile_2>

Description:	Separates paired end Illumina sequences into pairs 
		and singlets. Also checks if the output sequences 
		are in the same order in the resulting output files.

Input: 		Two files with sequences in fastq format (inFile_1 and inFile_2).
		
Output: 	'outpair1.fastq' and 'outpair2.fastq' contains the 
		sequence pairs. Sequences in 'outpair1.fastq' originates 
		from the first imput file, and 'outpair2.fastq' from 
		the other. 'outSingles1.fastq' and 'outSingles2.fastq' 
		contains the singglet sequences from each input file.


* Hej Paula!

