# -*- coding: utf-8 -*-

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

	def show(self):
		print("Factor:")
		print("Factor Prob:")
		print(self.prob)
		print("Factor Units:")
		print(self.units)

	def sumOut(self, unit):
		''' 
		Used for the variable elimination algorithm.
		Complexity: O(n)
		'''
		self.cutOut(unit, -1)

	def cutOut(self, unit, value):
		''' 
		Used for the variable elimination algorithm.
		if value = 0 || 1 -> Removes the unused value from a set evidence variable.
		if value = -1 sums out the *unit* variable. unit is the variable index in the node.
		Complexity: O(n)
		'''
		new_prob = []

		# Updating positions
		unit_pos = self.units[unit]
		for element in self.units:
			if self.units[element] > unit_pos:
				self.units[element] -= 1
		
		max_hops = self.getMultiplier(unit_pos)
		hop_distance = max_hops
		i = 0

		while i < len(self.prob):
			for remaining_hops in range(max_hops):
				# Obtain P(unit = true)
				if value == 1:
					new_prob.append(self.prob[i + hop_distance])
				# Obtain P(unit = false)
				elif value == 0:
					new_prob.append(self.prob[i])
				# Obtain P(unit = false) + P(unit = true): sumOut
				elif value == -1:
					new_prob.append(self.prob[i] + self.prob[i + hop_distance])

				i += 1
			i += hop_distance
		
		del self.units[unit]
		self.prob = new_prob


	def mul(self, factor):
		''' 
		Multiplies a factor by another, storing the result in self.
		Complexity: idk
		'''

		max_common = [-1, -1]
		factors = (self, factor)
		common_units = []

		for element in self.units:
			if element in factor.units:
				common_units.append(element)
				if max_common[0] == -1:
					max_common[0] = self.units[element]
					max_common[1] = factor.units[element]
				elif max_common[0] > self.units[element]:
					max_common[0] = self.units[element]
					max_common[1] = factor.units[element]
		
		hops = [1, 1]

		if self.getMultiplier(max_common[0]) != factor.getMultiplier(max_common[1]):
			multiplier = self.getMultiplier(max_common[0]) / float(factor.getMultiplier(max_common[1]))
			if multiplier > 1:
				hops = [1, int(multiplier)]
			else:
				hops = [int(1 / multiplier), 1]
		
		print(common_units)

		new_prob = [1] * (1 << (len(factors[0].units) + len(factors[1].units) - 2 * len(common_units)))
		for i in range(2):
			factor_index = 0
			it = 0
			while it < len(new_prob):
				hops_left = hops[i]
				while hops_left > 0:
					new_prob[it] *= factors[i].prob[factor_index]
					it += 1
					hops_left -= 1

				factor_index += 1
				if factor_index >= len(factors[i].prob):
					factor_index = 0	
	
		self.prob = new_prob

		'''
		

		self.prob = new_prob
		self.units = new_units
		'''

	def getMultiplier(self, unit_pos):
		return 1 << (len(self.units) - 1 - unit_pos)

def getFactorFromNode(node, node_index):
	new_prob = [0] * (2**(len(node.parents) + 1))
	index = 0
	for i in range(0, len(new_prob), 2):
		new_prob[i] = 1 - node.prob[index]
		new_prob[i + 1] = node.prob[index]
		index += 1
	unit_list = {}
	index = 0
	for parent in node.parents:
		unit_list[parent] = index
		index += 1
	unit_list[node_index] = index

	return Factor(new_prob, unit_list)

class Node():
	def __init__(self, prob, parents = []):
		prob = prob.tolist()
		self.prob = flatten(prob)
		
		self.parents = parents

	def show(self):
		print ("Node parents:")
		print (self.parents)
		print ("Node prob:")
		print (self.prob)

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
		# Getting query and unknown variables
		unknown = []
		query = -1
		for i in range(len(evid)):
			if evid[i] == []:
				unknown.append(i)
			elif evid[i] == -1:
				query = i
		if query == -1:
			print ("No query")
			return

		# Creating factors
		factors = []
		for i in range(len(self.nodes)):
			factors.append(getFactorFromNode(self.nodes[i], i))

		# *** STEP 1 - CUT EVIDENCE VARIABLES *** #
		for i in range(len(evid)):
			if evid[i] == 0 or evid[i] == 1:
				val = evid[i]
				for f in factors:
					f.cutOut(i, val)
		
		# *** STEP 2 - SUM_OUT *** #
		
		return 0
	
	def computeJointProb(self, evid):
		'''
		Complexity: O(n * m)
		n is the number of nodes. m is the number of the node's parents.
		'''

		res = 1
		for i in range(len(self.nodes)):
			res *= self.nodes[i].computeProb(evid)[evid[i]]
		return res