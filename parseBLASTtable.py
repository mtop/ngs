#!/usr/bin/env python

import sys

table = sys.argv[1]
table_file = open(table, "r")
pt_result = {}
bact_result = {}
result = {}

# Extract best hit for each gene prediction, and store them in two dictionaries.
for line in table_file.readlines():
	if line[:8] == "# Query:":
		length = line.split()[3]
	if line[:6] == "contig":
		hit = [line.split()[1]]
		identity = line.split()[2]
		if "|ref|" in line.split()[1]:
#			pt_result[line.split()[0].replace(",", "" )] = hit #line.split()[1]
#			pt_result[line.split()[0].replace(",", "" )].append("Pt")
			result[line.split()[0].replace(",", "" )] = hit
			result[line.split()[0].replace(",", "" )].append("Pt")
			result[line.split()[0].replace(",", "" )].append(identity)
			result[line.split()[0].replace(",", "" )].append(length)
		else:
#			bact_result[line.split()[0].replace(",", "" )] = hit #line.split()[1]
#			bact_result[line.split()[0].replace(",", "" )].append("B")
			result[line.split()[0].replace(",", "" )] = hit
			result[line.split()[0].replace(",", "" )].append("B")
			result[line.split()[0].replace(",", "" )].append(identity)
			result[line.split()[0].replace(",", "" )].append(length)


# Find the start and stop positions of the gene prediction in the Pt contigs.
for key in result:
	gff_file = key.split(".")[0] + ".gff"
	for line in open(gff_file, "r").readlines():
		# Identify the right line in the *.gff file.
		if key.split(".")[1] == line.split()[9][5:].replace("\"", ""):
			start = line.split()[3]
			stop = line.split()[4]
#			result[key].append("Pt")
			result[key].append(start)
			result[key].append(stop)


#for key in bact_result:
#	gff_file = key.split(".")[0] + ".gff"
#	for line in open(gff_file, "r").readlines():
#		# Identify the right line in the *.gff file.
#		if key.split(".")[1] == line.split()[9][5:].replace("\"", ""):
#			start = line.split()[3]
#			stop = line.split()[4]
#			bact_result[key].append("B")
#			bact_result[key].append(start)
#			bact_result[key].append(stop)


print "# Contig_nr" + "\t" + "Pt/B" + "\t" + "% Id." + "\t" + "Length" +  "\t" + "Start" + "\t" + "Stop" + "\t" + "Model" + "\t" + "Match"
for key in sorted(result):
	print key.split(".")[0] + "\t" + result[key][1] + "\t" + result[key][2] + "\t" + result[key][3] + "\t" + result[key][4] + "\t" + result[key][5] + "\t" + key.split(".")[1] + "\t" + result[key][0]


	
