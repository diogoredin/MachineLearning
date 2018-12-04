# -*- coding: utf-8 -*-

import copy

class Factor():
	def __init__(self, prob, unit_list, from_node):
		prob_list = [0]*(2**len(unit_list))
		print(prob_list)
		if len(prob) == 1:
			self.prob = [1 - prob[0], prob[0]]
		else:
			self.prob = prob
		
			if from_node:
				list_negative = copy.deepcopy(self.prob)

				for i in range(2**(len(unit_list)-1)):
					l = list_negative
					idx = makeIdxCombo(len(unit_list)-1, i)

					for index in idx[:-1]:
						l = l[int(index)]
					l[idx[-1]] = 1 - l[idx[-1]]

				self.prob = [list_negative, self.prob]
		self.unit_list = unit_list

	def getProb(self, evid):
		p = self.prob
		for val in evid[1:]:
			p = p[val]
		return p

	def sumOut(self, unit):
		evid = []
		for i in range(len(self.unit_list)):
			evid.append(0)
			if unit == self.unit_list[i]:
				unit_pos = i
				break

		new_prob = []
		for i in range(2**(len(self.unit_list))):

			idx = makeIdxCombo(len(self.unit_list), i)
			new_idx = idx.copy()
			new_idx.pop(unit_pos)
			iterator = new_prob
			for index in new_idx:
				
				if len(iterator) == 0:
					iterator.extend([[],[]])

			val = self.sumProbPair(idx,unit_pos)
			for index in new_idx[:-1]:
				iterator = iterator[index]
			iterator.append(val)
		
		return iterator

	def sumProbPair(self, idx, unit_pos):
		prob = self.prob
		val1 = 0
		val2 = 0
		idx[unit_pos] = 0
		for index in idx:
			prob = prob[index]
		val1 = prob
		idx[unit_pos] = 1
		prob = self.prob
		for index in idx:
			prob = prob[index]
		val2 = prob
		return val1 + val2

class Node():
	def __init__(self, prob, parents = []):
		self.prob = prob
		self.parents = parents

	def computeProb(self, evid):

		# If there are no parents, the probability is trivial
		if self.parents == []:
			p = self.prob[0]

		# If there are parents, evaluate each parent
		else:
			p = self.prob
			for dad in self.parents:
				p = p[evid[dad]]

		# Returns a tuple corresponding to: (P(self = false), P(self = true))
		return (1 - p, p)
	
class BN():
	def __init__(self, gra, nodes):
		self.gra = gra
		self.nodes = nodes

	def computePostProb(self, evid):

		# Create a list of factors corresponding to : [index,parents,...]
		factors = []
		for i in range(len(self.nodes)):
			unit_list = []
			unit_list.append(i)
			for dad in self.nodes[i].parents:
				unit_list.append(dad)
			factors.append(Factor(self.nodes[i].prob, unit_list, True))

		return 0

		ign = []
		for i in range(len(evid), 0, -1):
			if evid[i] == []:
				ign.append(i)
			elif evid[i] == -1:
				query = i
	
		return 0
	
	def computeJointProb(self, evid):
		res = 1
		i = 0
		for prob in self.nodes:
			res *= prob.computeProb(evid)[evid[i]]
			i += 1
		return res

def makeIdxCombo(size, i):
	idx = []
	for binary in range(size):
		idx.append(int(i & 1 << binary != 0))
	return idx