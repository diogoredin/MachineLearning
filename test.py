from BN import *

p3 = Node( np.array([[.001,.29],[.94,.95]]), gra[2] )   # alarm F(A,B,E)

Factor(p3.prob, [2,0,1])