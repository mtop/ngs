#!/usr/bin/env python

import subprocess
import os.path

### Use a flag to indicate the config file to use. Uses 'my.cfg' for now.

class FastqFile(object):
	def __init__(self, fileInfo):
		self.name = fileInfo.split()[0]
		self.illformat = fileInfo.split()[1]
		try:
			if fileInfo.split()[2] == "'" or fileInfo.split()[2] == '"':
				self.delim = ' '
			else:
				self.delim = fileInfo.split()[2]
		except:
			self.delim = ' '
	
	def getName(self):
		return self.name

	def getIllFormat(self):
		return self.illformat
	
	def getDelim(self):
		return self.delim
		

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
		self.cpus = config.get('clc', 'cpus')
		self.output_file = config.get('clc', 'output_file')
		self.min_dist = config.get('clc', 'min_dist')
		self.max_dist = config.get('clc', 'max_dist')

		self.fxt = config.get('run', 'fastx_trimmer')
		self.ca = config.get('run', 'cutadapt')
		self.fqf = config.get('run', 'fastq_quality_filter')
		self.ps = config.get('run', 'pairSeq.py')
		self.clc_novo_assemble = config.get('run', 'clc_novo_assemble')

		self.fxt_ext = ".FXT"
		self.ca_ext = ".CA"
		self.fqf_ext = ".FQF"
		self.ps_ext = ".PS"

		# Create a list of file names.
		self.files = []
		for i in range(1, 21):
			try: 
				# Find the name of the input file.
				self.fileName = config.get('rawfiles', str(i))
				# Create a FastqFile object.
				f = FastqFile(self.fileName)
				# Append the objet to a file object list.
				self.files.append(f)
			except:
				continue

	def getAssemblyFiles(self):
		num = 0
		pairList = []
		singlesList = []
		while num+1 <= len(self.get_files()):
			tmpList = []
			file1 = conf.get_files()[num].getName()
			file2 = conf.get_files()[num+1].getName()
			file1_pair = noFileExt(file1)[0] + self.fxt_ext + self.ca_ext + self.fqf_ext + self.ps_ext + ".Pair" + noFileExt(file1)[1]
			file2_pair = noFileExt(file2)[0] + self.fxt_ext + self.ca_ext + self.fqf_ext + self.ps_ext + ".Pair" + noFileExt(file2)[1]
			file1_singlets = noFileExt(file1)[0] + self.fxt_ext + self.ca_ext + self.fqf_ext + self.ps_ext + ".Singles" + noFileExt(file1)[1]
			file2_singlets = noFileExt(file2)[0] + self.fxt_ext + self.ca_ext + self.fqf_ext + self.ps_ext + ".Singles" + noFileExt(file2)[1]
			tmpList.append(file1_pair)
			tmpList.append(file2_pair)
			pairList.append(tmpList)
			singlesList.extend([file1_singlets, file2_singlets])
			num = num+2
		return pairList, singlesList

	def getPairs(self):
		return self.getAssemblyFiles()[0]

	def getSinglets(self):
		return self.getAssemblyFiles()[1]


		

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

	def run_clc_novo_assemble(self):
		if self.clc == "":
			return False
		if self.clc.lower()[0] == 'y' or self.clc.lower()[0] == 't':
			return True

	def get_files(self):
		return self.files

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

	def get_cpus(self):
		return self.cpus

	def get_output_file(self):
		return self.output_file
	
	def get_min_dist(self):
		return self.min_dist

	def get_max_dist(self):
		return self.max_dist


class FastxTrimmer(object):
	# Run "fastx_trimmer" on each of the input files.
	def __init__(self, conf):
		conf = conf
	
	def run(self):
		fxtOutFiles = []
		for i in conf.get_files():
			fileName = i.getName()
#			fileName = i.split()[0]
#			qual = "-" + i.split()[1].upper()
			illFormat = "-" + i.getIllFormat().upper()
#			print illFormat				# Devel.
			outFile = noFileExt(fileName)[0] + conf.fxt_ext + noFileExt(fileName)[1]
			try:
				subprocess.call([	"fastx_trimmer", illFormat,
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
		for i in conf.get_files():
			nameBase = noFileExt(i.getName())[0] + conf.fxt_ext
			readInfoFile = "--info-file=%s%s_read_info_%s.txt" % (nameBase, conf.ca_ext, fileNumber)
			inFile = nameBase + noFileExt(i.getName())[1]
			outFile1 = nameBase + conf.ca_ext + noFileExt(i.getName())[1]
			outFile2 = nameBase + conf.ca_ext + "_run_info_%s" % fileNumber + noFileExt(i.getName())[1]
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
		for i in conf.get_files():
			nameBase = noFileExt(i.getName())[0] + conf.fxt_ext + conf.ca_ext
			illFormat = "-" + i.getIllFormat().upper()
			inFile = nameBase + noFileExt(i.getName())[1]
			outFile = nameBase + conf.fqf_ext + noFileExt(i.getName())[1]

			try:
				subprocess.call([	"fastq_quality_filter", illFormat,
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
		while num+1 <= len(conf.get_files()):
			file1 = conf.get_files()[num]
			file2 = conf.get_files()[num+1]
			
			# Test if the two files in the pair have the same delimiter registered in the config file.
			if file1.getDelim() == file2.getDelim():
				pass
			else:
				print "%s and %s have different delimeters" % (file1.getDelim(), file2.getDelim())
				break

			try:
				subprocess.call(["pairSeq.py", file1.getName(), file2.getName(), file1.getDelim()])
			except:
				print "Wrong again!"

			num = num+2

class Clc_novo_assemble(object):
	def __init__(self, conf):
		conf = conf

	def run(self):
		args = ["clc_novo_assemble", "--cpus", conf.get_cpus(), 
			"-o", conf.get_output_file(), 
			"-p", "fb", "ss", conf.get_min_dist(), conf.get_max_dist()]

		args.extend(["-q", "-i"])
		for pair in conf.getPairs():
			# TODO: Test if files exists and are non-empty.
			args.extend([pair[0], pair[1]])

		args.extend(["-p", "no", "-q"])
		for i in conf.getSinglets():
			# TODO: Test if file exists and is non-empty.
			args.append(i)

		try:
			subprocess.call(args)
		except:
			print "No, no, no!"


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

	if conf.run_clc_novo_assemble() == True:
		clc = Clc(conf)
		clc.run()


if __name__ == "__main__":
	conf = Conf()
	main(conf)
