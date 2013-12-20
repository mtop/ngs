#!/usr/bin/env python

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--evalue", help="Set the cutoff e-value", default="1.0")
parser.add_argument("-i", "--infile", help="Set input file", nargs="*")
parser.add_argument("-g", "--group", help="Set the organism group to parse the result for [BAC, DIA, CHY, OOM]", nargs="*", default="BAC" )
args = parser.parse_args()

table_file = open(args.infile[0], "r")
bact_result = {}
diatom_result = {}
chytrid_result = {}
oomyc_result = {}


def main():
	# Extract best hit for each gene prediction, and store them in different dictionaries.
	for line in table_file.readlines():
		if line.split()[1][:4] == "BAC_" or line.split()[1][:4] == "CYA_":
			# Make first selection based on e-value for the BLAST match.
			if float(line.split()[10]) < float(args.evalue):
				try:
					bact_result[line.split()[0]] += 1
				except KeyError:
					bact_result[line.split()[0]] = 1

		if line.split()[1][:4] == "DIA_":
			# Make first selection based on e-value for the BLAST match.
			if float(line.split()[10]) < float(args.evalue):
				try:
					diatom_result[line.split()[0]] += 1
				except KeyError:
					bact_result[line.split()[0]] = 1

		if line.split()[1][:4] == "CHY_":
			# Make first selection based on e-value for the BLAST match.
			if float(line.split()[10]) < float(args.evalue):
				try:
					chytrid_result[line.split()[0]] += 1
				except KeyError:
					bact_result[line.split()[0]] = 1

		if line.split()[1][:4] == "OOM_":
			# Make first selection based on e-value for the BLAST match.
			if float(line.split()[10]) < float(args.evalue):
				try:
					oomyc_result[line.split()[0]] += 1
				except KeyError:
					oomyc_result[line.split()[0]] = 1
	
	# Print result to STDOUT
	if args.group == "BAC":
		for key in bact_result:
			print key
	if args.group == "DIA":
		for key in diatom_result:
			print key
	if args.group == "CHY":
		for key in chytrid_result:
			print key
	if args.group == "OOM":
		for key in oomyc_result:
			print key


if __name__ == "__main__":
	main()
