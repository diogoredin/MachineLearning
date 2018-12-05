from BN import *
import numpy as np

gra = [[],[0],[0]]

p1 = Node([0.5], gra[0]) # Probability that it's raining
p2 = Node([0.8, 0.1], gra[1]) # Probability that i go to the beach
p3 = Node([0.2, 0.8], gra[2]) # Probability that there are waves

prob = [p1,p2,p3]

ev = [-1, 1, 1]
bn = BN(gra, prob)

print("For event " + str(ev))
print("probability is: " + str(bn.computePostProb(ev)))