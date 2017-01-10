#!/usr/bin/env python

# 1). Reads a sequence in fasta format from file. 
# 2). Calculates the gc ratio in a window.
# 3). Plots the result using R.

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*", type=str, help="The names of the input files.")
parser.add_argument("-w", "--window", help="Defines size of window for calculating gc ratio.", type=int, default=1000)
args = parser.parse_args()

class fastaSeq(object):
	def __init__(self, name, seq):
		self.name = name
		self.seq = seq

	def header(self):
		return self.name[1:]

	def sequence(self):
		return self.seq

	def length(self):
		return len(self.seq)

	def __str__(self):
		return "%s%s" % (self.name, self.seq)

	def __getitem__(self):
		return self.seq

	def get_gc(self):
		A = 0
		T = 0
		C = 0
		G = 0
		IUPAC = 0
		tot = 0.0
		tot_gc = 0
		frag_list = []
		start = 0
		end = args.window - 1
#		print start, end
#		print self.sequence()
#		print self.seq[0:10], self.seq[10:20]
#		while tot < args.window:
		for base in self.seq:
			if base.lower() == "a":
				A += 1
			if base.lower() == "t":
				T += 1
			if base.lower() == "c":
				C += 1
			if base.lower() == "g":
				G += 1
				tot_gc += 1
			else:
				IUPAC += 1
			tot += 1

			if tot == args.window:
				yield ((G+C)/tot)*100
				A = 0
				T = 0
				C = 0
				G = 0
				IUPAC = 0
				tot = 0.0
#				yield G+C



#		return self.sequence()[start:end]

#		for section in self.sequence():
#			fragment = section[start:end]
#			start = start + args.window
#			end = start + args.window - 1 
#			frag_list.append(len(fragment))
#			print start, end
#		return frag_list

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


def main():
	for infile in args.files:
		with open(infile) as my_file:
			for name, seq in read_fasta(my_file):
				print name.rstrip("\n")
				my_seq = fastaSeq(name, seq)
				for gc_ratio in my_seq.get_gc():
					print gc_ratio


if __name__ == "__main__":
	main()
	
