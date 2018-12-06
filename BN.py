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
		
	def sumOut(self, factor):
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
		if value = -1 sums out the *unit* variable. unit is the variable index in the node.
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
		Complexity: idk
		'''

		max_common = [-1, -1]
		factors = (self, factor)
		common_units = []
		new_units = {}

		for element in self.units:
			if element in factor.units:
				common_units.append(element)

			if element not in new_units:
				updateDict(new_units, element)

		for element in factor.units:
			if element not in new_units:
				updateDict(new_units, element)

		new_prob = [1] * (1 << (len(factors[0].units) + len(factors[1].units) - len(common_units)))

		for i in range(1 << len(new_units)):
			new_prob[i] = self.getProb(i, new_units) * factor.getProb(i, new_units)

		return Factor(new_prob, new_units)

	def getMultiplier(self, unit_pos):
		return 1 << (len(self.units) - 1 - unit_pos)

	def normalize(self):
		add = self.prob[0] + self.prob[1]
		self.prob[0] /= add
		self.prob[1] /= add

	def getProb(self, evid, new_units):
		index = 0
		mul = len (self.units) - 1

		for unit in self.units:
			index += int(evid & 1 << len (new_units) - 1 - new_units[unit] != 0) << mul - self.units[unit]
		return self.prob[index]


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


def updateDict(d, val):
	pos = len(d)
	for i in d:
		if i > val:
			if pos > d[i]:
				pos = d[i]
			d[i] += 1
	d[val] = pos


class Node():
	def __init__(self, prob, parents = []):
		if type(prob) != list:
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
		# Getting query and unknown variables
		unknown = []
		
		for i in range(len(evid)):
			if evid[i] == []:
				unknown.append(i)		

		# Creating factors
		factors = []
		for i in range(len(self.nodes)):
			factors.append(getFactorFromNode(self.nodes[i], i))

		# *** STEP 1 - CUT EVIDENCE VARIABLES *** #
		for i in range(len(evid)):
			val = evid[i]
			if val == 0 or val == 1:
				for findex in range(len(factors)):
					factors[findex] = factors[findex].cut(i, val)
		# *** STEP 2 - SUM_OUT *** #

		factor_val = (0, 1)

		while len(unknown):
			sum_var = unknown[-1]
			unknown = unknown[:-1]
			to_sum = []
			factor_sums = [Factor([1.0],{}), Factor([1.0],{})]

			
			for f in factors:
				if sum_var in f.units:
					to_sum.append(f)
			for val in factor_val:
				for f in to_sum:
					factor_sums[val] = factor_sums[val].mul(f.cut(sum_var, val))

			
			if len(factor_sums[0].units) != 0:
				factor_sums[0].sumOut(factor_sums[1])
				factors.append(factor_sums[0])

			for f in to_sum:
				factors.remove(f)
		
		f_res = Factor([1], {})
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