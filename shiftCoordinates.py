#!/usr/bin/env python

from __future__ import print_function
import sys

try:
    import argparse
except ImportError:
	sys.stderr.write("[Error] The python module 'argparse' is not installed\n")
	sys.stderr.write("[--] Would you like to install it now using 'sudo easy_install' [Y/N]? ")
	answer = sys.stdin.readline()
	if answer[0].lower() == "y":
		sys.stderr.write("[--] Running 'sudo easy_install argparse'\n")
		from subprocess import call
		call(["sudo", "easy_install", "argparse"])
	else:
		sys.exit("[Error] Exiting due to missing dependency 'argparser'")
														        
parser = argparse.ArgumentParser(prog="ADD-SCRIPT-NAME-HERE")
parser.add_argument("gbf", metavar='Genbank file')
parser.add_argument("-v", "--verbose", action="store_true", help="Be more verbose")
parser.add_argument("-s", "--shift",  help="Number of bases to shift the features of the genebank file", default=0, type=int)
args = parser.parse_args()

def shift(line, feature):
	# Isolate the actuall coordinates
	coordinates = line.rsplit()[1].replace("complement(", "").replace(")", "")
	start = int(coordinates.split("..")[0]) + args.shift
	stop = int(coordinates.split("..")[1]) + args.shift
	if "complement" in line:
		print("     %s            complement(%s..%s)" % (feature, start, stop))
	else:
		print("     %s            %s..%s" % (feature, start, stop))


def main():
	### Remove the next line and add your own code instead ###
	gbf = open(args.gbf)
	for line in gbf.readlines():
		if "gene" in line and ".." in line:
			shift(line, "gene")
		elif "CDS" in line and ".." in line:
			shift(line, "CDS")
#			# Isolate the actuall coordinates
#			coordinates = line.rsplit()[1].replace("complement(", "").replace(")", "")
#			start = int(coordinates.split("..")[0]) + args.shift
#			stop = int(coordinates.split("..")[1]) + args.shift
#			if "complement" in line:
#				print("     gene            complement(%s..%s)" % (start, stop))
#			else:
#				print("     gene            %s..%s" % (start, stop))
		else:
			print(line, end="")

if __name__ == "__main__":
    main()
