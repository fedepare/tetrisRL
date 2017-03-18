import math
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

NUM_COLORS = 8
cm = plt.get_cmap('gist_rainbow')

grid = True

############################################################################################
# LEARNING CURVES - COMPARISON

# LEARNING

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard_LEARNING_COMPLETE.dat", "rb") as f:
    BNoN1 = pickle.load(f)

with open("/home/fedepare/tetrisRL/results/biggerBoard_DecNoise_LEARNING_COMPLETE.dat", "rb") as f:
    resultsDecNoise = pickle.load(f)

with open("/home/fedepare/tetrisRL/results/biggerBoard_CnstNoise_LEARNING_COMPLETE.dat", "rb") as f:
    resultsCnstNoise = pickle.load(f)

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(1)
ax = fig.gca()
ax.set_xlabel('Iterations', fontsize=15)
ax.set_ylabel('Cleared lines', fontsize=15)

fede = [x for x in xrange(0,81)]
ax.plot(fede, BNoN1, linewidth=2, label="No Noise",linestyle="-")
ax.plot(fede, resultsDecNoise, linewidth=2, label="Dec Noise",linestyle="-")
ax.plot(fede, resultsCnstNoise, linewidth=2, label="Cnst Noise",linestyle="-")

ax.set_yscale('log')
ax.set_ylim([10**0,10**3])
ax.legend(loc=4)
ax.grid(grid)
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

############################################################################################
# WEIGHTS AND STD DEVIATION - NO NOISE

# STANDARD DEVIATION

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    sigma = np.asarray(BNoN1[1])

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(2)
ax = fig.gca()
ax.set_xlabel('Iterations', fontsize=15)
ax.set_ylabel('Std Deviation', fontsize=15)
ax.set_ylim([0,18])

fede = [x for x in xrange(0,41)]
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

for y in xrange(0,len(sigma[0])):
	vector = [10 for z in xrange(0,41)]
	for x in xrange(1,len(sigma)+1):
		vector[x] = sigma[x-1][y]
	ax.plot(fede, vector, linewidth=2, label="w" + str(y+1))

sigmaLast = sigma

