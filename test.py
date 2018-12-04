from BN import *
import numpy as np

gra = [[],[],[0,1],[2],[2]]
p3 = Node([[.001,.29],[.94,.95]], gra[2] )   # alarm F(A,B,E)

Factor(p3.prob, [2,0,1])