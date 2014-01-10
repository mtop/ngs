#!/usr/bin/env python

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--evalue", help="Include matches with an evalue < [evalue]", default="100.0")
parser.add_argument("-a", "--a_length", help="Include matches with an alignment length > [a-length] ", default="0")
parser.add_argument("-q", "--q_length", help="Include matches where the query sequence length is > [q-length]", default="0")
parser.add_argument("-p", "--percent", help="Minimum percentage of hits to as sequence from [group]", default="1")
parser.add_argument("-i", "--infile", help="Set input file", nargs="*")
parser.add_argument("-g", "--group", help="Set the organism group to parse the result for [BAC, DIA, CHY, OOM]", nargs="*", default="BAC" )
parser.add_argument("-t", "--grxxxoup", help="Set the organism group to parse the result for [BAC, DIA, CHY, OOM]", action="store_true")
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

	def setDIA(self):
		pass

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
				try:
					result.bact_result[line.split()[0]] += 1
				except KeyError:
					result.bact_result[line.split()[0]] = 1

		if line.split()[1][:4] == "DIA_":
			if selection(line, result):
				try:
					result.diatom_result[line.split()[0]] += 1
				except KeyError:
					result.diatom_result[line.split()[0]] = 1

		if line.split()[1][:4] == "CHY_":
			if selection(line, result):
#			if float(line.split()[10]) < float(args.evalue):
				try:
					result.chytrid_result[line.split()[0]] += 1
				except KeyError:
					result.chytrid_result[line.split()[0]] = 1
#				selected_matches += 1

		if line.split()[1][:4] == "OOM_":
			if selection(line, result):
#			if float(line.split()[10]) < float(args.evalue):
				try:
					result.oomyc_result[line.split()[0]] += 1
				except KeyError:
					result.oomyc_result[line.split()[0]] = 1
#				selected_matches += 1

	
	# Print result to STDOUT
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
				break
		except:
			raise
			sys.exit("[ Error ] Input file is not in the right format")
			
			
	

if __name__ == "__main__":
#	tests()
	main()
