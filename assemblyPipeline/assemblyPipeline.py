#!/usr/bin/env python

import subprocess
import os.path
import time

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
		self.output_prefix = config.get('output', 'prefix')
		self.min_dist = config.get('clc', 'min_dist')
		self.max_dist = config.get('clc', 'max_dist')

		self.fxt = config.get('run', 'fastx_trimmer')
		self.ca = config.get('run', 'cutadapt')
		self.fqf = config.get('run', 'fastq_quality_filter')
		self.ps = config.get('run', 'pairSeq.py')
		self.clc_novo_assemble = config.get('run', 'clc_novo_assemble')
		self.clc_ref_assemble = config.get('run', 'clc_ref_assemble')
		self.clc_info_assemble = config.get('run', 'clc_info_assemble')

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
			file1_pair = noFileExt(file1)[0] + ".Pair" + noFileExt(file1)[1]
			file2_pair = noFileExt(file2)[0] + ".Pair" + noFileExt(file2)[1]
			file1_singlets = noFileExt(file1)[0] + ".Singles" + noFileExt(file1)[1]
			file2_singlets = noFileExt(file2)[0] + ".Singles" + noFileExt(file2)[1]
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
		if self.clc_novo_assemble == "":
			return False
		if self.clc_novo_assemble.lower()[0] == 'y' or self.clc_novo_assemble.lower()[0] == 't':
			return True

	def run_clc_ref_assemble(self):
		if self.clc_ref_assemble == "":
			return False
		if self.clc_ref_assemble.lower()[0] == 'y' or self.clc_ref_assemble.lower()[0] == 't':
			return True

	def run_clc_info_assemble(self):
		if self.clc_info_assemble == "":
			return False
		if self.clc_info_assemble.lower()[0] == 'y' or self.clc_info_assemble.lower()[0] == 't':
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

	def get_output_novo(self):
		return self.output_prefix + "_novo.out"

	def get_output_ref(self):
		return self.output_prefix + "_ref.out"

	def get_output_info(self):
		return self.output_prefix + "_info.out"
	
	def get_output_prefix(self):
		return self.output_prefix
	
	def get_min_dist(self):
		return self.min_dist

	def get_max_dist(self):
		return self.max_dist

class Log(object):
	def __init__(self, conf):
		conf = conf
		out = open(conf.output_prefix + ".log", "a")	# Is this step necessary?

	def write(self, text):
		out = open(conf.output_prefix + ".log", "a")
		out.write(text + '\n')
		out.close()

	def time(self):
		self.write(time.ctime())


class FastxTrimmer(object):
	# Run "fastx_trimmer" on each of the input files.
	def __init__(self, conf):
		conf = conf
	
	def run(self):
		log.write('\n'"	fastx_trimmer"'\n')
		fxtOutFiles = []
		for i in conf.get_files():
			fileName = i.getName()
#			fileName = i.split()[0]
#			qual = "-" + i.split()[1].upper()
			illFormat = "-" + i.getIllFormat().upper()
#			print illFormat				# Devel.
			outFile = noFileExt(fileName)[0] + conf.fxt_ext + noFileExt(fileName)[1]

			log.time()
			log.write("[--] " + "Running fastx_trimmer: %s" % i.getName())

			try:
				subprocess.call([	"fastx_trimmer", illFormat,
							"-f", conf.get_f(), 
							"-i", fileName, 
							"-o", os.getcwdu() + "/" + outFile])
				fxtOutFiles.append(outFile)				# Perhaps redundant

			except:
				print "Dude, this is not working!"

class Cutadapt(object):
	# Run "cutadapt" on each of the output files from "fastx_trimmer".
	def __init__(self, conf):
		conf = conf
