from BN import *
import numpy as np

gra = [[],[0],[0],[1,2]]
p3 = Node( np.array([.2,.8]), gra[2] )# rain
p4 = Node( np.array([[.0,.9],[.9,.99]]), gra[3] )# wetgrass

f1 = getFactorFromNode(p4, 3)
f1.show()
f1.sumOut(1)
f1.show()