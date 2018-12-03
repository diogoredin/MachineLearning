import numpy as np
import RL as RL

print("exercicio 1")
#exercise 1
## Env 2
# 0  1
# 2  3
# A = {Up,Down,Left,Right}
# A = {0,  1,   2,   3}
# X = {0,1,2,3}

Pl = np.zeros((4,4,4))

###
Pl[:,0,:] = np.array([	[1,0,0,0],
						[0,1,0,0],
						[1,0,0,0],
						[0,1,0,0]])

Pl[:,1,:] = np.array([	[0,0,1,0],
						[0,0,0,1],
						[0,0,1,0],
						[0,0,0,1]])

Pl[:,2,:] = np.array([	[1,0,0,0],
						[1,0,0,0],
						[0,0,1,0],
						[0,0,1,0]])

Pl[:,3,:] = np.array([	[0,1,0,0],
						[0,1,0,0],
						[0,0,0,1],
						[0,0,0,1]])

Rl = np.array([	[-1,-1,-1,0],
				[-1,0,-1,-1],
				[-1,-1,-1,0],
				[-1,0,-1,0]])

absorv = np.zeros((4,1))
absorv[-1]=1

fmdp = RL.finiteMDP(4,4,0.9,Pl,Rl,absorv)

J,traj = fmdp.runPolicy( 3000,0,poltype = "exploration")
data = np.load("Q2.npz")
Qr = fmdp.traces2Q(traj)
if np.sqrt(sum(sum((data['Q1']-Qr)**2)))<1:
	print("Aproximação de Q dentro do previsto. OK\n")
else:
	print("Aproximação de Q fora do previsto. FAILED\n")

J,traj = fmdp.runPolicy(3,1,poltype = "exploitation", polpar = Qr)
if np.sqrt(sum(sum((data['traj2']-traj)**2)))<1:
	print("Trajectória óptima. OK\n")
else:
	print("Trajectória não óptima. FAILED\n")

#exercise 2
print("exercicio 2")

data = np.load("traj2.npz")
fmdp = RL.finiteMDP(4,4,0.9)
q2 = fmdp.traces2Q(data['traj'])

if np.sqrt(sum(sum((data['Q']-q2)**2)))<1:
	print("Aproximação de Q dentro do previsto. OK\n")
else:
	print("Aproximação de Q fora do previsto. FAILED\n")
