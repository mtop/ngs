#!/usr/bin/env python

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
														        
parser = argparse.ArgumentParser(prog="parseCDHITresult.py")
parser.add_argument("-v", "--verbose", action="store_true", help="Be more verbose")
parser.add_argument("cdhitfile", type=str, help="The name of the CH-HIT results file [*.clust] to analyse.")
args = parser.parse_args()


class Cluster(object):
	def __init__(self, cluster, result):
		self.name = cluster
		self.result = result
		self.parse_result()
	
	def get_name(self):
		return self.name

	def get_result(self):
		return self.result

	def get_results_numbers(self):
		return self.r_number_list
	
	def get_results_length(self):
		return self.r_length_list

	def get_results_seq_names(self):
		return self.r_seq_name_list

	def get_strains(self):
		return self.r_strain_list

	def get_identities(self):
		return self.r_identity_list

	def parse_result(self):
		self.r_number_list = []
		self.r_length_list = []
		self.r_seq_name_list = []
		self.r_strain_list = []
		self.r_identity_list = []
		for line in self.result.split("\n"):
			# Skip empty lines
			if not line.strip():
				pass
			else:
				# Number for the result in this cluster
				self.r_number_list.append(line.split()[0])
				# Length of the sequence in this result
				self.r_length_list.append(line.split()[1].split("nt,")[0])
				# Sequence name
				self.r_seq_name_list.append(line.split()[2].split("...")[0].lstrip(">"))
				# Strain (+ or -)
				if line.split()[3] == "*":
					self.r_strain_list.append("REF")
					self.r_identity_list.append("REF")
				else:
					self.r_strain_list.append(line.split()[4].split("/")[0])
					# Identity
					self.r_identity_list.append(float(line.split()[4].split("%")[0].split("/")[1]))
	

def readCDHITtable(infile):
	cluster, result = None, []
	for line in infile:
		if line.startswith(">"):
			if cluster: yield (cluster, ''.join(result))
			cluster, result = line, []
		else:
#			line = line.rstrip()
			result.append(line)
	if cluster: yield (cluster, ''.join(result))


def main():
	clusters = []
	with open(args.cdhitfile) as infile:
		for cluster, stuff in readCDHITtable(infile):
			clusters.append(Cluster(cluster, stuff))
	
	for cluster in clusters:
#		print cluster.get_result()
		print cluster
		break


if __name__ == "__main__":
    main()
