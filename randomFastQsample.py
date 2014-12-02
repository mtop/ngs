#!/usr/local/opt/python/bin/python2.7

# This script takes one or several fastq files as input
# and prints a ramdom sample of sequences to screen.
#
# Usage: ./randomFastQsample.py -n X <fastq-file>
#
# ...where "X" is an integer smaller then the number 
# of sequences in the fastq input file.

import argparse
import random
import sys
from Bio import SeqIO

###########################################################################################
parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*", type=str, help="The name(s) of the fastq input file(s).")
parser.add_argument("-n", help="Number of sequences to sample", default=1)
args = parser.parse_args()
###########################################################################################



### Print random sample of sequences to STDOUT ###
def sample():
	sampleDict = {}
	for infile in args.files:
		my_file = SeqIO.parse(infile, "fastq")
#		with SeqIO.parse(infile, "fastq") as my_file:
		for fastq_seq in my_file:
			sampleDict[fastq_seq.id] = fastq_seq
	# Make sure that the number of sequences in the 
	# input file(s) are greater then the desired sample.
	try:
		randomList = random.sample(sampleDict.items(), int(args.n))
	except ValueError:
		sys.exit("[Error] The requested random sample is greater than the total number of sequences.")
	for seq in randomList:
		print seq[1].format("fastq").rstrip("\n")
	
				
if __name__ == "__main__":
	
	sample()
