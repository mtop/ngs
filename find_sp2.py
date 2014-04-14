#!/usr/bin/env python

gff_file = open("Athaliana_167_gene.gff3", "r")
variation_files = ["LIB5669.clc_find_variation.out", "LIB5670.clc_find_variation.out", "LIB5671.clc_find_variation.out"]
gene_object_list = []
mutaion_object_list = []

class Gff(object):
	def __init__(self, chromosome, start, stop, name):
		self.chromosome = chromosome
		self.start = start
		self.stop = stop
		self.name = name
		
	def get_chromosome(self):
		return self.chromosome

	def get_name(self):
		return self.name

	def first_base(self):
		return self.start

	def last_base(self):
		return self.stop

	def inside(self, pos, chromosome):
		if self.get_chromosome() == chromosome and int(self.start) <= int(pos) and int(pos) <= int(self.stop):
			return True

class Mutation(object):
	def __init__(self, possition, mutation, org_base, mut_base, chromosome):
		self.possition = possition
		self.mutation = mutation
		self.org_base = org_base
		self.mut_base = mut_base
		self.chromosome = chromosome

	def in_gene(self):
		# Test if the mutation occures in a gene
		print gene_object_list
		for gene in gene_object_list:
			if gene.inside(self.possition, self.chromosome):
				return gene.get_name()
			else:
				return None

	def original_base(self):
		return self.org_base
	
	def mutated_base(self):
		return self.mut_base

	def get_position(self):
			return self.possition

	def get_chromosome(self):
		return self.chromosome

def main():
	# Parse the gff file and fish out the "genes"
	# Store them in separate instances of the Gff object, 
	# and collect all instances in a list.
	if gff_file.readline() == "#":
		pass
	for line in gff_file.readlines():
		if line.split()[2] == "gene":
			# Instantiate a Gff object
			gene_name = line.split()[8].split("Name=")[1]
			# 0: Chromosome, 3: Start pos. 4: Stop pos.
			gff_object = Gff(line.split()[0], line.split()[3], line.split()[4], gene_name)
			gene_object_list.append(gff_object)
			
			

	for var_file in variation_files:
		# Print the name of hte variation file
		print var_file
		# Open the variation file.
		var = open(var_file, "r")
		# Create a dictionary for each variation file to store the mutation objects in.
		var_file = {}
		for line in var.readlines():
			# Store info about on which chromosome positions refere to.
			try:
				if line.split()[1] == "CHROMOSOME":
					chromosome = line.split()[0]
			except IndexError:
				pass

			# Ignore empty lines.
			if line.strip():
				if line.split()[0][0:3] == "Chr":
					pass
				else:
					# Parse the recorded differences between the mutant 
					# dataset and the reference sequence.
					# 					possition, 		 mutation, 		  original_base,   mutated_base
					mutation_obj = Mutation(line.split()[0], line.split()[1], line.split()[2], line.split()[4], chromosome)
					# Do the actuall testing of the mutaion
					if mutation_obj.original_base() == "G" and mutation_obj.mutated_base() == "A" \
					or mutation_obj.original_base() == "C" and mutation_obj.mutated_base() == "T":


						for gene in gene_object_list:
							if gene.inside(mutation_obj.get_position(), mutation_obj.get_chromosome()):
								try:
									var_file[gene.get_name()] = mutation_obj
								except KeyError:
									pass
		# Print all keys and positions for the mutations to STDOUT.							
		for key in var_file:
			print key, var_file[key].get_position()

if __name__ == "__main__":
	main()	
