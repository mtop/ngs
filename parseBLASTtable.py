#!/usr/bin/env python

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--evalue", help="Include matches with an evalue < [evalue]", default="100.0")
parser.add_argument("-a", "--a_length", help="Include matches with an alignment length > [a-length] ", default="0")
parser.add_argument("-q", "--q_length", help="Include matches where the query sequence length is > [q-length]", default="0")
parser.add_argument("-p", "--percent", help="Minimum percentage of hits to as sequence from [group]", default="1")
parser.add_argument("-i", "--infile", help="Set input file", nargs="*")
parser.add_argument("-g", "--group", help="Set the organism group to parse the result for [BAC, DIA, CHY, OOM, CONT]", nargs="*") #, default="NO_GROUP")
parser.add_argument("-t", "--test", help="Test if some subject sequences have any of the correct prefixes [BAC, DIA, CHY, OOM]", action="store_true")
#parser.add_argument("-v", "--verbose", help="Provide more verbose output", action="store_true")
args = parser.parse_args()

try:
	table_file = open(args.infile[0], "r")
except:
	sys.exit("[ Error ] No such file \'%s\'" % args.infile[0])
#table_file = open(args.infile[0], "r")
###bact_result = {}
###diatom_result = {}
###chytrid_result = {}
###oomyc_result = {}

class Result(object):
	def __init__(self):
		self.bact_result = {}
		self.diatom_result = {}
		self.chytrid_result = {}
		self.oomyc_result = {}
		self.best_match = {}

	def setBestMatch(self, line):
		try:
			# Test if a match with a better e-value has already been saved.
#			print self.best_match[line.split()[0]].split()[10]
			if float(self.best_match[line.split()[0]].split()[10]) > float(line.split()[10]):
				self.best_match[line.split()[0]] = line
		except KeyError:
			# Store line if no match has been saved before.
			self.best_match[line.split()[0]] = line

	def passedSelection(self, contig):
		try:
			i = self.bact_result[contig]
		except:
			i = 0
		try:
			j = self.diatom_result[contig]
		except:
			j = 0
		try:
			k = self.chytrid_result[contig]
		except:
			k = 0
		try:
			l = self.oomyc_result[contig]
		except:
			l = 0
		return i + j + k + l

def selection(line, result):
	if float(line.split()[10]) <= float(args.evalue)\
		and int(line.split()[3]) >= int(args.a_length)\
		and int(line.split()[12]) >= int(args.q_length):
		return True
	else:
		return False

def fraction(resultDict, contig, result):
	# Identify the number of contigs from the desired organism group
	i = resultDict[contig]
#	print i, "/", result.passedSelection(contig)
#	print (float(i)/result.passedSelection(contig))*100, contig
	if (float(i)/result.passedSelection(contig))*100 >= int(args.percent):
		return True
	else:
		return False
	
	

def main():
	result = Result()
	# Extract best hit for each gene prediction, and store them in different dictionaries.
	for line in table_file.readlines():
		if line.split()[1][:4] == "BAC_" or line.split()[1][:4] == "CYA_":
			if selection(line, result):
				# Test, then store best match (e-value).
				result.setBestMatch(line)
				try:
					result.bact_result[line.split()[0]] += 1
				except KeyError:
					result.bact_result[line.split()[0]] = 1

		if line.split()[1][:4] == "DIA_":
			if selection(line, result):
				# Test, then store best match (e-value).
				result.setBestMatch(line)
				try:
					result.diatom_result[line.split()[0]] += 1
				except KeyError:
					result.diatom_result[line.split()[0]] = 1

		if line.split()[1][:4] == "CHY_":
			if selection(line, result):
				# Test, then store best match (e-value).
				result.setBestMatch(line)
#			if float(line.split()[10]) < float(args.evalue):
				try:
					result.chytrid_result[line.split()[0]] += 1
				except KeyError:
					result.chytrid_result[line.split()[0]] = 1
#				selected_matches += 1

		if line.split()[1][:4] == "OOM_":
			if selection(line, result):
				# Test, then store best match (e-value).
				result.setBestMatch(line)
#			if float(line.split()[10]) < float(args.evalue):
				try:
					result.oomyc_result[line.split()[0]] += 1
				except KeyError:
					result.oomyc_result[line.split()[0]] = 1
#				selected_matches += 1

	
	# Print result to STDOUT
	if not args.group:
		for key in result.best_match:
			# Pring query sequence name, e-value, length of query sequence and name of best match.
			print result.best_match[key].split()[0] + "\t" \
				+ result.best_match[key].split()[10] + "\t"	\
				+ result.best_match[key].split()[12] + "\t"	\
				+ result.best_match[key].split()[1]
	else:
		for group in args.group:
			if group == "BAC":
				for key in result.bact_result:
					if fraction(result.bact_result, key, result):
						print key
			if group == "DIA":
				for key in result.diatom_result:
					if fraction(result.diatom_result, key, result):
						print key
			if group == "CHY":
				for key in result.chytrid_result:
					if fraction(result.chytrid_result, key, result):
						print key
			if group == "OOM":
				for key in result.oomyc_result:
					if fraction(result.oomyc_result, key, result):
						print key

			if group == "CONT":
				from collections import Counter
				dicts = [result.bact_result, result.chytrid_result, result.oomyc_result]
				c = Counter()
				for d in dicts:
					c.update(d)
				for key in dict(c):
					if fraction(dict(c), key, result):
						print key

def tests():
	# Test if some subject sequences have the correct prefix.
	for line in table_file.readlines():
		try:
			if line.split()[1][:4] == "BAC_" \
			or line.split()[1][:4] == "CYA_" \
			or line.split()[1][:4] == "DIA_" \
			or line.split()[1][:4] == "CHY_" \
			or line.split()[1][:4] == "OOM_":
				length = line.split()[12]
				sys.exit("[ -- ] Input file seems to be in the right format")
		except:
			raise
			sys.exit("[ Error ] Input file is not in the right format")
			
			
	

if __name__ == "__main__":
	if args.test == True:
		tests()
	main()
