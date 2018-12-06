# -*- coding: utf-8 -*-
"""TG17, 83405 Joao Neves, 84711 Diogo Redin"""
import numpy as np

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
		Also used for the pointwise product, to obtain values for true and false for a variable.
		Complexity: O(n)
		'''
		# If there's nothing to cut, return self
		if unit not in self.units:
			return self
		new_prob = []

		res = Factor(self.prob, self.units.copy())

		# Updating positions in dictionary, removing variable to cut
		unit_pos = res.units[unit]
		for var in res.units:
			if res.units[var] > unit_pos:
				res.units[var] -= 1
		del res.units[unit]
		
		# Offset is used to choose between true and false values
		# Since false values are first, offset = 0 for false
		offset = 0

		# Limit is the number of sequential values to cut,
		# which is the number of sequential values for which unit = true OR unit = false
		limit = 1 << unit_pos

		# If value = true, offset will be instead the first value for which unit = true,
		# so it skips all sequential values for unit = false
		if value == 1:
			offset += limit

		# To cut out the desired variable, get all elements 
		# in start + limit, which are sequential values for unit = true OR unit = false.
		# Step is 2 * limit, so start is at the next sequence of unit = true OR unit = false.
		for start in range(offset, len(res.prob), limit << 1):
			new_prob += res.prob[start:start + limit]
		
		res.prob = new_prob

		# A new factor is returned for this operation
		# self may be necessary for operations later, so remains unchanged
		return res

	def mul(self, factor):
		''' 
		Multiplies a factor by another, storing the result in self.
		Complexity: O(n log n)
		'''

		common_units = 0
		new_units = {}

		# Complexity: O(n log n)
		# Adding up both unit dictionaries, updating positions
		for element in self.units:
			if element in factor.units:
				common_units += 1

			if element not in new_units:
				updateDict(new_units, element)
		for element in factor.units:
			if element not in new_units:
				updateDict(new_units, element)

		# Getting new size for the factor prob
		new_size = 1 << (len(self.units) + len(factor.units) - common_units)
		new_prob = []

		# Complexity: O(n)
		for i in range(new_size):
			new_prob.append(self.getProb(i, new_units) * factor.getProb(i, new_units))
		
		# Returns a new, separate factor,
		# since the original factors are necessary for later
		return Factor(new_prob, new_units)

	def normalize(self):
		'''
		Normalizes a factor.
		Complexity = O(1)
		'''
		add = float(self.prob[0] + self.prob[1])
		self.prob[0] /= add
		self.prob[1] /= add

	def getProb(self, evid, new_units):
		'''
		Returns a factor's specific prob for evid, new units coordinates
		Used for factor multiplication, to get corresponding values in both factors
		O(k), k is the number of the factor's units
		'''
		index = 0
		for unit in self.units:
			index += int(evid & 1 << new_units[unit] != 0) << self.units[unit]
		return self.prob[index]


def getFactorFromNode(node, node_index):
	'''
	Create a factor given a node.
	Complexity: which is O(2**k), k is the units.
	Size Complexity for each factor is O(2**k).
	'''
	# New prob list adds a dimension: node_index
	# which necessitates the value for node_index = false AND = true.(1-prob, prob)
	new_prob = []
	for prob in node.prob:
		new_prob.append(1 - prob)
		new_prob.append(prob)
	
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
		if type(prob) == np.ndarray:
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

		#
		# *** STEP 1 - CUT EVIDENCE VARIABLES *** #
		#

		# Run through evidence array,
		# cutting evidence variables for the specific value
		for ev in range(len(evid)):
			val = evid[ev]
			if val == 0 or val == 1:
				for i in range(len(factors)):
					factors[i] = factors[i].cut(ev, val)

		#
		# *** STEP 2 - SUM OUT *** #
		#

		factor_val = (0, 1)
		to_sum = []
		factor_sums = [0, 0]

		# Loop while there are still unknown variables
		while len(unknown) > 0:

			# Get variable to be summed out
			# will be the last value in to_sum
			# (deepest unknown node in the BN, in this case)
			sum_var = unknown[-1]

			# Factor sums will save the multiplication results
			# for all the factors to be summed out (true and false)
			factor_sums[0] = getNewFactor()
			factor_sums[1] = getNewFactor()
			
			# Finding factors to be summed out
			for f in factors:
				if sum_var in f.units:
					to_sum.append(f)

			# Pointwise product, for variable = true
			# and variable = false, (0, 1)
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
			
			# Removing unknown from list
			del unknown[-1]
			to_sum.clear()
		
		#
		# *** STEP 3 - POINT-WISE PRODUCT ON REMAINING FACTORS *** #
		#

		f_res = getNewFactor()
		
		for f in factors:
			f_res = f_res.mul(f)

		f_res.normalize()

		# Returns the value for query = true
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