#!/usr/bin/env python

# parseCLCinfo.py extracts information about individual 
# contigs from the output file created by the program 
# clc_mapping_info that is part of the CLC assembly cell package.
#
# ./parseCLCinfo.py -h

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("infile", nargs=1, type=str, help="Input files to parse")
args = parser.parse_args()

infile = open(args.infile[0], "r")
nr = None
mapped = None
sites = None
unambiguous = None
covered_0 = None
covered_1 = None
covered_2 = None
covered_3 = None
covered_0perc = None
covered_1perc = None
covered_2perc = None
covered_3perc = None
ave_cover = None
corrected = None

print 'Contig_nr', 'Mapped_reads', 'Sites', 'Unambiguous', 'Covered_0_times', 'Covered_0_times_%', 'Covered_1_times', 'Covered_1_times_%', 'Covered_2_times', 'Covered_2_times_%', 'Covered_3+_times', 'Covered_3+_times_%', 'Average_coverage', 'Corrected_coverage'

for line in infile.readlines():
	if not line:
		continue
	match = re.search('Contig [0-9]+ info:', line)
	if match:
		nr =  line.split()[1]
	match2 = re.search('Mapped reads', line)	
	if match2:
		mapped = line.split()[2]
	match3 = re.search('Sites', line)
	if match3:
		sites = line.split()[1]
	match4 = re.search('Unambiguous', line)
	if match4:
		unambiguous = line.split()[1]
	match5 = re.search('Covered    0  times', line)
	if match5:
		covered_0 = line.split()[3]
		covered_0perc = line.split()[4]
	match6 = re.search('Covered    1  time', line)
	if match6:
		covered_1 = line.split()[3]
		covered_1perc = line.split()[4]
	match7 = re.search('Covered    2  times', line)
	if match7:
		covered_2 = line.split()[3]
		covered_2perc = line.split()[4]
	match8 = re.search('Covered    3', line)
	if match8:
		covered_3 = line.split()[3]
		covered_3perc = line.split()[4]
	match9 = re.search('Average coverage', line)
	if match9:
		ave_cover = line.split()[2]
	match10 = re.search('Corrected', line)
	if nr != None and match10:
		corrected = line.split()[1]
		print nr, mapped, sites, unambiguous, covered_0, covered_0perc, covered_1, covered_1perc, covered_2, covered_2perc, covered_3, covered_3perc, ave_cover, corrected
