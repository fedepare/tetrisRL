#########
# IMPORTS
#########

import numpy as np
import random

###########
# FUNCTIONS
###########

def features(figIdx, nextfigIdx, figOrient, board):

	# variable definition
	width  = len(board[0])
	height = len(board)
	
	# 1. current figure
	curFig = ""

	if figIdx == 0:
		curFig = "O"
	elif figIdx == 1:
		curFig = "J"
	elif figIdx == 2:
		curFig = "L"
	elif figIdx == 3:
		curFig = "I"
	elif figIdx == 4:
		curFig = "Z"
	elif figIdx == 5:
		curFig = "S"
	elif figIdx == 6:
		curFig = "T"

	# 2. next figure
	nxtFig = ""

	if nextfigIdx == 0:
		nxtFig = "O"
	elif nextfigIdx == 1:
		nxtFig = "J"
	elif nextfigIdx == 2:
		nxtFig = "L"
	elif nextfigIdx == 3:
		nxtFig = "I"
	elif nextfigIdx == 4:
		nxtFig = "Z"
	elif nextfigIdx == 5:
		nxtFig = "S"
	elif nextfigIdx == 6:
		nxtFig = "T"

	# 3. board height
	accum   = 0
	contour = [0 for x in range(width-2)]
	for w in xrange(1,width-1):
		for h in range(height-1,0,-1):
			if board[h][w] != 1 and board[h][w] != 0:
			   contour[w-1] = height - 1 - h
			   accum       += contour[w-1]
	
	boardHeight = accum / (width-2)

	# 4. board level
	boardLevel = 1
	diffHeight = [0 for x in range(width-3)]
	for w in xrange(0,len(contour)-1):
		diffHeight[w] = contour[w+1] - contour[w]
		if diffHeight[w] > 3 or diffHeight[w] < -3:
			boardLevel = 0

	# 5. single and multiple (unit-width) valley
	counter        = 0
	singleValley   = 0
	multipleValley = 0
	for w in xrange(0,len(diffHeight)-1):
		if diffHeight[w] < 0 and diffHeight[w+1] > 0:
			singleValley = 1
			counter += 1
		elif w == 0 and diffHeight[w] > 0:
			singleValley = 1
			counter += 1
		elif w+1 == len(diffHeight)-1 and diffHeight[w+1] < 0:
			singleValley = 1
			counter += 1

	if counter > 1:
		singleValley   = 0
		multipleValley = 1

	# 6. number of buried holes
	buriedHoles = 0
	for w in xrange(0,len(contour)):
		hStart = height - 1 - contour[w]
		for h in xrange(hStart,height-1):
			if board[h][w+1] == 0:
				buriedHoles += 1

	return curFig, nxtFig, boardHeight, boardLevel, singleValley, multipleValley, buriedHoles

def buried(board):

	# variable definition
	width  = len(board[0])
	height = len(board)

	# contour
	contour = [0 for x in range(width-2)]
	for w in xrange(1,width-1):
		for h in range(height-1,0,-1):
			if board[h][w] != 1 and board[h][w] != 0:
			   contour[w-1] = height - 1 - h

    # number of buried holes
	buriedHoles = 0
	for w in xrange(0,len(contour)):
		hStart = height - 1 - contour[w]
		for h in xrange(hStart,height-1):
			if board[h][w+1] == 0:
				buriedHoles += 1

	return buriedHoles

def minimizeBuriedHoles(board, curFig, figOrient):

	# variable definition
	width  = len(board[0])
	height = len(board)

	# each piece has a different set of rotations and translations
	if curFig == "O":
		rotations = 0

	elif curFig == "J":
		rotations = 3

	elif curFig == "L":
		rotations = 3

	elif curFig == "I":
		rotations = 1

	elif curFig == "Z":
		rotations = 1

	elif curFig == "S":
		rotations = 1

	elif curFig == "T":
		rotations = 3

	# create reward vector
	reward = [1e6 for x in range(32)]
	rCnt   = 0

	# create a matrix to store the translations used with each rotation
	possibilities = np.full((4, 8), -1)
	cntTries      = 0

	# rotate the figure
	rot = 0
	while rot <= rotations:
		
		# current orientation
		if rot != 0:
			figOrient = [[figOrient[x][-y-1] for x in range(len(figOrient))] for y in range(len(figOrient[0]))]
		
		# width of the figure with the current orientation
		wFig = len(figOrient)
		
		# number of possible translations for the current orientation
		numTrans = width - 2 - wFig + 1

		# evaluate the board with all the possible translations
		for t in xrange(1,numTrans+1):

			# store the try
			possibilities[rot][t-1] = cntTries
			cntTries += 1

			# create a copy of the board
			simBoard = np.asarray(board)
			
			# location of the figure
			figLoc = [t, 0]

			# initialize collision flag
			collision = 0

			# board update
			while True:

				# detect collision (CHANGE SOMETHING HERE)
				horCnt = 0
				for l in figOrient:
					verCnt = 0
					for k in l:

						if board[verCnt+figLoc[1]][horCnt+figLoc[0]] and k:
							collision = 1

						verCnt += 1
					horCnt += 1

				# update the simulated board with the current piece
				if collision:
					horCnt = 0
					for l in figOrient:
						verCnt = 0
						for k in l:
							if k:
								simBoard[verCnt+figLoc[1]-1][horCnt+figLoc[0]] = 14
							verCnt += 1
						horCnt += 1
					break

				# update the location of the piece
				figLoc[1] += 1

			# count the number of buried holes
			reward[rCnt] = buried(simBoard)
			rCnt += 1

		# update the number of rotations
		rot += 1

	# indexes with minimum (maximum) reward
	minIdx = np.array(reward.index(min(reward)))
	for w in xrange(minIdx+1,len(reward)):
		if reward[w] == reward[np.array(reward.index(min(reward)))]:
			minIdx = np.append(minIdx, w)

	# select a random number from the optimal set
	print minIdx
	action = random.choice(minIdx) # CAMBIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARLO

	# find the location and orientation that corresponds to this action
	result = np.where( possibilities == action )

	print action
	print possibilities
	print result[0]
	print result[1]