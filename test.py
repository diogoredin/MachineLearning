from BN import *
import numpy as np

gra = [[],[],[0,1],[2],[2]]
p1 = Node( np.array([.001]), gra[0] )
p3 = Node( np.array([[.001,.29],[.94,.95]]), gra[2] )   # alarm F(A,B,E)

F2 = Factor(p3.prob, [2,0,1])
'''
print(F2.prob)
print("Sum pair:")
print(F2.sumProbPair([1,0,0], 1))
print("Sum out:")
print(F2.sumOut(1))
'''