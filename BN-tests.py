import numpy as np
np.set_printoptions(precision=4, suppress=True)

from BN import *

''' TEST SET 1 '''
print("Test Set 1: ")
print()

gra = [[],[],[0,1],[2],[2]]
ev = (1,1,0,1,1)
	
p0 = Node(np.array([.001]), gra[0])                   # burglary F(B)
print("p0 = 0: %.4g p0 = 1: %.4g" % (p0.computeProb(ev)[0] , p0.computeProb(ev)[1])) 
print()

p1 = Node(np.array([.002]), gra[1])                   # earthquake F(E)

p2 = Node(np.array([[.001,.29],[.94,.95]]), gra[2])   # alarm F(A,B,E)
print("p0 = 1, p1 = 1 | p2 = 0: %.4g p2 = 1: %.4g" % (p2.computeProb(ev)[0] , p2.computeProb(ev)[1])) 
print()
p3 = Node(np.array([.05,.9]), gra[3])                 # johncalls F(A,J)

p4 = Node(np.array([.01,.7]), gra[4])                 # marycalls F(A,M)

nodes = [p0,p1,p2,p3,p4]	

gra = [[],[],[0,1],[2],[2]] 
bn = BN(gra, nodes)

jp = []
for e1 in [0,1]:
	for e2 in [0,1]:
		for e3 in [0,1]:
			for e4 in [0,1]:
				for e5 in [0,1]:
					jp.append(bn.computeJointProb((e1, e2, e3, e4, e5)))

print("Sum Joint %.3f (1)" % sum(jp))
print()

ev = (-1,[],[],1,1)
print("For evidence : " + str(ev))
print("Post : %.4g (0.2842)" % bn.computePostProb(ev))
print()

ev = ([],-1,[],1,1)
print("For evidence : " + str(ev))
print("Post : %.3f (0.176)" % bn.computePostProb(ev))
print()

ev = ([],0,1,-1,[])
print("For evidence : " + str(ev))
print("Post : %.3f (0.900)" % bn.computePostProb(ev))
print()


''' TEST SET 2 '''
print("Test Set 2: ")
print()

gra = [[],[0],[0],[1,2]]
ev = (1,1,1,1)

p0 = Node(np.array([.5]), gra[0])# cloudy
print("p1 false %.4g p1 true %.4g" % (p0.computeProb(ev)[0] , p0.computeProb(ev)[1])) 
print()

p1 = Node(np.array([.5,.1]), gra[1])# sprinkler

p2 = Node(np.array([.2,.8]), gra[2])# rain
p3 = Node(np.array([[.0,.9],[.9,.99]]), gra[3])# wetgrass
print("p2 = 1, p3 = 1, p4 false %.4g p4 true %.4g" % (p3.computeProb(ev)[0] , p3.computeProb(ev)[1]))
print()

prob = [p0,p1,p2,p3]

bn = BN(gra, prob)
jp = []
for e1 in [0,1]:
	for e2 in [0,1]:
		for e3 in [0,1]:
			for e4 in [0,1]:
				jp.append(bn.computeJointProb((e1, e2, e3, e4)))
print("Sum Joint %.3f (1)" % sum(jp))
print()

### Tests to joint Prob
ev = (0,0,0,0)
print("For evidence : " + str(ev))
print("Joint %.4g (0.2)" % bn.computeJointProb(ev)) 
print()

ev = (1,1,1,1)
print("For evidence : " + str(ev))
print("Joint %.4g (0.0396)" % bn.computeJointProb(ev))
print()

### Tests to post Prob
# P(e1|e4=1)
ev = (-1,[],[],1)
print("For evidence : " + str(ev))
print("Post : %.4g (0.5758)" % bn.computePostProb(ev))
print()

# P(e4|e1=1)
ev = (1,[],[],-1)
print("For evidence : " + str(ev))
print("Post : %.4g (0.7452)" % bn.computePostProb(ev))
print()

# P(e1|e2=0,e3=0)

ev = (-1,0,0,[])
print("For evidence : " + str(ev))
print("Post : %.4g (0.3103)" % bn.computePostProb(ev))
print()
