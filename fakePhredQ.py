#!/usr/bin/env python

import sys

class fastaSeq(object):
	def __init__(self, name, seq):
		self.name = name
		self.seq = seq

	def header(self):
		return self.name[1:].rstrip("\n")

	def sequence(self):
		return self.seq
	
	def quality(self):
		qual = ""
		for letter in self.sequence():
			qual += "Z"
		return qual

	def length(self):
		return len(self.seq)

	def __str__(self):
		return "%s%s" % (self.name, self.seq)



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


def main():
	infile = sys.argv[1]
	with open(infile) as my_file:
		for name, seq in read_fasta(my_file):
			fs = fastaSeq(name, seq)
			print fs.header()
			print fs.sequence()
			print "+"
			print fs.quality()


if __name__ == "__main__":
	main()
