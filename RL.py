# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 20:31:54 2017

@author: mlopes
"""
import numpy as np
import random

from tempfile import TemporaryFile
outfile = TemporaryFile()

# Markov Decision Process
class finiteMDP:

	def __init__(self, nS, nA, gamma, P=[], R=[], absorv=[]):

		# Finite number of states
		self.nS = nS

		# Finite number of actions
		self.nA = nA

		# Matrix that holds the values learned for each action on each state
		self.Q = np.zeros((self.nS, self.nA))

		# List that holds the expected returns with discount for each state
		self.V = np.zeros((self.nS))

		# Discount factor (0 prefers an immediate reward while 1 prefers a later reward) 
		self.gamma = gamma

		# Rate at which we want want to update the Q value (also known as learning factor)
		self.alpha = 0.01

		# Holds the probability of success of going from one state to another when performing a certain action
		if len(P)==0:
			self.P = np.zeros((self.nS, self.nA, self.nS))
		else:
			self.P = P

		# Indicates for a given state and action the immediate reward of performing such action
		if len(R)==0:
			self.R = np.zeros((self.nS, self.nA))
		else:
			self.R = R

		# List that holds all the states that have 0 reward
		if len(absorv)==0:
			self.absorv = np.zeros((self.nS))
		else:
			self.absorv = absorv

	def runPolicy(self, n, x0, poltype = 'greedy', polpar=[]):
		#DO NOT CHANGE
		traj = np.zeros((n,4))
		x = x0
		J = 0
		for ii in range(0,n):
			a = self.policy(x,poltype,polpar)
			r = self.R[x,a]
			y = np.nonzero(np.random.multinomial( 1, self.P[x,a,:]))[0][0]
			traj[ii,:] = np.array([x, a, y, r])
			J = J + r * self.gamma**ii
			if self.absorv[x]:
				y = x0
			x = y
		
		return J,traj

	def VI(self):
		#DO NOT CHANGE
		nQ = np.zeros((self.nS,self.nA))
		while True:
			self.V = np.max(self.Q,axis=1) 
			for a in range(0,self.nA):
				nQ[:,a] = self.R[:,a] + self.gamma * np.dot(self.P[:,a,:],self.V)
			err = np.linalg.norm(self.Q-nQ)
			self.Q = np.copy(nQ)
			if err<1e-7:
				break
		
		#update policy
		self.V = np.max(self.Q,axis=1) 
		#correct for 2 equal actions
		self.Pol = np.argmax(self.Q, axis=1)

		return self.Q,  self.Q2pol(self.Q)

	def traces2Q(self, trace):
		'''From a trace of the trajectory calculates the Q values for each action.'''

		# Matrix of nQ values - value of performing an action (nA) in a given state (nS)
		nQ = np.zeros((self.nS,self.nA))

		# Learning process stops when the difference between two iterations is marginal (value converges)
		while True:

			# A point in the trace has the format [0 - Initial State, 1 - Action, 2 - Final State, 3 - Reward]
			# Formula for reinforcement learning is applied to calculate the Q value for each (Action, State)
			for p in trace:
				nQ[int(p[0]),int(p[1])] += self.alpha * (p[3] + self.gamma * max(nQ[int(p[2]),:]) - nQ[int(p[0]),int(p[1])])

			# Calculates the determinant of the differences between the old values and the new learned
			# If this margin is too low means it isnt improving much and the learning process can stop
			if np.linalg.norm(self.Q-nQ) < 1e-2:
				break

			# Update matrix with new learned values
			self.Q = np.copy(nQ)

		return self.Q

	def policy(self, x, poltype, polpar = []):
		'''For a given state returns the best corresponding action according to the specified policy. This function is used to calculate trajectories.'''

		# Exploitation - Take the action with the highest Q value for this state
		if poltype == 'exploitation':

			actionsQs = self.Q2pol(polpar)[x]
			maxActionIndex = np.argmax(actionsQs)

			return int(maxActionIndex)

		# Exploration - Taking a random action for this state
		elif poltype == 'exploration':

			# Draw number between 0 and 1
			r = np.random.uniform(0,1)

			# Get entries with associated probability > random
			truth = self.P[x][self.P[x] > r]

			# Find the indices of those entries [x, action, state]
			indices = np.where(truth)
			actions = indices[0]
			actionIndex = actions[-1]

			return int(actionIndex)

	def Q2pol(self, Q):

		# States and actions
		nS = len(Q)
		nA = len(Q[0])

		# Mark on the matrix the position that has the higher Qvalue (state, action)
		pol = np.zeros((nS, nA))
		for i, line in enumerate(Q):
			pol[i][np.argmax(line)] = 1

		# Returns the matrix with the position marked
		return pol