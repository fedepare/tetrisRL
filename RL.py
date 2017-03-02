#########
# IMPORTS
#########

import numpy as np

###########
# FUNCTIONS
###########

def contours(f):

	# define width and height
	width  = len(f[0])
	height = len(f)

	# ASSUMPTION: only the contour of the well is considered
	# contour vector: maximum occupied hight for each column
	contourVec = [height-1 for x in range(width-2)]

	# go through the array for contour computation
	for w in xrange(1,width-1):
		for h in range(height-1,0,-1):
			if f[h][w] != 1 and f[h][w] != 0:
			   contourVec[w-1] = h

	# ASSUMPTION: Separate the contour vector in all the 4-block combinations
	init    = 0
	numComb = len(contourVec) - 3
	contSubsets = [[0 for x in range(4)] for y in range(numComb)]
	
	for x in xrange(0,numComb):
		contSubsets[x][:] = contourVec[init:init+4]
		init += 1

	# difference in height computation
	diffSubsets = [[0 for x in range(3)] for y in range(numComb)]

	for x in xrange(0,numComb):
		for w in xrange(0, 3):
			diffSubsets[x][w] = contSubsets[x][w] - contSubsets[x][w+1]
			if diffSubsets[x][w] > 3:
				diffSubsets[x][w] = 3
			elif diffSubsets[x][w] < -3:
				diffSubsets[x][w] = -3

	# outputs
	return contSubsets, diffSubsets

def computeReward(contSubsets, diffSubsets):




	reward = 0
	return reward
