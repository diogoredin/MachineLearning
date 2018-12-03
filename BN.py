# -*- coding: utf-8 -*-

class Node():
	def __init__(self, prob, parents = []):
		self.prob = prob
		self.parents = parents

	def computeProb(self, evid):
		#TODO - THIS ONLY WORKS FOR JOINT PROB, FIX IT

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

		res = 0
		# Find position of unknown
		# Find position of target
		# Calculate Combination of True/False on the unknown position
		# Sum combinations

		return res
		
	
	def computeJointProb(self, evid):
		res = 1
		i = 0
		for prob in self.prob:
			res *= prob.computeProb(evid)[evid[i]]
			i += 1
		return res