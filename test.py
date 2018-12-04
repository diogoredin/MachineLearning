from BN import *
import numpy as np

gra = [[],[],[0,1],[2],[2]]

p3 = Node( np.array([[.001,.29],[.94,.95]]), gra[2] )
p5 = Node( np.array([.01,.7]), gra[4] )

f1 = getFactorFromNode(p3, 2)
f1.sumOut(1)
f1.show()

f2 = getFactorFromNode(p5, 4)
f2.sumOut(4)
f2.show()