# -*- coding: utf-8 -*-
class Factor():
	def __init__(self, prob, units):
		self.prob = prob
		self.units = units
	
	def eliminate(self, unit, factors):
		dictio = {}
		return dictio

	
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
	def __init__(self, gra, prob):
		self.gra = gra
		self.prob = prob

	def computePostProb(self, evid):
		#TODO
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