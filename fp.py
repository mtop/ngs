#!/usr/bin/env python

import sys
import argparse

###########################################################################################
parser = argparse.ArgumentParser()
parser.add_argument("--length", help="Print length of sequences to STDOUT.", action="store_true")
parser.add_argument("--longest", help="Print the longest sequence to STDOUT, and its length to STDERR.", action="store_true")
parser.add_argument("--duplicates", help="Find sequences in common between two or more fasta files, or duplicates in a single file.", action="store_true")
parser.add_argument("--unique", help="Print the unique sequence in one or several fasta files.", action="store_true")
parser.add_argument("--remove", help="Remove duplicates in one or several fasta files.", action="store_true")
parser.add_argument("--header", help="Print sequence headers (use together with --length).", action="store_true")
parser.add_argument("files", nargs="*", type=str, help="The names of the input files.")
parser.add_argument("--seq", help="Print the sequence for the provided header")
parser.add_argument("--grep", help="Use headers in file as arguments for --seq", nargs=1)
args = parser.parse_args()
###########################################################################################



class fastaSeq(object):
	def __init__(self, name, seq):
		self.name = name[1:].rstrip()
		self.seq = seq

	def header(self):
		return self.name

	def sequence(self):
		return self.seq

	def length(self):
		return len(self.seq)

	def __str__(self):
		return ">%s\n%s" % (self.name, self.seq)



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

### Print the length of sequences ###
def length():
	for infile in args.files:
		with open(infile) as my_file:
			for name, seq in read_fasta(my_file):
				fs = fastaSeq(name, seq)
				if args.header == True:
					print fs.length(), fs.header()
				else:
					print fs.length()

### Print longest sequence to STDOUT, and the length to STDERR ###
def longest():
	length = 0
	for infile in args.files:
		with open(infile) as my_file:
			for name, seq in read_fasta(my_file):
				fs = fastaSeq(name, seq)
				if fs.length() > length:
					length = fs.length()
					longest_seq = fs
				else:
					continue
	print longest_seq
	print >> sys.stderr, length
				

### Print sequences in common between two or more 
### fasta files, duplicates in a single file, or 
### unique sequences.
def duplicates_or_unique():
	sequence_dict = {}
	for infile in args.files:
		with open(infile) as my_file:
			for name, seq in read_fasta(my_file):
				fs = fastaSeq(name, seq)
				if fs.sequence() in sequence_dict:
					sequence_dict[fs.sequence()].append(fs.header())
				else:
					sequence_dict[fs.sequence()] = [fs.header()]
	for sequence in sequence_dict:
		### Duplicated sequences ###
		if args.duplicates == True:
			if len(sequence_dict[sequence]) > 1:
				combi_header = ""
				for header in sequence_dict[sequence]:
					combi_header = combi_header.lstrip() + " " + header.rstrip()
				print combi_header
				print sequence
		
		### Unique sequences ###
		if args.unique == True:
			if len(sequence_dict[sequence]) == 1:
				for header in sequence_dict[sequence]:
					print header.rstrip()
					print sequence

		### Remove duplicates ###
		# Note: Will only remove identical sequences, not identical fasta headers
		if args.remove == True:
			print sequence_dict[sequence][0].rstrip()
			print sequence

def print_sequence():
	for infile in args.files:
		with open(infile) as my_file:
			for name, seq in read_fasta(my_file):
				fs = fastaSeq(name, seq)
				if args.seq == fs.header():
					print fs

#def print_sequences():
#	for infile in args.files:
#		with open(infile) as my_file:
#			for name, seq in read_fasta(my_file):
#				try:
#					for grep_file in args.grep:
#						with open(grep_file) as infile:
#							for header in infile.readlines():
#								print name[1:].rstrip(), header
#								if name == header:
#									print header
#				except:
#					pass

def grep():
	for grep_file in args.grep:
		with open(grep_file) as infile:
			for header in infile.readlines():
				print header
				print_sequence(header)


if __name__ == "__main__":
	
	if args.length == True:
		length()

	if args.longest == True:
		longest()

	if args.duplicates == True:
		duplicates_or_unique()

	if args.unique == True:
		duplicates_or_unique()

	if args.remove == True:
		duplicates_or_unique()
	
	if args.seq:
		print_sequence()
