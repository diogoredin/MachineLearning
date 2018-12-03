# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 09:27:16 2018

@author: malopes
"""

import numpy as np
import RL as RL

print("exercicio 1")
#exercise 1
## Env 1
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
fmdp = RL.finiteMDP(7,2,0.9,Pl,Rl,absorv)

J,traj = fmdp.runPolicy( " choose this value ",3,poltype = "exploration")
data = np.load("Q1.npz")
Qr = fmdp.traces2Q(traj)
if np.sqrt(sum(sum((data['Q1']-Qr)**2)))<1:
	print("Aproximação de Q dentro do previsto. OK\n")
else:
	print("Aproximação de Q fora do previsto. FAILED\n")

J,traj = fmdp.runPolicy(3,3,poltype = "exploitation", polpar = Qr)
if np.sqrt(sum(sum((data['traj2']-traj)**2)))<1:
	print("Trajectória óptima. OK\n")
else:
	print("Trajectória não óptima. FAILED\n")
	
#exercise 2
print("exercicio 2")
data = np.load("traj.npz")
fmdp = RL.finiteMDP(8,4,0.9)
q2 = fmdp.traces2Q(data['traj'])

if np.sqrt(sum(sum((data['Q']-q2)**2)))<1:
	print("Aproximação de Q dentro do previsto. OK\n")
else:
	print("Aproximação de Q fora do previsto. FAILED\n")
