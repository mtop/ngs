#!/usr/local/packages/anaconda2/bin/python

# Usage: pytest -v tests/test_parseCDHITresult.py

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import pytest
import parseCDHITresult
import subprocess


class TestCluster:
	
	def setup_args(self):
		# Test of ...
		return parseCDHITresult.parse_args(['-c', '2', '-d', '_TRINITY_', '-r', '2', 'tests/small_cluster-file.clstr'])

	def populate_the_class(self):
#		n = 0
		self.TestClusterClass = []
		self.args = self.setup_args()
		with open(self.args.cdhitfile) as infile:
			for cluster, stuff in parseCDHITresult.readCDHITtable(infile):
				self.TestClusterClass.append(parseCDHITresult.Cluster(cluster, stuff, self.args))
		return self.TestClusterClass

	def test_name(self):
		n = 0
		for cluster in self.populate_the_class():
			assert cluster.get_name() == ">Cluster %s\n" % n
			n += 1

#	def test_result(self):
#		# Everything that is contained in the output 
#		# from this method is outputed by the other methods
#		pass

	def test_results_numbers(self):
		n = 0
		for cluster in self.populate_the_class():
			assert cluster.get_results_numbers()[n] == "%s" % n
			n += 1

	def test_results_length(self):
		n = 0
		length = [[1572], [14126, 14200], [249, 8833, 1201], [14979, 1418, 275, 374], [4887, 9334, 724, 14929, 859], [577, 394, 363, 999, 715, 471], [1810, 2310, 1656, 1905, 14519, 1372, 1390], [2512, 2034, 1039, 402, 394, 290, 310, 3932], [616, 1372, 457, 280, 361, 289, 202, 1364, 5361], [12982, 4242, 14316, 11991, 1072, 12678, 8380, 14332, 11940, 14323]]
		for cluster in self.populate_the_class():
			for x in range(len(cluster.get_results_length())):
				assert int(cluster.get_results_length()[x]) == length[n][x]
			n += 1

	def test_results_seq_names(self):
		n = 0
		names = [["P3503_104_TRINITY_DN23094_c0_g1_i1"], ["P3503_104_TRINITY_DN23026_c14_g1_i1", "P3503_107_TRINITY_DN21914_c2_g3_i2"], ["P3503_104_TRINITY_DN3855_c0_g1_i1", "P3503_104_TRINITY_DN23047_c7_g2_i1", "P3503_104_TRINITY_DN23047_c9_g1_i1"], ["P3503_107_TRINITY_DN22044_c4_g4_i2", "P3503_110_TRINITY_DN37029_c0_g1_i1", "P3503_112_TRINITY_DN39144_c0_g1_i1", "P3503_112_TRINITY_DN19415_c2_g1_i1"], ["P3503_104_TRINITY_DN22906_c0_g2_i1", "P3503_104_TRINITY_DN22906_c1_g1_i1", "P3503_104_TRINITY_DN22906_c2_g1_i1", "P3503_107_TRINITY_DN21601_c0_g1_i1", "P3503_110_TRINITY_DN22683_c0_g1_i1"], ["P3503_104_TRINITY_DN18991_c1_g1_i1", "P3503_104_TRINITY_DN18991_c2_g1_i1", "P3503_104_TRINITY_DN18991_c3_g1_i1", "P3503_104_TRINITY_DN35788_c0_g1_i1", "P3503_104_TRINITY_DN10774_c0_g1_i1", "P3503_104_TRINITY_DN10774_c1_g1_i1"], ["P3503_112_TRINITY_DN22925_c4_g1_i1", "P3503_116_TRINITY_DN22730_c0_g1_i2", "P3503_122_TRINITY_DN24331_c1_g1_i1", "P3503_124_TRINITY_DN24205_c0_g2_i1", "P3503_128_TRINITY_DN21867_c0_g1_i4", "P3503_128_TRINITY_DN21867_c0_g2_i1", "P3503_129_TRINITY_DN21847_c0_g2_i1"], ["P3503_104_TRINITY_DN22955_c2_g3_i1", "P3503_104_TRINITY_DN19776_c0_g1_i1", "P3503_104_TRINITY_DN19776_c1_g1_i1", "P3503_104_TRINITY_DN18756_c0_g1_i1", "P3503_104_TRINITY_DN18756_c1_g1_i1", "P3503_104_TRINITY_DN9726_c0_g1_i1", "P3503_104_TRINITY_DN9726_c1_g1_i1", "P3503_104_TRINITY_DN21663_c0_g1_i1"], ["P3503_104_TRINITY_DN23344_c0_g1_i1", "P3503_104_TRINITY_DN17918_c0_g1_i1", "P3503_104_TRINITY_DN36912_c0_g1_i1", "P3503_104_TRINITY_DN312_c0_g1_i1", "P3503_104_TRINITY_DN11376_c0_g1_i1", "P3503_104_TRINITY_DN11376_c1_g1_i1", "P3503_104_TRINITY_DN38427_c0_g1_i1", "P3503_110_TRINITY_DN22872_c3_g3_i1", "P3503_112_TRINITY_DN22264_c0_g1_i1"], ["P3503_107_TRINITY_DN21878_c1_g1_i1", "P3503_107_TRINITY_DN21878_c1_g1_i2", "P3503_110_TRINITY_DN22846_c1_g4_i1", "P3503_116_TRINITY_DN22730_c0_g3_i1", "P3503_122_TRINITY_DN24331_c0_g2_i1", "P3503_122_TRINITY_DN24331_c0_g3_i1", "P3503_124_TRINITY_DN28360_c1_g1_i3", "P3503_126_TRINITY_DN22736_c1_g1_i1", "P3503_127_TRINITY_DN25385_c1_g2_i2", "P3503_128_TRINITY_DN21867_c0_g1_i3"]]
		for cluster in self.populate_the_class():
			print cluster.get_results_seq_names()
			for x in range(len(cluster.get_results_length())):
				assert cluster.get_results_seq_names()[x] == names[n][x]
			n += 1

	def test_strains(self):
		n = 0
		strains = [["REF"], ["+", "REF"], ["+", "REF", "+"], ["REF", "+", "+", "+"], ["+", "+", "+", "REF", "+"], ['+', '+', '+', 'REF', '+', '+'], ['+', '+', '+', '+', 'REF', '+', '+'], ['+', '+', '+', '+', '+', '+', '+', 'REF'], ['+', '+', '+', '+', '+', '+', '+', '+', 'REF'], ['+', '+', '+', '+', '+', '+', '+', 'REF', '+', '+']]
		for cluster in self.populate_the_class():
			assert cluster.get_strains() == strains[n]
			n += 1

	def test_identities(self):
		n = 0
		identities = [['REF'], [99.99, 'REF'], [100.0, 'REF', 100.0], ['REF', 99.93, 98.91, 100.0], [99.82, 99.89, 98.9, 'REF', 99.53], [100.0, 100.0, 100.0, 'REF', 100.0, 100.0], [100.0, 100.0, 99.94, 100.0, 'REF', 99.71, 99.71], [100.0, 99.95, 100.0, 100.0, 100.0, 100.0, 100.0, 'REF'], [99.84, 99.93, 100.0, 100.0, 100.0, 99.65, 99.5, 99.78, 'REF'], [99.94, 99.15, 99.95, 99.98, 98.32, 99.97, 99.95, 'REF', 99.98, 99.94]]
		for cluster in self.populate_the_class():
			print cluster.get_identities()
			assert cluster.get_identities() == identities[n]
			n += 1

	def test_cluster_size(self):
		n = 0
		size = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		for cluster in self.populate_the_class():
			assert cluster.get_cluster_size() == size[n]
			n += 1

	def test_cluster_center(self):
		n = 0
		center = ["P3503_104_TRINITY_DN23094_c0_g1_i1", "P3503_107_TRINITY_DN21914_c2_g3_i2", "P3503_104_TRINITY_DN23047_c7_g2_i1", "P3503_107_TRINITY_DN22044_c4_g4_i2", "P3503_107_TRINITY_DN21601_c0_g1_i1", "P3503_104_TRINITY_DN35788_c0_g1_i1", "P3503_128_TRINITY_DN21867_c0_g1_i4", "P3503_104_TRINITY_DN21663_c0_g1_i1", "P3503_112_TRINITY_DN22264_c0_g1_i1", "P3503_126_TRINITY_DN22736_c1_g1_i1"]
		for cluster in self.populate_the_class():
			assert cluster.get_center() == center[n]
			n += 1

	def test_number_of_samples(self):
		n = 0
		number_of_samples = [1, 2, 1, 3, 3, 1, 6, 1, 3, 8]
		for cluster in self.populate_the_class():
			assert cluster.get_number_of_samples() == number_of_samples[n]
			n += 1

