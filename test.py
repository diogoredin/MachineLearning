from BN import *
import numpy as np

gra = [[],[0],[0],[1,2]]

'''
f1 = getFactorFromNode(p3, 2)
f1.sumOut(1)
f1.show()

f2 = getFactorFromNode(p5, 4)
f2.sumOut(2)
f2.show()

f3 = getFactorFromNode(p5, 4)
f3.cutOut(4, 0)
f3.show()
'''


p1 = Node( np.array([.5]), gra[0] )# cloudy

p2 = Node( np.array([.5,.1]), gra[1] )# sprinkler

p3 = Node( np.array([.2,.8]), gra[2] )# rain
p4 = Node( np.array([[.0,.9],[.9,.99]]), gra[3] )# wetgrass

prob = [p1,p2,p3,p4]

bn = BN(gra, prob)
evid = (-1,0,0,[])
bn.computePostProb(evid)
