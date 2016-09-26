#!/usr/bin/env python

# Usage:	pairSeq.py <inFile_1> <inFile_2> "/"
#
# Description:	Separates paired end Illumina sequences into pairs 
#		and singlets. Also checks if the output sequences 
#		are in the same order in the resulting output files.
#
# Input: 	Two files with sequences in fastq format (inFile_1 and inFile_2).
#		
# Output: 	'outpair1.fastq' and 'outpair2.fastq' contains the 
#		sequence pairs. Sequences in 'outpair1.fastq' originates 
#		from the first imput file, and 'outpair2.fastq' from 
#		the other. 'outSingles1.fastq' and 'outSingles2.fastq' 
#		contains the singglet sequences from each input file.
#
# Citation: 	If you use this version of the program, please cite;
#   		Mats T"opel (2013) Open Laboratory Notebook. www.matstopel.se
#
#
#   Copyright (C) 2013 Mats Topel.
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
#
# TODO: Make sure that output is written to PWD.	
#



import sys
import gc
#import io
from itertools import izip

# Identify the input files
f1 = sys.argv[1]
f2 = sys.argv[2]

# Identify the sequence ID's
def getSeqId():
	with open(f1, 'r') as f:
		first_line = f.readline()
		return first_line[0:3]
seqID = getSeqId()


try:
	delim = sys.argv[3].strip('"\'')	# Perhaps redundant to try to remove " and ' characters.
except:
	delim = ' '


# pairF1 = "%s.pair_1.fastq.txt" % f1		# Redundant.
# pairF2 = "%s.pair_2.fastq.txt" % f2		# Redundant.


class sequence(object):
	def __init__(self):
		self.Id = None
		self.seq = None
		self.qid = None
		self.qual = None

	def setId(self, line):
		self.Id = line

	def setSeq(self, line):
		self.seq = line

	def setQid(self, line):
		self.qid = line
	
	def setQual(self, line):
		self.qual = line

	def getId(self):
		return self.Id

	def getPairId(self):
		return self.Id.split(delim)[0]

	def getSeq(self):
		return self.seq

	def getQid(self):
		return self.qid

	def getQual(self):
		return self.qual

	def __str__(self):
		return "%s%s%s%s" % (self.Id, self.seq, self.qid, self.qual)



class fastqFile(file):
	def __init__(self, name, mode):
		file.__init__(self, name, mode)

	def readParts(self, partSize=256):
		while True:
			data = self.read(partSize)
			if not data:
				break
			yield data
	
	def Ids2Dict(self):
		# Reads the file, one sequence object at the time, and identifies
		# the sequence identifiers. The identifiers
		# are then split at the indicated delimiter, and the first
		# part is stored in a dictionary.
		seqIdDict = {}

		for seq in self.getSeqs():
			seqIdDict[seq.getId().split(delim)[0]] = False
		return seqIdDict

	def cmpIds2Dict(self, fwDict, outPair, outSing, fileNr):
		# Compair the sequence id's in the second file to the 
		# once in file 1 (stored in a dictionary). Then write 
		# sequence information to output files.

		pair = False
		if fileNr == 1:
			pair = True

		for seq in self.getSeqs():
			seqId = seq.getId().split(delim)[0]
			try:
				if fwDict[seqId] == pair:
					# Set output file to be the "pairs" file.	
					out = outPair
					# Set seqId in dict to "True" to indicate 
					# that a pair has been found.
					fwDict[seqId] = True
				else:
					# Set output file to the "singlets" file.
					out = outSing
			except KeyError:
				# Insert a key from the second file in the 
				# dictionary if it's not allready there.
				fwDict[seqId] = False
				out = outSing

			out.write(str(seq))

	def getSeqs(self):
		with self as f:
			for line in f:
#				if line[0:3] == getSeqId():
				if line[0:3] == seqID:
					# Create a sequence object.
					seq = sequence()
					seq.setId(line)
				elif seq.getId() != None and seq.getSeq() == None:
					seq.setSeq(line)
				elif seq.getId() != None and seq.getSeq() != None and seq.getQid() == None:
					seq.setQid(line)
				elif seq.getId() != None and seq.getSeq() != None and seq.getQid() != None and seq.getQual() == None:
					seq.setQual(line)

					yield seq

def compSeqOrder(outPair_1, outPair_2):
	count = 0
	with outPair_1 as f1:
		with outPair_2 as f2:
			for (fwSeq, rwSeq) in izip(f1.getSeqs(), f2.getSeqs()):
				if fwSeq.getPairId() == rwSeq.getPairId():
					count += 1
			return count

def noFileExt(fileName):
	if fileName[-6:].lower() == ".fastq":
		name = fileName[:-6]
		ext = fileName[-6:]
		return name, ext

def genFileName(inFile, outType):
	name = noFileExt(inFile)[0]
	ext = noFileExt(inFile)[1]
	newName = name + outType + ext
	return newName

#def getSeqId():
#	with open(f1, 'r') as f:
#		first_line = f.readline()
#		return first_line[0:3]

					
def main():
	# Generate fastqFile objects to read from and write to.
	inFile1 = fastqFile(f1, 'r')		# First sequence file to read from
	inFile2 = fastqFile(f2, 'r')		# Second sequence file to read from
	outPair_1 = fastqFile(genFileName(f1, ".Pair"), 'w')	
	outPair_2 = fastqFile(genFileName(f2, ".Pair"), 'w')
	outSing_1 = fastqFile(genFileName(f1, ".Singles"), 'w')
	outSing_2 = fastqFile(genFileName(f2, ".Singles"), 'w')

	# Create dictionary containing sequence id's from first file (info. on direction removed).
	print "[--] Building initial dictionary of sequence id's in first file."
	fwDict = inFile1.Ids2Dict()			

	# Release memory if possible
	print "[--] Attempting memory garbage collection"
	gc.collect()

	# Compair Id's in file 2 to the once in the dictionary, then write to outfiles.
	print "[--] Comparing id's in second file to the dictionary."
	inFile2.cmpIds2Dict(fwDict, outPair_2, outSing_2, 2)

	# Compair Id's in file 1 to the once in the dictionary, then write to outfiles.
	print "[--] Comparing id's in first file to the dictionary"
	inFile1 = fastqFile(f1, 'r')		# Open the first file again
	inFile1.cmpIds2Dict(fwDict, outPair_1, outSing_1, 1)

	# Check if sequences in the "pair" files are in the same order
	outPair_1 = fastqFile(genFileName(f1, ".Pair"), 'r')              # Change name of file later
	outPair_2 = fastqFile(genFileName(f2, ".Pair"), 'r')              # Change name of file later

	print "[--] Check if sequences in 'pair' files are in the same order"

	print "[op] %s sequnce pairs are in order" % compSeqOrder(outPair_1, outPair_2)


if __name__ == "__main__":
	main()
