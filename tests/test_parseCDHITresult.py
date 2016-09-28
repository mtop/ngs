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
		pass

	def test_strains(self):
		pass

	def test_identities(self):
		pass

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
		pass

