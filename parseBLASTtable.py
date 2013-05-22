#!/usr/bin/env python

import sys

table = sys.argv[1]

table_file = open(table, "r")

pt_result = {}
bact_result = {}

for line in table_file.readlines():
	if line[:6] == "contig":
#		print line.split()[0].replace(",", "" )			# Devel.
		if "|ref|" in line.split()[1]:
			pt_result[line.split()[0].replace(",", "" )] = line.split()[1]
		else:
			bact_result[line.split()[0].replace(",", "" )] = line.split()[1]
			
for key in pt_result:
	lineNr = 1
#	key.split(".")
	gff_file = key.split(".")[0] + ".gff"
	for line in open(gff_file, "r").readlines():
		if lineNr == key.split(".")[1]:
			print line.split()[3], line.split()[4]
		lineNr =+1

	print key


	
print pt_result
print bact_result
