# -*- coding: utf-8 -*-
"""TG17, 83405 Joao Neves, 84711 Diogo Redin"""
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
			self.R = np.zeros((self.nA, self.nS))
		else:
			self.R = R

		# List that holds all the states that have 0 reward
		if len(absorv)==0:
			self.absorv = np.zeros((self.nS))
		else:
			self.absorv = absorv

	def runPolicy(self, n, x0,  poltype = 'greedy', polpar=[]):
		#nao alterar
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
		#nao alterar
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

		# Matrix of Q values - value of performing an action (nA) in a given state (nS)
		tempQ = np.zeros((self.nS,self.nA))

		# Learning process stops when the difference between two iterations is marginal (value converges)
		while True:

			# A point in the trace has the format [0 - Initial State, 1 - Action, 2 - Final State, 3 - Reward]
			# Formula for reinforcement learning is applied to calculate the Q value for each (Action, State)
			for p in trace:

				initialState = int(p[0])
				action = int(p[1])
				finalState = int(p[2])
				reward = p[3]

				# Reinforcement formula
				tempQ[initialState,action] += self.alpha * (reward + self.gamma * max(tempQ[finalState,:]) - tempQ[initialState,action])

			# Calculates the determinant of the differences between the old values and the new learned
			# If this margin is too low means it isnt improving much and the learning process can stop
			if np.linalg.norm(self.Q-tempQ) < 1e-2:
				break

			# Update matrix with new learned values
			self.Q = np.copy(tempQ)

		return self.Q

	def policy(self, x, poltype, polpar = []):
		'''For a given state returns the best corresponding action according to the specified policy. This function is used to calculate trajectories.'''

		# Exploitation - Take the action with the highest Q value for this state
		if poltype == 'exploitation':
			
			# States and actions
			nS = len(polpar)
			nA = len(polpar[0])

			# Mark on the matrix the position that has the higher Qvalue (state, action)
			pol = np.zeros((nS, nA))
			for state, action in enumerate(polpar):
				pol[state][np.argmax(action)] = 1

			# Q values are given and we chose the action with the highest
			actionsQs = pol[x]
			maxActionIndex = np.argmax(actionsQs)

			return int(maxActionIndex)

		# Exploration - Taking a random action for this state
		elif poltype == 'exploration':

			# Find the indices of those entries [x, action, state] with p > 0
			indices = np.where(self.P[x] > 0)
			actions = indices[0]

			# Choose a random one
			actionIndex = random.choice(actions)

			return int(actionIndex)

	def Q2pol(self, Q, eta=5):
		return np.exp(eta*Q)/np.dot(np.exp(eta*Q),np.array([[1,1],[1,1]]))