#########
# IMPORTS
#########

import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings
warnings.filterwarnings("ignore")

###########
# FUNCTIONS
###########


def features(board, prevLines, bricksLastPiece, altitudeLast, weights, nCnt, featSet):

	# variable definition
	width  = len(board[0])
	height = len(board)
	cntEroded = 0

	if featSet == 1:

		# 1. pile height
		contour = [0 for x in range(width-2)]
		for w in xrange(1,width-1):
			for h in range(height-1,0,-1):
				if board[h][w] != 1 and board[h][w] != 0:
				   contour[w-1] = height - 1 - h

		pileHeight = max(contour)

	    # 2. number of buried holes
		holeDepth   = 0
		buriedHoles = 0
		for w in xrange(0,len(contour)):
			hStart = height - 1 - contour[w]
			for h in xrange(hStart,height-1):
				if board[h][w+1] == 0:
					buriedHoles += 1
					holeDepth += contour[w]

		# 3. removed lines
		removedLines = prevLines

		# 4. altitude difference
		altitudeDiff = pileHeight - min(contour)

		# 5. maximum well depth (single width)
		# 6. sum of all wells
		# 7. sum of wells depth
		diffHeight = [0 for x in range(width-3)]
		for w in xrange(0,len(contour)-1):
			diffHeight[w] = contour[w+1] - contour[w]

		maxDepthWell = 0
		cntWell      = 0
		depthCnt     = 0
		for w in xrange(0,len(diffHeight)-1):
			if w == 0 and diffHeight[w] > 0:
				maxDepthWell = diffHeight[w]
				depthCnt    += diffHeight[w]
				cntWell += 1
			elif diffHeight[w] < 0 and diffHeight[w+1] > 0:
				depth = min([abs(diffHeight[w]), abs(diffHeight[w+1])])
				depthCnt += depth
				if depth > maxDepthWell:
					maxDepthWell = depth
				cntWell += 1
			elif w+1 == len(diffHeight)-1 and diffHeight[w+1] < 0:
				depth = abs(diffHeight[w+1])
				depthCnt += depth
				if depth > maxDepthWell:
					maxDepthWell = depth
				cntWell += 1

		# 8. landing height
		landingHeight = height - 1 - altitudeLast

		# 9. row transitions
		rowTrans = 0
		hStart   = height - 1 - max(contour)
		for h in xrange(hStart,height-1):
			for w in xrange(0,len(contour)-1):
				if board[h][w+1] == 0 and board[h][w+2] != 0:
					rowTrans += 1
				elif board[h][w+1] != 0 and board[h][w+2] == 0:
					rowTrans += 1

		# 10. column transitions
		colTrans = 0
		for w in xrange(0,len(contour)-1):
			hStart   = height - 1 - contour[w]
			for h in xrange(hStart,height-1):
				if board[h-1][w+1] == 0 and board[h][w+1] != 0:
					colTrans += 1
				elif board[h-1][w+1] != 0 and board[h][w+1] == 0:
					colTrans += 1

		# bricks of the current piece removed
		hStart    = height - 1 - min(contour)
		cntEroded = 0
		lineFlag  = 0
		for h in xrange(hStart,height-1):
			accum  = 0
			for w in xrange(0,len(contour)):
				if board[h][w+1] == 0:
					lineFlag  = 0
					accum = 0
					break
				else: 
					lineFlag = 1
					if board[h][w+1] == 14:
						accum += 1

			if lineFlag == 0:
				break
			else:
				cntEroded += accum

		# 12. eroded piece cells
		erodedCells = removedLines * bricksLastPiece

		# 13. rows with holes
		rowHole = 0
		hStart = height - 1 - max(contour)
		for h in xrange(hStart,height-1):
			for w in xrange(0,len(contour)):
				if board[h][w+1] == 0 and board[h-1][w+1] != 0:
					rowHole+=1
					break

		# Dellacherie features
		featVec = [landingHeight, erodedCells, rowTrans, colTrans, buriedHoles, depthCnt, holeDepth, rowHole]

	else:

		# 1. pile height
		contour = [0 for x in range(width-2)]
		for w in xrange(1,width-1):
			for h in range(height-1,0,-1):
				if board[h][w] != 1 and board[h][w] != 0:
				   contour[w-1] = height - 1 - h

	    # 2. number of buried holes
		buriedHoles = 0
		for w in xrange(0,len(contour)):
			hStart = height - 1 - contour[w]
			for h in xrange(hStart,height-1):
				if board[h][w+1] == 0:
					buriedHoles += 1

		# 5. contour difference
		diffHeight = [0 for x in range(width-3)]
		for w in xrange(0,len(contour)-1):
			diffHeight[w] = abs(contour[w+1] - contour[w])

		# Bertsekas and Tsitsiklis features
		cnt = 0
		featVec = [0 for x in range(len(contour) + len(diffHeight) + 2)]

		for x in xrange(0,len(featVec)):
			if cnt < len(contour):
				featVec[cnt] = contour[x]
			elif cnt >= len(contour) and cnt < len(contour) + len(diffHeight):
				featVec[cnt] = diffHeight[x - len(contour)]
			cnt += 1
		
		featVec[-2] = max(contour)
		featVec[-1] = buriedHoles

	# value of the state
	value = 0
	for x in xrange(0,len(featVec)):
		value += featVec[x] * weights[nCnt][x]

	return value, cntEroded