with open("/home/fedepare/tetrisRL/results/biggerBoard_continue.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    sigma = np.asarray(BNoN1[1])

fede = [x for x in xrange(40,81)]
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

for y in xrange(0,len(sigma[0])):
	vector = [sigmaLast[-1][y] for z in xrange(0,41)]
	for x in xrange(1,len(sigma)+1):
		vector[x] = sigma[x-1][y]
	ax.plot(fede, vector, linewidth=2)

ax.legend(loc=1)
ax.grid(grid)

# WEIGHTS

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    weights = np.asarray(BNoN1[0])

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(3)
ax = fig.gca()
ax.set_xlabel('iterations', fontsize=15)
ax.set_ylabel('Weights', fontsize=15)
ax.set_ylim([-20,10])

ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

fede = [x for x in xrange(0,41)]
for y in xrange(0,len(weights[0])):
	vector = [0 for z in xrange(0,41)]
	for x in xrange(1,len(weights)+1):
		vector[x] = weights[x-1][y]
	ax.plot(fede, vector, linewidth=2, label="w" + str(y+1))

weightsLast = weights

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard_continue.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    weights = np.asarray(BNoN1[0])

fede = [x for x in xrange(40,81)]
for y in xrange(0,len(weights[0])):
	vector = [weightsLast[-1][y] for z in xrange(0,41)]
	for x in xrange(1,len(weights)+1):
		vector[x] = weights[x-1][y]
	ax.plot(fede, vector, linewidth=2)

ax.legend(loc=4)
ax.grid(grid)

############################################################################################
# WEIGHTS AND STD DEVIATION - LINEARLY DECREASING NOISE

# STANDARD DEVIATION

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard_DecNoise.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    sigma = np.asarray(BNoN1[1])

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(4)
ax = fig.gca()
ax.set_xlabel('Iterations', fontsize=15)
ax.set_ylabel('Std Deviation', fontsize=15)
ax.set_ylim([0,18])

fede = [x for x in xrange(0,41)]
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

for y in xrange(0,len(sigma[0])):
	vector = [10 for z in xrange(0,41)]
	for x in xrange(1,len(sigma)+1):
		vector[x] = sigma[x-1][y]
	ax.plot(fede, vector, linewidth=2, label="w" + str(y+1))

sigmaLast = sigma

with open("/home/fedepare/tetrisRL/results/biggerBoard_DecNoise_continue.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    sigma = np.asarray(BNoN1[1])

fede = [x for x in xrange(40,81)]
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

for y in xrange(0,len(sigma[0])):
	vector = [sigmaLast[-1][y] for z in xrange(0,41)]
	for x in xrange(1,len(sigma)+1):
		vector[x] = sigma[x-1][y]
	ax.plot(fede, vector, linewidth=2)

ax.legend(loc=1)
ax.grid(grid)

# WEIGHTS

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard_DecNoise.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    weights = np.asarray(BNoN1[0])

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(5)
ax = fig.gca()
ax.set_xlabel('iterations', fontsize=15)
ax.set_ylabel('Weights', fontsize=15)
ax.set_ylim([-20,10])
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

fede = [x for x in xrange(0,41)]
for y in xrange(0,len(weights[0])):
	vector = [0 for z in xrange(0,41)]
	for x in xrange(1,len(weights)+1):
		vector[x] = weights[x-1][y]
	ax.plot(fede, vector, linewidth=2, label="w" + str(y+1))

weightsLast = weights

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard_DecNoise_continue.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    weights = np.asarray(BNoN1[0])

fede = [x for x in xrange(40,81)]
for y in xrange(0,len(weights[0])):
	vector = [weightsLast[-1][y] for z in xrange(0,41)]
	for x in xrange(1,len(weights)+1):
		vector[x] = weights[x-1][y]
	ax.plot(fede, vector, linewidth=2)

ax.legend(loc=4)
ax.grid(grid)


############################################################################################
# WEIGHTS AND STD DEVIATION - CONSTANT NOISE

# STANDARD DEVIATION

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard_CnstNoise.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    sigma = np.asarray(BNoN1[1])

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(6)
ax = fig.gca()
ax.set_xlabel('Iterations', fontsize=15)
ax.set_ylabel('Std Deviation', fontsize=15)
ax.set_ylim([0,18])

fede = [x for x in xrange(0,41)]
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

for y in xrange(0,len(sigma[0])):
	vector = [10 for z in xrange(0,41)]
	for x in xrange(1,len(sigma)+1):
		vector[x] = sigma[x-1][y]
	ax.plot(fede, vector, linewidth=2, label="w" + str(y+1))

sigmaLast = sigma

with open("/home/fedepare/tetrisRL/results/biggerBoard_CnstNoise_continue.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    sigma = np.asarray(BNoN1[1])

fede = [x for x in xrange(40,81)]
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

for y in xrange(0,len(sigma[0])):
	vector = [sigmaLast[-1][y] for z in xrange(0,41)]
	for x in xrange(1,len(sigma)+1):
		vector[x] = sigma[x-1][y]
	ax.plot(fede, vector, linewidth=2)

ax.legend(loc=1)
ax.grid(grid)

# WEIGHTS

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard_CnstNoise.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    weights = np.asarray(BNoN1[0])

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(7)
ax = fig.gca()
ax.set_xlabel('iterations', fontsize=15)
ax.set_ylabel('Weights', fontsize=15)
ax.set_ylim([-20,10])
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

fede = [x for x in xrange(0,41)]
for y in xrange(0,len(weights[0])):
	vector = [0 for z in xrange(0,41)]
	for x in xrange(1,len(weights)+1):
		vector[x] = weights[x-1][y]
	ax.plot(fede, vector, linewidth=2, label="w" + str(y+1))

weightsLast = weights

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard_CnstNoise_continue.dat", "rb") as f:
    BNoN1 = pickle.load(f)
    weights = np.asarray(BNoN1[0])

fede = [x for x in xrange(40,81)]
for y in xrange(0,len(weights[0])):
	vector = [weightsLast[-1][y] for z in xrange(0,41)]
	for x in xrange(1,len(weights)+1):
		vector[x] = weights[x-1][y]
	ax.plot(fede, vector, linewidth=2)

ax.legend(loc=4)
ax.grid(grid)

############################################################################################
# WEIGHTS AND STD DEVIATION - LEARNING CURVES COMPARISON

# read the results from the file
with open("/home/fedepare/tetrisRL/results/biggerBoard_LEARNING_COMPLETE.dat", "rb") as f:
    BNoN1 = pickle.load(f)

with open("/home/fedepare/tetrisRL/results/biggerBoard_DecNoise_LEARNING_COMPLETE.dat", "rb") as f:
    resultsDecNoise = pickle.load(f)

with open("/home/fedepare/tetrisRL/results/biggerBoard_CnstNoise_LEARNING_COMPLETE.dat", "rb") as f:
    resultsCnstNoise = pickle.load(f)

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(10)
ax = fig.gca()
ax.set_xlabel('Iterations', fontsize=15)
ax.set_ylabel('Cleared lines', fontsize=15)

fede = [x for x in xrange(0,81)]
ax.plot(fede, BNoN1, linewidth=2, label="No Noise",linestyle="-")
ax.plot(fede, resultsDecNoise, linewidth=1, label="Dec Noise",linestyle="--")
ax.plot(fede, resultsCnstNoise, linewidth=1, label="Cnst Noise",linestyle="--")

#ax.set_yscale('log')
ax.set_ylim([10**0,600])
ax.legend(loc=4)
ax.grid(grid)

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(11)
ax = fig.gca()
ax.set_xlabel('Iterations', fontsize=15)
ax.set_ylabel('Cleared lines', fontsize=15)

fede = [x for x in xrange(0,81)]
ax.plot(fede, BNoN1, linewidth=1, label="No Noise",linestyle="--")
ax.plot(fede, resultsDecNoise, linewidth=2, label="Dec Noise",linestyle="-")
ax.plot(fede, resultsCnstNoise, linewidth=1, label="Cnst Noise",linestyle="--")

#ax.set_yscale('log')
ax.set_ylim([10**0,600])
ax.legend(loc=4)
ax.grid(grid)

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(12)
ax = fig.gca()
ax.set_xlabel('Iterations', fontsize=15)
ax.set_ylabel('Cleared lines', fontsize=15)

fede = [x for x in xrange(0,81)]
ax.plot(fede, BNoN1, linewidth=1, label="No Noise",linestyle="--")
ax.plot(fede, resultsDecNoise, linewidth=1, label="Dec Noise",linestyle="--")
ax.plot(fede, resultsCnstNoise, linewidth=2, label="Cnst Noise",linestyle="-")

#ax.set_yscale('log')
ax.set_ylim([10**0,600])
ax.legend(loc=4)
ax.grid(grid)

############################################################################################
# SENSITIVITY ANALYSIS - BOARD SIZE

# SIZE 8X20
with open("/home/fedepare/tetrisRL/results/NoNoise_8_LEARNING.dat", "rb") as f:
    performanceEight = pickle.load(f)

with open("/home/fedepare/tetrisRL/results/OriginalController_8_LEARNING.dat", "rb") as f:
    performanceOriginal = pickle.load(f)

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(13)
ax = fig.gca()
ax.set_xlabel('Iterations', fontsize=15)
ax.set_ylabel('Cleared lines', fontsize=15)

fede = [x for x in xrange(0,41)]
ax.plot(fede, performanceEight, linewidth=2, label="8x20 Controller",linestyle="-")
ax.plot(fede, performanceOriginal, linewidth=2, label="Original Controller",linestyle="-")

ax.legend(loc=4)
ax.grid(grid)

# SIZE 6X20
with open("/home/fedepare/tetrisRL/results/NoNoise_6_LEARNING.dat", "rb") as f:
    performanceEight = pickle.load(f)

with open("/home/fedepare/tetrisRL/results/OriginalController_6_LEARNING.dat", "rb") as f:
    performanceOriginal = pickle.load(f)

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(14)
ax = fig.gca()
ax.set_xlabel('Iterations', fontsize=15)
ax.set_ylabel('Cleared lines', fontsize=15)

fede = [x for x in xrange(0,41)]
ax.plot(fede, performanceEight, linewidth=2, label="6x20 Controller",linestyle="-")
ax.plot(fede, performanceOriginal, linewidth=2, label="Original Controller",linestyle="-")

ax.legend(loc=4)
ax.grid(grid)

############################################################################################
# SENSITIVITY ANALYSIS - FEATURES

with open("/home/fedepare/tetrisRL/results/NoNoise_8_LEARNING.dat", "rb") as f:
    performanceEight = pickle.load(f)

plt.show()