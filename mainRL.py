# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 09:27:16 2018

@author: malopes
"""

import numpy as np
import RL as RL

#------------------------------- EXERCISE 1 -------------------------------#
print("Exercise 1")

# Data
Pl = np.zeros((7,2,7))
Pl[0,0,1]=1
Pl[1,0,2]=1
Pl[2,0,3]=1
Pl[3,0,4]=1
Pl[4,0,5]=1
Pl[5,0,6]=0.9
Pl[5,0,5]=0.1
Pl[6,0,6]=1
Pl[0,1,0]=1
Pl[1,1,1]=0
Pl[1,1,0]=1
Pl[2,1,1]=1
Pl[3,1,2]=1
Pl[4,1,3]=1
Pl[5,1,4]=1
Pl[6,1,5]=1

Rl = np.zeros((7,2))
Rl[[0,6],:]=1
absorv = np.zeros((7,1))
absorv[[0,6]]=1

# Constructor
fmdp = RL.finiteMDP(7,2,0.9,Pl,Rl,absorv)

# Generate an optimal trajectory according to Exploration
J,traj = fmdp.runPolicy(3000,3,poltype = "exploration")

# Calculate the Q values of the trajectory chosen
Qr = fmdp.traces2Q(traj)

# Print results
# np.set_printoptions(threshold=np.nan)

# result = [list(tupl) for tupl in {tuple(item) for item in traj }]
# for r in result:
# 	print(r)
# 	print("_____________________________________")

print(np.sum(fmdp.VI()))

J,traj = fmdp.runPolicy(3000,3,poltype = "exploitation", polpar = Qr)

print(np.sum(fmdp.VI()))

#print(Rl)
#print(traj)
#print(Qr)

# Check results
data = np.load("Q1.npz")
if np.sqrt(sum(sum((data['Q1']-Qr)**2)))<1:
	print("Aproximação de Q dentro do previsto (calcula traj com exploration). OK\n")
else:
	print("Aproximação de Q fora do previsto (calcula traj com exploration). FAILED\n")

# Generate an optimal trajectory according to Exploration
J,traj = fmdp.runPolicy(3,3,poltype = "exploitation", polpar = Qr)

# Print results
# print(traj)

# Check results
if np.sqrt(sum(sum((data['traj2']-traj)**2)))<1:
	print("Trajectória óptima (calcula traj com exploitation). OK\n")
else:
	print("Trajectória não óptima (calcula traj com exploitation). FAILED\n")

#------------------------------- EXERCISE 2 -------------------------------#
print("Exercise 2")

# Data
data = np.load("traj.npz")

# Constructor
fmdp = RL.finiteMDP(8,4,0.9)

# Calculate the Q values of the given trajectory
q2 = fmdp.traces2Q(data['traj'])
#print(data['traj'])
#print(q2)

# Check results
if np.sqrt(sum(sum((data['Q']-q2)**2)))<1:
	print("Aproximação de Q dentro do previsto. OK\n")
else:
	print("Aproximação de Q fora do previsto. FAILED\n")
