#!/usr/bin/env python

import argparse
import re

parser = argparse.ArgumentParser()
#parser.add_argument("-i", "--input", help="Input file to be prsed", action="store_true")
parser.add_argument("infile", nargs=1, type=str, help="Input files to parse")
parser.add_argument("outfile", nargs=1, type=str, help="Name of the output file")
args = parser.parse_args()


#print args.infile			# Devel.
#print args.outfile			# Devel.

class Contig(object):
	def __init__(self):
		self.nr = None
		self.mapped = None
	
	def setNr(self, nr):
		self.nr = nr
	def setMapped(self, value):
		self.Mapped = value

	def getNr(self):
		return self.nr
	def getMapped(self):
		return self.mapped



#class Infile(file):
#	def __init__(self, name, mode):
#		file.__init__(self, name, mode)
	
infile = open(args.infile[0], "r")
# Directory to store the contig stats in
result = {}


nr = None
mapped = None
sites = None
unambiguous = None
covered_0 = None
covered_1 = None
covered_2 = None
covered_3 = None
ave_cover = None

for line in infile.readlines():
	if not line:
		continue
	match = re.search('Contig [0-9]+ info:', line)
	if match:
		nr =  line.split()[1]
		continue
	match2 = re.search('Mapped reads', line)	
	if nr != None and match2:
		mapped = line.split()[2]
#		print nr, mapped			# Devel.
		continue
	match3 = re.search('Sites', line)
	if nr != None and mapped != None and match3:
		sites = line.split()[1]
#		print nr, mapped, sites		# Devel.
		continue
	match4 = re.search('Unambiguous', line)
	if nr != None and sites != None and match4:
		unambiguous = line.split()[1]
#		print nr, mapped, sites, unambiguous     # Devel.
	match5 = re.search('Covered    0  times', line)
	if nr != None and unambiguous != None and match5:
		covered_0 = line.split()[3]
		covered_0perc = line.split()[4]
#		print nr, mapped, sites, unambiguous, covered_0, covered_0perc     # Devel.
	match6 = re.search('Covered    1  time', line)
	if nr != None and covered_0 != None and match6:
		covered_1 = line.split()[3]
		covered_1perc = line.split()[4]
#		print nr, mapped, sites, unambiguous, covered_0, covered_0perc, covered_1, covered_0perc     # Devel.
	match7 = re.search('Covered    2  times', line)
	if nr != None and covered_1 != None and match7:
		covered_2 = line.split()[3]
		covered_2perc = line.split()[4]
#		print nr, mapped, sites, unambiguous, covered_0, covered_0perc, covered_1, covered_0perc, covered_2, covered_2perc # Devel.
	match8 = re.search('Covered    3', line)
	if nr != None and covered_2 != None and match8:
		covered_3 = line.split()[3]
		covered_3perc = line.split()[4]
#		print nr, mapped, sites, unambiguous, covered_0, covered_0perc, covered_1, covered_0perc, covered_2, covered_2perc, covered_3, covered_3perc  #Devel.
	match9 = re.search('Average coverage', line)
	if nr != None and covered_3 != None and match9:
		ave_cover = line.split()[2]
#		print nr, ave_cover 			# Devel.
	match10 = re.search('Corrected', line)
	if covered_3 != None and match10:
		corrected = line.split()[1]
		print nr, corrected
		



	








