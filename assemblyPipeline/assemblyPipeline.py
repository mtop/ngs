#!/usr/bin/env python

import subprocess
import os.path

### Use a flag to indicate the config file to use. Uses 'my.cfg' for now.

class Conf(object):
	# Variable values read from configuration file 
	# and misc. default values used during the analysis
	def __init__(self):
		import ConfigParser
		config = ConfigParser.RawConfigParser()
		config.read('my.cfg')

		self.f = config.get('fastx_trimmer', 'f')
		self.q = config.get('cutadapt', 'q')
		self.o = config.get('cutadapt', 'o')
		self.e = config.get('cutadapt', 'e')
		self.n = config.get('cutadapt', 'n')
		self.m = config.get('cutadapt', 'm')
		self.p = config.get('fastq_quality_filter', 'p')
		self.k = config.get('fastq_quality_filter', 'k')

		self.fxt = config.get('run', 'fastx_trimmer')
		self.ca = config.get('run', 'cutadapt')
		self.fqf = config.get('run', 'fastq_quality_filter')
		self.ps = config.get('run', 'pairSeq.py')

		self.fxt_ext = ".FXT"
		self.ca_ext = ".CA"
		self.fqf_ext = ".FQF"
		self.ps_ext = ".PS"

		# Create a list of file name variables (i.e. ["File1", "File2"]
		# Probably redundant.
		self.fileList = []
		# Create a list of actual file names
		self.fileNames = []
		for i in range(1, 11):
			name = "File" + str(i)
			try: 
				self.name = config.get('rawfiles', str(i))
				self.fileList.append(name)
				self.fileNames.append(self.name)
			except:
				continue

	def run_fxt(self):
		if self.fxt == "":
			return False
		if self.fxt.lower()[0] == 'y' or self.fxt.lower()[0] == 't':
			return True
	
	def run_ca(self):
		if self.ca == "":
			return False
		if self.ca.lower()[0] == 'y' or self.ca.lower()[0] == 't':
			return True

	def run_fqf(self):
		if self.fqf == "":
			return False
		if self.fqf.lower()[0] == 'y' or self.fqf.lower()[0] == 't':
			return True

	def run_ps(self):
		if self.ps == "":
			return False
		if self.ps.lower()[0] == 'y' or self.ps.lower()[0] == 't':
			return True

	def get_fileList(self):
		return self.fileList

	def get_fileNames(self):
		return self.fileNames

	def get_f(self):
		return self.f

	def get_q(self):
		return self.q

	def get_o(self):
		return self.o

	def get_e(self):
		return self.e
	
	def get_n(self):
		return self.n
	
	def get_m(self):
		return self.m

	def get_p(self):
		return self.p

	def get_k(self):
		return self.k


class FastxTrimmer(object):
	# Run "fastx_trimmer" on each or the input files.
	def __init__(self, conf):
		conf = conf
	
	def run(self):
		fxtOutFiles = []
		for i in conf.get_fileNames():
			fileName = i.split()[0]
			qual = "-" + i.split()[1].upper()
			outFile = noFileExt(fileName)[0] + conf.fxt_ext + noFileExt(fileName)[1]
			try:
				subprocess.call([	"fastx_trimmer", qual,
							"-f", conf.get_f(), 
							"-i", fileName, 
							"-o", outFile])
				fxtOutFiles.append(outFile)				# Perhaps redundant

			except:
				print "Dude, this is not working!"

class Cutadapt(object):
	# Run "cutadapt" on each of the output files from "fastx_trimmer".
	def __init__(self, conf):
		conf = conf
#		makeCAconf()			# Redundant
	
	def run(self):
		fileNumber = 1
		for i in conf.get_fileNames():
			nameBase = noFileExt(i.split()[0])[0] + conf.fxt_ext
			readInfoFile = "--info-file=%s%s_read_info_%s.txt" % (nameBase, conf.ca_ext, fileNumber)
			inFile = nameBase + noFileExt(i.split()[0])[1]
			outFile1 = nameBase + conf.ca_ext + noFileExt(i.split()[0])[1]
			outFile2 = nameBase + conf.ca_ext + "_run_info_%s" % fileNumber + noFileExt(i.split()[0])[1]
			output = open(outFile2, "w")

			try:
				subprocess.call([	"cutadapt",
							"-a", "AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACATCACGATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACCGATGTATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACTTAGGCATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACTGACCAATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACGCCAATATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACCAGATCATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACACTTGAATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACGATCAGATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACTAGCTTATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACGGCTACATCTCGTATGCCGTCTTCTGCTTG",
							"-a", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACCTTGTAATCTCGTATGCCGTCTTCTGCTTG",
							"-q", conf.get_q(),
							"-O", conf.get_o(),
							"-e", conf.get_e(),
							"-n", conf.get_n(),
							"-m", conf.get_m(),
							readInfoFile,
							"-o", outFile1,
							inFile], stdout=output)
				output.close()
				fileNumber += 1
			except:
				print "Hmm... there is something wrong with cutadapt!"


class FastqQualityFilter(object):
	def __init__(self, conf):
		conf = conf

	def run(self):
		# Run "fastq_quality_filter" on each of the output 
		# files in fastq format from "cutadapt".
		for i in conf.get_fileNames():
			nameBase = noFileExt(i.split()[0])[0] + conf.fxt_ext + conf.ca_ext
			qual = "-" + i.split()[1].upper()
			inFile = nameBase + noFileExt(i.split()[0])[1]
			outFile = nameBase + conf.fqf_ext + noFileExt(i.split()[0])[1]

			try:
				subprocess.call([	"fastq_quality_filter", qual,
							"-q", conf.get_k(),
							"-p", conf.get_p(),
							"-i", inFile,
							"-o", outFile])
			except:
				print "Bummer, this does not work!"

class PairSeq(object):
	def __init__(self, conf):
		conf = conf
	
	def run(self):
		num = 0
		while num+1 <= len(conf.get_fileNames()):
			file1 = conf.get_fileNames()[num].split()[0]
			file2 = conf.get_fileNames()[num+1].split()[0]

			try:
				subprocess.call(["pairSeq.py", file1, file2])
			except:
				print "Wrong again!"

			num = num+2


def noFileExt(fileName):
	if fileName[-6:].lower() == ".fastq":
		name = fileName[:-6]
		ext = fileName[-6:]
		return name, ext

def main(conf):
	if conf.run_fxt() == True:
		fxt = FastxTrimmer(conf)
		fxt.run()
		
	if conf.run_ca() == True:
		ca = Cutadapt(conf)
		ca.run()

	if conf.run_fqf() == True:
		fqf = FastqQualityFilter(conf)
		fqf.run()

	if conf.run_ps() == True:
		ps = PairSeq(conf)
		ps.run()


if __name__ == "__main__":
	conf = Conf()
	main(conf)
