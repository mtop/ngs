#!/usr/bin/env python

import sys
import argparse

###########################################################################################
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--length", help="Print length of sequences to STDOUT", action="store_true")
parser.add_argument("files", nargs="*", type=str, help="The names of the input files")
args = parser.parse_args()
###########################################################################################


class fastaSeq(object):
	def __init__(self, header, sequence):
		self.header = header
		self.sequence = sequence

	def length(self):
		return len(self.sequence)

	def __str__(self):
		return "%s%s" % (self.header, self.sequence)



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

### Print length of sequences ###
def length():
	for infile in args.files:
		with open(infile) as my_file:
			for name, seq in read_fasta(my_file):
				fs = fastaSeq(name, seq)
				print fs.length()


if __name__ == "__main__":

	if args.length == True:
		length()


