# -*- coding: utf-8 -*-
""" TG17, 84711 Diogo Redin, 83405 Joao Neves """
import numpy

def flatten(l):

	'''
	Flattens a list with an arbitrary number of inner lists, creating a single, one dimensional list.
	O(n * m) -> n is the list size, m is the max list depth
	'''
	i = 0
	while i < len(l):
		while isinstance(l[i], list):
			if l[i] == []:
				del l[i]
				i -= 1
				break
			else:
				l[i:i + 1] = l[i]
		i += 1
	return l

class Factor():
	def __init__(self, prob, units):
		''' 
		Used for the variable elimination algorithm.
		prob is the probability, ordered according to the units (variables)
		Initialization is O(1).
		'''
		self.prob = prob
		self.units = units
		
	def sumFactor(self, factor):
		''' 
		Used for the variable elimination algorithm.
		Complexity: O(n)
		'''
		for i in range(len(self.prob)):
			self.prob[i] += factor.prob[i]

	def cut(self, unit, value):
		''' 
		Used for the variable elimination algorithm.
		if value = 0 || 1 -> Removes the unused value from a set evidence variable.
		Complexity: O(n)
		'''
		if unit not in self.units:
			return self
		new_prob = []

		res = Factor(self.prob, self.units.copy())
		# Updating positions
		unit_pos = res.units[unit]

		for element in res.units:
			if res.units[element] > unit_pos:
				res.units[element] -= 1
		

		max_hops = res.getMultiplier(unit_pos)
		hop_distance = max_hops
		i = 0

		while i < len(res.prob):
			for remaining_hops in range(max_hops):
				# Obtain P(unit = true)
				if value == 1:
					new_prob.append(res.prob[i + hop_distance])
				# Obtain P(unit = false)
				elif value == 0:
					new_prob.append(res.prob[i])
				i += 1
			i += hop_distance
		del res.units[unit]
		res.prob = new_prob
		return res

	def mul(self, factor):
		''' 
		Multiplies a factor by another, storing the result in self.
		Complexity: O(n log n)
		'''

		common_units = 0
		new_units = {}

		# Complexity: O(n log n)
		for element in self.units:
			if element in factor.units:
				common_units += 1

			if element not in new_units:
				updateDict(new_units, element)

		for element in factor.units:
			if element not in new_units:
				updateDict(new_units, element)

		new_prob = [1] * (1 << (len(self.units) + len(factor.units) - common_units))

		# Complexity: O(n)
		for i in range(len(new_prob)):
			new_prob[i] = self.getProb(i, new_units) * factor.getProb(i, new_units)

		return Factor(new_prob, new_units)


	def getMultiplier(self, unit_pos):
		'''
		Gets the index multiplier for the specific position
		Complexity = O(1)
		'''
		return 1 << unit_pos

	def normalize(self):
		'''
		Normalizes a factor.
		Complexity = O(1)
		'''
		add = float(self.prob[0] + self.prob[1])
		self.prob[0] /= add
		self.prob[1] /= add

	def getProb(self, evid, new_units):
		index = 0
		for unit in self.units:
			index += int(evid & 1 << new_units[unit] != 0) << self.units[unit]
		return self.prob[index]


def getFactorFromNode(node, node_index):
	'''
	Create a factor given a node.
	Complexity: O(n), n is the prob size, which is O(2**k), k is the units.
	Size Complexity for each factor is O(2**k).
	'''
	# Creating new prob list for factor
	new_prob = [0] * (1 << (len(node.parents) + 1))
	for i in range(0, len(new_prob), 2):
		new_prob[i] = 1 - node.prob[i >> 1]
		new_prob[i + 1] = node.prob[i >> 1]
	
	unit_list = {}
	unit_pos = len(node.parents)

	# Creating new unit list + position for factor
	for parent in node.parents:
		unit_list[parent] = unit_pos
		unit_pos -= 1
	unit_list[node_index] = unit_pos

	return Factor(new_prob, unit_list)


def updateDict(d, val):
	''' 
	Updates the dictionary for the next positions
	Complexity O(n), n is the dictionary size.
	'''
	pos = len(d)
	for i in d:
		if i > val:
			if pos > d[i]:
				pos = d[i]
			d[i] += 1
	d[val] = pos

def getNewFactor():
	return Factor([1.0],{})

class Node():
	def __init__(self, prob, parents = []):
		if type(prob) == numpy.ndarray:
			prob = prob.tolist()

		self.prob = flatten(prob)
		self.parents = parents

	def computeProb(self, evid):
		'''
		Complexity is O(m), m is the number of parents the node has.
		'''
		# If there are no parents, the probability is trivial
		if self.parents == []:
			p = self.prob[0]

		# If there are parents, evaluate each parent	
		else:
			index = 0
			dad_count = len(self.parents) - 1
			for dad in self.parents:
				index += (1 & evid[dad]) << dad_count
				dad_count -= 1
			p = self.prob[index]
		
		return [1 - p, p]

class BN():
	def __init__(self, gra, nodes):
		self.gra = gra
		self.nodes = nodes

	def computePostProb(self, evid):
		'''
		Time Complexity: O(2**k), number of operations for each parent k
		Space Complexity: O(2**k), k is the number of parents (max factor size)
		'''

		# Getting unknown variables
		unknown = []
		
		for i in range(len(evid)):
			if evid[i] == []:
				unknown.append(i)		

		# Creating factors
		# O(n)
		factors = []
		for i in range(len(self.nodes)):
			factors.append(getFactorFromNode(self.nodes[i], i))

		# *** STEP 1 - CUT EVIDENCE VARIABLES *** #
		for i in range(len(evid)):
			val = evid[i]
			if val == 0 or val == 1:
				for findex in range(len(factors)):
					factors[findex] = factors[findex].cut(i, val)

		# *** STEP 2 - SUM OUT *** #
		factor_val = (0, 1)
		to_sum = []
		factor_sums = []

		while len(unknown):
			sum_var = unknown[-1]
			factor_sums[:] = [getNewFactor(), getNewFactor()]

			# Finding factors to be summed out
			for f in factors:
				if sum_var in f.units:
					to_sum.append(f)

			# Pointwise product, for variable = true and variable = false
			for val in factor_val:
				for f in to_sum:
					factor_sums[val] = factor_sums[val].mul(f.cut(sum_var, val))

			# Sum the two results
			if len(factor_sums[0].units) != 0:
				factor_sums[0].sumFactor(factor_sums[1])
				factors.append(factor_sums[0])

			# Removing factors that were summed out
			for f in to_sum:
				factors.remove(f)
			
			unknown = unknown[:-1]
			to_sum.clear()
		
		f_res = getNewFactor()
		
		for f in factors:
			f_res = f_res.mul(f)
		f_res.normalize()
		return f_res.prob[1]
	
	def computeJointProb(self, evid):
		'''
		Complexity: O(n * m)
		n is the number of nodes. m is the number of the node's parents.
		'''

		res = 1
		for i in range(len(self.nodes)):
			res *= self.nodes[i].computeProb(evid)[evid[i]]
		return res