# -*- coding: utf-8 -*-

def flatten(l):

	'''
	Flattens a list with an arbitrary number of dimensions, creating a single, one dimensional list.
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

		unit_pos = -1
		
		for i in range(len(self.units)):
			if unit == self.units[i]:
				unit_pos = i

		if unit_pos == -1:
			print("No variable to cut")
			return

		max_hops = 2**(len(self.units) - 1 - unit_pos)
		hop_distance = max_hops
		print (max_hops)

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
				remaining_hops -= 1
				i += 1
			i += hop_distance
		
		del self.units[unit_pos]
		self.prob = new_prob

		
		

def getFactorFromNode(node, node_index):
	new_prob = [0] * (2**(len(node.parents) + 1))
	halfway = len(new_prob) // 2
	new_prob[halfway:] = node.prob

	for i in range(halfway):
		new_prob[i] = 1 - new_prob[i + halfway]

	
	unit_list = [0] * (len(node.parents) + 1)
	unit_list[0] = node_index
	unit_list[1:] = node.parents

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
		
		return (1 - p, p)

class BN():
	def __init__(self, gra, nodes):
		self.gra = gra
		self.nodes = nodes

	def computePostProb(self, evid):
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
