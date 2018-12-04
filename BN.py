# -*- coding: utf-8 -*-

import copy

class Factor():
	def __init__(self, prob, unit_list):
		prob = list(prob)
		if len(prob) == 1:
			self.prob = prob[0]
		else:
			self.prob = prob

		list_negative = copy.deepcopy(self.prob)

		for i in range((len(unit_list)-1)**2):
			idx = []
			for binary in range(len(unit_list)-1):
				idx.append(int(i & 1 << binary != 0))
			l = list_negative
			for index in idx[:-1]:
				l = l[int(index)]
			l[idx[-1]] = 1 - l[idx[-1]]

		self.prob = [list_negative, self.prob]
		print(self.prob)

	def getProb(self, evid):
		p = self.prob
		for val in evid[1:]:
			p = p[val]
		if evid[1] == 0:
			p = 1 - p
		return p

	# def multiply(self, factorB):
	# def sumOut(self, unit, factors):
		# evid = ()
		# self.getProb()

class Node():
	def __init__(self, prob, parents = []):
		self.prob = prob
		self.parents = parents

	def computeProb(self, evid):
		#If there are no parents, the probability is trivial
		if self.parents == []:
			p = self.prob[0]
		#If there are parents, evaluate each parent
		else:
			p = self.prob
			for dad in self.parents:
				p = p[evid[dad]]

		#Returns a tuple corresponding to: (P(self = false), P(self = true))
		return (1 - p, p)
	
class BN():
	def __init__(self, gra, nodes):
		self.gra = gra
		self.nodes = nodes

	def computePostProb(self, evid):

		# Create a list corresponding to : [index,parents,...]
		factors = []
		for i in range(len(self.nodes)):
			unit_list = []
			unit_list.append(i)
			for dad in self.nodes[i].parents:
				unit_list.append(dad)
			factors.append(Factor(self.nodes.prob, unit_list))

		# F1 = Factor(earthquakeNode.prob, unit_list)
		# F2 = Factor(alarmNode.prob, unit_list)
		# F1.multiply(F2)

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
		for prob in self.prob:
			res *= prob.computeProb(evid)[evid[i]]
			i += 1
		return res