#		makeCAconf()			# Redundant
	
	def run(self):
		log.write('\n'"	cutadapt"'\n')
		fileNumber = 1
		for i in conf.get_files():
			nameBase = noFileExt(i.getName())[0] + conf.fxt_ext
			readInfoFile = "--info-file=%s%s_read_info_%s.txt" % (nameBase, conf.ca_ext, fileNumber)
			inFile = nameBase + noFileExt(i.getName())[1]
			outFile1 = os.getcwdu() + "/" + nameBase + conf.ca_ext + noFileExt(i.getName())[1]
			outFile2 = nameBase + conf.ca_ext + "_run_info_%s" % fileNumber + noFileExt(i.getName())[1]
			outFile3 = nameBase + conf.ca_ext + "_summary_%s" % fileNumber + noFileExt(i.getName())[1]
			output = open(outFile2, "w")
			output_sum = open(outFile3, "w") 

			log.time()
			log.write("[--] " + "Running cutadapt: %s" % i.getName())

			try:
				# Note: the -b flag indicates a seach in both 5' and 3' ends.
				analysis = subprocess.Popen([	"cutadapt",
							"-b", "AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACATCACGATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACCGATGTATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACTTAGGCATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACTGACCAATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACGCCAATATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACCAGATCATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACACTTGAATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACGATCAGATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACTAGCTTATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACGGCTACATCTCGTATGCCGTCTTCTGCTTG",
							"-b", "GATCGGAAGAGCACACGTCTGAACTCCAGTCACCTTGTAATCTCGTATGCCGTCTTCTGCTTG",
							"-q", conf.get_q(),
							"-O", conf.get_o(),
							"-e", conf.get_e(),
							"-n", conf.get_n(),
							"-m", conf.get_m(),
							readInfoFile,
							"-o", outFile1,
							inFile], stdout=subprocess.PIPE)
				output.close()
				output_sum.write(analysis.communicate()[0])
				output_sum.close()
				
				fileNumber += 1
			except:
				print "Hmm... there is something wrong with cutadapt!"


class FastqQualityFilter(object):
	def __init__(self, conf):
		conf = conf

	def run(self):
		# Run "fastq_quality_filter" on each of the output 
		# files in fastq format from "cutadapt".
		log.write('\n'"	fastq_quality_filter"'\n')
		for i in conf.get_files():
			nameBase = noFileExt(i.getName())[0] + conf.fxt_ext + conf.ca_ext
			illFormat = "-" + i.getIllFormat().upper()
			inFile = nameBase + noFileExt(i.getName())[1]
			outFile = nameBase + conf.fqf_ext + noFileExt(i.getName())[1]

			log.time()
			log.write("[--] " + "Running fastq_quality_filter: %s" % i.getName())

			try:
				subprocess.call([	"fastq_quality_filter", illFormat,
							"-q", conf.get_k(),
							"-p", conf.get_p(),
							"-i", inFile,
							"-o", os.getcwdu() + "/" + outFile])
			except:
				print "Bummer, this does not work!"

class PairSeq(object):
	def __init__(self, conf):
		conf = conf
	
	def run(self):
		log.write('\n'"	pairSeq.py"'\n')
		num = 0
		while num+1 <= len(conf.get_files()):
			file1 = conf.get_files()[num]
			file2 = conf.get_files()[num+1]

			inFile1 = noFileExt(file1.getName())[0] + conf.fxt_ext + conf.ca_ext + conf.fqf_ext + noFileExt(file1.getName())[1]
			inFile2 = noFileExt(file2.getName())[0] + conf.fxt_ext + conf.ca_ext + conf.fqf_ext + noFileExt(file2.getName())[1]

			log.time()
			log.write("[--] " + "Running pairSeq.py: %s & %s" % (file1.getName(), file2.getName()))
			
			# Test if the two files in the pair have the same delimiter registered in the config file.
			if file1.getDelim() == file2.getDelim():
				pass
			else:
				log.write("[ww] %s and %s have different delimeters" % (file1.getDelim(), file2.getDelim())) # Bug.
				break
			
			try:
				subprocess.call(["pairSeq.py", inFile1, inFile2, file1.getDelim()])
			except:
				print "Wrong again!"

			num = num+2

class Clc_novo_assemble(object):
	def __init__(self, conf):
		conf = conf

	def run(self):

		log.write('\n'"	clc"'\n')
