import math
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl

# read the results from the file
with open("/home/fedepare/tetrisRL/results/Bertsekas_NoNoise_LEARNING_1.dat", "rb") as f:
    BNoN1 = pickle.load(f)
with open("/home/fedepare/tetrisRL/results/Bertsekas_CnstNoise_LEARNING_1.dat", "rb") as f:
    BCnstN1 = pickle.load(f)
with open("/home/fedepare/tetrisRL/results/Bertsekas_DecNoise_LEARNING_1.dat", "rb") as f:
    BDecN1 = pickle.load(f)

# initialize figure
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(1)
ax = fig.gca()
ax.set_xlabel('iterations', fontsize=15)
ax.set_ylabel('Cleared lines', fontsize=15)

fede = [x for x in xrange(0,40)]
ax.plot(fede, BNoN1, linewidth=1, color='k', label="No Noise")
ax.plot(fede, BCnstN1, linewidth=1, color='k', linestyle='--', label="Constant Noise")
ax.plot(fede, BDecN1, linewidth=1, color='k', linestyle='-.', label="Decreasing Noise")
print BDecN1
ax.set_yscale('log')
ax.legend(loc=4)

plt.show()