def getNewBoard(board, curFig, figOrient, diffLines, bricksLastPiece, altitudeLast, weights, nCnt, featSet):

	# initial orientation
	initOrient = figOrient

	# variable definition
	width  = len(board[0])
	height = len(board)

	# each piece has a different set of rotations and translations
	if curFig == 0:
		rotations = 0

	elif curFig == 1:
		rotations = 3

	elif curFig == 2:
		rotations = 3

	elif curFig == 3:
		rotations = 1

	elif curFig == 4:
		rotations = 1

	elif curFig == 5:
		rotations = 1

	elif curFig == 6:
		rotations = 3

	# create reward vector
	stateValue    = [-float('Inf') for x in range(4*(width-2))]
	bricksRemoved = [-float('Inf') for x in range(4*(width-2))]
	rCnt       = 0

	# create a matrix to store the translations used with each rotation
	possibilities = np.full((4, width-2), -1)
	finalHeight   = np.full((4, width-2), -1)
	finalTrans    = np.full((4, width-2), -1)
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
			cntTries += 1
			possibilities[rot][t-1] = cntTries
			
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

					finalHeight[rot][t-1] = figLoc[1]
					finalTrans[rot][t-1]  = figLoc[0]
					break

				# update the location of the piece
				figLoc[1] += 1

			# extract the features of the new board
			stateValue[rCnt], bricksRemoved[rCnt] = features(simBoard, diffLines, bricksLastPiece, altitudeLast, weights, nCnt, featSet)
			rCnt += 1

		# update the number of rotations
		rot += 1

	# indexes with maximum value
	maxIdx = np.array(stateValue.index(max(stateValue)))
	for w in xrange(maxIdx+1,len(stateValue)):
		if stateValue[w] == stateValue[np.array(stateValue.index(max(stateValue)))]:
			maxIdx = np.append(maxIdx, w)

	# select a random number from the optimal set
	if maxIdx.ndim != 0:
		if len(maxIdx) > 1:                               
			configuration = maxIdx[random.randint(0,len(maxIdx)-1)]
	else:
		configuration = int(maxIdx)

	# bricks removed by the configuration with the maximum value
	cntEroded =  bricksRemoved[configuration]

	# find the location and orientation that corresponds to this action
	result = np.where( possibilities == configuration+1 )

	# rotate the initial orientation
	rot = 0
	figOrient = initOrient
	while rot <= result[0]:

		if rot != 0:
			figOrient = [[figOrient[x][-y-1] for x in range(len(figOrient))] for y in range(len(figOrient[0]))]

		# update the number of rotations
		rot += 1

	# translate the figure
	figLoc = [int(finalTrans[int(result[0])][int(result[1])]), int(finalHeight[int(result[0])][int(result[1])])]

	# create a copy of the board
	simBoard = np.asarray(board)

	# update the board
	horCnt = 0
	for l in figOrient:
		verCnt = 0
		for k in l:
			if k:
				simBoard[verCnt+figLoc[1]-1][horCnt+figLoc[0]] = 14
			verCnt += 1
		horCnt += 1

	return simBoard, figLoc, cntEroded