#		log.time()
#		log.write("[--] " + "Running clc_novo_assemble")

		args = ["clc_novo_assemble", "--cpus", str(conf.get_cpus()), 
			"-o", os.getcwdu() + "/" + str(conf.get_output_novo()), 
			"-p", "fb", "ss", str(conf.get_min_dist()), str(conf.get_max_dist())]

		args.extend(["-q", "-i"])
		for pair in conf.getPairs():
			
			inFile_1 = noFileExt(pair[0])[0][:-5] + conf.fxt_ext + conf.ca_ext + conf.fqf_ext + ".Pair" + noFileExt(pair[0])[1]
			inFile_2 = noFileExt(pair[1])[0][:-5] + conf.fxt_ext + conf.ca_ext + conf.fqf_ext + ".Pair" + noFileExt(pair[1])[1]	


			# TODO: Test if files exists and are non-empty.
			args.extend([inFile_1, inFile_2])

		args.extend(["-p", "no", "-q"])
		for i in conf.getSinglets():
			singlesFile = noFileExt(i)[0][:-8] + conf.fxt_ext + conf.ca_ext + conf.fqf_ext + ".Singles" + noFileExt(i)[1]
			# TODO: Test if file exists and is non-empty.
			args.append(singlesFile)
		try:
			print "[--] Running clc_novo_assemble: %s" % args
			log.time()
			log.write("[--] Running clc_novo_assemble: %s" % args)
			subprocess.call(args)
		except:
			print "No, no, no!"

class Clc_ref_assemble(object):
	def __init__(self, conf):
		conf = conf
	
	def run(self):

		args = ["clc_ref_assemble", "--cpus", str(conf.get_cpus()), 
			"-o", os.getcwdu() + "/" + str(conf.get_output_ref()), 
			"-p", "fb", "ss", str(conf.get_min_dist()), str(conf.get_max_dist())]

		args.extend(["-q", "-i"])
		for pair in conf.getPairs():
			
			inFile_1 = noFileExt(pair[0])[0][:-5] + conf.fxt_ext + conf.ca_ext + conf.fqf_ext + ".Pair" + noFileExt(pair[0])[1]
			inFile_2 = noFileExt(pair[1])[0][:-5] + conf.fxt_ext + conf.ca_ext + conf.fqf_ext + ".Pair" + noFileExt(pair[1])[1]
			
			# TODO: Test if files exists and are non-empty.
#			args.extend([str(pair[0]), str(pair[1])])
			args.extend([inFile_1, inFile_2])

		args.extend(["-p", "no", "-q"])
		for i in conf.getSinglets():
			# TODO: Test if file exists and is non-empty.
			singlesFile = noFileExt(i)[0][:-8] + conf.fxt_ext + conf.ca_ext + conf.fqf_ext + ".Singles" + noFileExt(i)[1]
#			args.append(str(i))
			args.append(singlesFile)
		args.extend(["-d", str(conf.get_output_novo())])
		try:
			print "[--] Running clc_ref_assemble: %s" % args
			log.time()
			log.write("[--] Running clc_ref_assemble: %s" % args)
			subprocess.call(args)
		except:
			print "No, no, no!"


class Clc_info_assemble(object):
	def __init__(self, conf):
		conf = conf

	def run(self):

		args = ["assembly_info", "-c", "-n", conf.get_output_ref()]

		try:
			print "[--] Running assembly_info: %s" % args
			log.time()
			log.write("[--] Running assembly_info: %s" % args)

			call = subprocess.Popen(args, stdout=subprocess.PIPE)
			data = call.communicate()[0]

			out = open(os.getcwdu() + "/" + conf.get_output_info(), "w")
			out.write(data)
			out.close()

		except:
			print "Assembly_info is fubar"
		

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
		clcNovo = Clc_novo_assemble(conf)
		clcNovo.run()

	if conf.run_clc_ref_assemble() == True:
		clcRef = Clc_ref_assemble(conf)
		clcRef.run()

	if conf.run_clc_info_assemble() == True:
		clcInfo = Clc_info_assemble(conf)
		clcInfo.run()

	log.write("[--] Analysis finished %s" % time.ctime())	


if __name__ == "__main__":
	conf = Conf()
	log = Log(conf)
	main(conf)
#	print os.getcwdu() + "/"
#	print time.ctime()
