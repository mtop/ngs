#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2014 Mats Töpel. mats.topel@bioenv.gu.se
#
#   Citation: If you use this version of the program, please cite;
#   Mats Töpel (2014) Open Laboratory Notebook. www.matstopel.se
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import argparse

###########################################################################################
parser = argparse.ArgumentParser()
parser.add_argument("--length", help="Print length of sequences to STDOUT.", action="store_true")
parser.add_argument("--longest", help="Print the longest sequence to STDOUT, and its length to STDERR.", action="store_true")
parser.add_argument("--duplicates", help="Find sequences in common between two or more fasta files, or duplicates in a single file.", action="store_true")
parser.add_argument("--unique", help="Print the unique sequence in one or several fasta files.", action="store_true")
parser.add_argument("--remove", help="Remove duplicated sequences in one or several fasta files.", action="store_true")
parser.add_argument("--header", help="Print sequence headers (use together with --length).", action="store_true")
parser.add_argument("--filter_length", help="Print sequence longer than [threshold] to screen.", default=0)
parser.add_argument("files", nargs="*", type=str, help="The name of the input file.")
parser.add_argument("--seq", help="Print the sequence for the provided header")
parser.add_argument("--grep", help="Use headers in file as arguments for --seq", nargs=1)
parser.add_argument("--gc", help="Calculate the GC ratio for sequences", action="store_true")
parser.add_argument("--gaps", help="Count number of gap characters", action="store_true")
args = parser.parse_args()
###########################################################################################

#seq_dict = {}

###########################################################################################

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
	
	def get_gc(self):
		self.a = self.seq.lower().count("a")
		self.t = self.seq.lower().count("t")
		self.c = self.seq.lower().count("c")
		self.g = self.seq.lower().count("g")
		self.gc_count = self.g + self.c
		self.gc_ration = (float(self.gc_count) / self.length()) * 100
		return ("%.1f" % self.gc_ration) + "%"
	
	def get_gaps(self):
		self.n = self.seq.lower().count("n")
		self.dash = self.seq.lower().count("-")
#		self.ratio = (self.n + self.dash) / self.length()
		return self.n, self.dash, self.length()
		

	def __str__(self):
		return "%s\n%s" % (self.name, self.seq)


### From BioPython and http://stackoverflow.com/questions/7654971/parsing-a-fasta-file-using-a-generator-python ###
### Read the fasta file(s) ###
def read_fasta(infile):
	name, seq = None, []
	for line in infile:
		if line.startswith(">"):
			if name: yield (name.split()[0], ''.join(seq))
			name, seq = line.split()[0], []
		else:
			line = line.rstrip()
			seq.append(line)
	if name: yield (name.split()[0], ''.join(seq))


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
					print ">", header.rstrip()
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
#				if args.seq in fs.header():			# Fubar
#				if args.seq + '\n' == fs.header():
				if args.seq == fs.header():
					print fs


def filter_length():
	# Extract sequences longer then a certain threshold
	for infile in args.files:
		with open(infile) as my_file:
			for name, seq in read_fasta(my_file):
				fs = fastaSeq(name, seq)
				if int(fs.length()) >= int(args.filter_length):
					print fs

def grep():
	seq_dict = {}
	with open(args.grep[0]) as grep_file: 
		for infile in args.files:				
			with open(infile) as fasta_file:
				for name, seq in read_fasta(fasta_file):
					seq_dict[name.lstrip(">")] = seq
		for header in grep_file.readlines():	
			try:
				print ">" + header + seq_dict[header.split()[0]]
			except KeyError as e:
				pass

def gc():
	for infile in args.files:
		with open(infile) as my_file:
			print "GC			Sequence"
			for name, seq in read_fasta(my_file):
				fs = fastaSeq(name, seq)
				print fs.get_gc() + "\t" + fs.header().rstrip()

def gaps():
	n = 0
	dash = 0
	length = 0
	for infile in args.files:
		with open(infile) as my_file:
			for name, seq in read_fasta(my_file):
				fs = fastaSeq(name, seq)
				result = fs.get_gaps()
				n += result[0]
				dash += result[1]
				length += result[2]
				ratio = (n + dash) / length
#				print n, dash, ratio, length
	print "N: %s \n-: %s \nRatio: %s \nTotal length: %s" % (n, dash, ratio, length)
			

#def grep():
#	print args.grep
#	print args.files
#	grep_file = open(args.grep[0], "r")
#	fasta_file = open(args.files, "r")
#	for fasta_file in args.files:
#		fasta = open(fasta_file, "r")
#		for name, seq in read_fasta(fasta):
#			for header in grep_file.readlines():
#				fs = fastaSeq(name, seq)
#				if header == fs.header():
#					print fs



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

	if args.filter_length:
		filter_length()

	if args.grep:
		grep()

	if args.gc == True:
		gc()

	if args.gaps == True:
		gaps()
