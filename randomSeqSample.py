#!/usr/bin/env python

# This script takes one of several fasta files as input
# and prints a ramdom sample of sequences to screen.
#
# Usage: ./randomSeqSample.py -n X <fasta-file>
#
# ...where "X" is an integer smaller then the number 
# of sequences in the fasta input file.

import argparse
import random
import sys

###########################################################################################
parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*", type=str, help="The name(s) of the fasta input file(s).")
parser.add_argument("-n", help="Number of sequences to sample", default=1)
args = parser.parse_args()
###########################################################################################

### From BioPython and http://stackoverflow.com/questions/7654971/parsing-a-fasta-file-using-a-generator-python ###
### Read the fasta file(s) ###
def read_fasta(infile):
	name, seq = None, []
	for line in infile:
		if line.startswith(">"):
			if name: yield (name, ''.join(seq))
			name, seq = line, []
		else:
			line = line.rstrip()
			seq.append(line)
	if name: yield (name, ''.join(seq))


### Print random sample of sequences to STDOUT ###
def sample():
	sampleDict = {}
	for infile in args.files:
		with open(infile) as my_file:
			for name, seq in read_fasta(my_file):
				sampleDict[name] = seq
	# Make sure that the number of sequences in the 
	# input file(s) are greater then the desired sample.
	try:
		randomList = random.sample(sampleDict.items(), int(args.n))
	except ValueError:
		sys.exit("[Error] The requested random sample is greater than the total number of sequences.")
	for item in randomList:
		print item[0].rstrip("\n")
		print item[1]
	
				
if __name__ == "__main__":
	
	sample()
