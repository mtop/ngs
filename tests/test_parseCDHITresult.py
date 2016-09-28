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

	def test_cluster_name(self):
		n = 0
		for cluster in self.populate_the_class():
			
			assert cluster.get_name() == ">Cluster %s\n" % n
			n += 1

	def test_cluster_center(self):
		n = 0
		center = ["P3503_104_TRINITY_DN23094_c0_g1_i1", "P3503_107_TRINITY_DN21914_c2_g3_i2", "P3503_104_TRINITY_DN23047_c7_g2_i1", "P3503_107_TRINITY_DN22044_c4_g4_i2", "P3503_107_TRINITY_DN21601_c0_g1_i1", "P3503_104_TRINITY_DN35788_c0_g1_i1", "P3503_128_TRINITY_DN21867_c0_g1_i4", "P3503_104_TRINITY_DN21663_c0_g1_i1", "P3503_112_TRINITY_DN22264_c0_g1_i1", "P3503_126_TRINITY_DN22736_c1_g1_i1"]
		for cluster in self.populate_the_class():
			assert cluster.get_center() == center[n]
			n += 1

	def test_cluster_size(self):
		n = 0

