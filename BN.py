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
		unknowns = []
		aux_evid = list(evid)

		# Find position of unknowns: []
		# Find position of target: -1
		for i in range(len(aux_evid)):
			if aux_evid[i] == []:
				unknowns.append(i)
			elif aux_evid[i] == -1:
				target = i

		aux_evid[target] = 1
		if unknowns == []:
			return self.computeJointProb(aux_evid)

		# Calculate Combination of True/False on the unknown position
		for i in range(len(unknowns)**2):
			for l in range(len(unknowns)):
				aux_evid[unknowns[l]] = int(i & 1 << l != 0)
				
			res += self.computeJointProb(aux_evid)

		# Sum combinations
		return res
	
	def computeJointProb(self, evid):
		res = 1
		i = 0
		for prob in self.prob:
			res *= prob.computeProb(evid)[evid[i]]
			i += 1
		return res