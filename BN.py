# -*- coding: utf-8 -*-

import copy

class Factor():
	def __init__(self, prob, unit_list):
		prob_list = [0]*(2**len(unit_list))
		if len(prob_list) == 2:
			prob_list[1] = prob[0]
			prob_list[0] = 1 - prob[0]
		else:
			for i in range(2**(len(unit_list)-1)):
				aux_prob = prob
				idx = []
				val = 0
				for binary in range(len(unit_list) - 1):
					idx.insert(0,int(i & 1 << binary != 0))
				for index in idx:
					aux_prob = aux_prob[index]
				print (aux_prob)
				putOnList(prob_list, idx, aux_prob)
			
		print(prob_list)

def getFromList(l, index):
	actual_index = 0
	for i in range(len(index)):
		if index[i] != 0:
			actual_index += 1 << i
	return l[actual_index]



def putOnList(l, index, val):
	actual_index = 0
	for i in range(len(index)):
		if index[i] != 0:
			actual_index += 1 << i
	l[actual_index] = val

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