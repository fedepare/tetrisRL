#########
# IMPORTS
#########

import pygame
import time
import random
import sys
import copy 
import os
from pygame.locals import *
from RL import *
import pickle
import operator

pg  = pygame
pd  = pg.display 
cdc = copy.deepcopy

display = 0

#########
# MAIN
#########

# game initialization
if display:
  pg.init()
  pd.set_mode((320,240),RESIZABLE)
  sk=pd.get_surface()

# number of games to be played
games    = 0
numGames = 40

# variable initialization
blockLines  = 0
accumLines  = 0
performance = [0 for x in xrange(0, numGames)]

# initial normal distribution
n    = 100
nCnt = 0
rho  = 0.1

# tries for each weight vector
L     = 5
cntL  = 0

# number of features used to represent the state of the board
nFeat = 6

# initial normal distribution
muVec   = np.zeros((numGames, nFeat))
sigVec  = np.zeros((numGames, nFeat))
for x in xrange(0,len(sigVec)):
  for y in xrange(0,len(sigVec[0])):
    sigVec[x][y] = 10

# weight initialization
weights = np.zeros((n, nFeat))
for x in xrange(0,n):
  for y in xrange(0,nFeat):
    weights[x][y] = np.random.normal(muVec[games][y], sigVec[games][y], 1)

# vector use to select the best weight configurations
nScore = [0.0 for x in xrange(0, n)]

while games < numGames:

  # definition of variables
  lines = 0
  t2    = 0
  nor   = 0
  pc    = [[[1,1],[1,1]],[[1,0],[1,0],[1,1]],[[0,1],[0,1],[1,1]],[[1],[1],[1],[1]],[[0,1,1],[1,1,0]],[[1,1,0],[0,1,1]],[[1,1,1],[0,1,0]]]
  cols  = [(0,0,0),(100,100,100),(10,100,225),(0,150,220),(0,220,150),(60,200,10),(180,210,5),(210,180,10),(100,200,170)]

  # f is the current state of the board
  f=[[1]+[0 for x in range(10)]+[1] for x in range(19)]+[[1 for x in range(12)]]

  # game stuff
  of  = cdc(f)
  s   = 12
  brt = Rect((100,0,s,s))
  b   = -1      # figure index (different from f)

  p   = []      # array indicating the orientation of the figure
  lc  = [-9,0]  # position of the leftmost and upmost point of the figure x = [1-8]; y = [0-18];
  t   = 0
  bt  = 60

  # altitude at which the previous piece landed
  altitudeLast = 19

  # number of bricks eliminated from the last piece added
  bricksLastPiece = 0

  if display:
    pg.key.set_repeat(200,100)
    crs = pg.Surface((8*s,s))
    crs.fill((255,0,0))
    crs.set_alpha(100)
    z   = pg.font.Font("c.ttf",14)

  cr  = []
  rh  = 0
  gv  = -1
  _=0

  it  = 0 # number of iterations

  # music
  # pg.mixer.music.load("t.ogg")
  # pg.mixer.music.play(-1)

  # the game
  while 1:

   if display:
     sk.fill((0,0,0));
     _su=z.render("Score " + str(_),1,(255,255,255))
     _rect=_su.get_rect()
     _rect.bottomright=(310,230)
     sk.blit(_su,_rect)

   if gv>-1:
     b=10
     rh=0
     if not t%5:
      gv-=1;
      f[9-gv]=[1]*10
      f[10+gv]=[1]*10
      t=1
     if gv==0:gv=99

   if b<-1:
    b+=1
   
   # initialization of a new figure
   if b==-1:
    b  = random.randint(0,6)
    p  = pc[b];
    lc = [5-len(p)/2,0]

   # update the location of the figure
   if not t%bt or rh:
    op=[p[:],lc[:]]
    lc[1] +=1

   if b < 0:continue

   rx=0;
   c=0

   # collision detection
   for l in p:
    r=0
    for k in l:
     while c+lc[0]<1:
      lc[0]+=1
     while c+lc[0]>8:
      lc[0]-=1
     if f[r+lc[1]][c+lc[0]] and k:
      if lc[1]==0:
        gv=10
      rx=1
     r+=1
    c+=1

   # update the board with a fallen piece
   if rx and not nor:
    p,lc = op
    c=0
    for l in p:
     r=0
     for k in l:
      if k:
       f[r+lc[1]][c+lc[0]]=b+2
       it = 0
      r+=1
     c+=1
    b  = -20
    t  = 1
    rx = 0
    rh = 0
    p  = []
   nor = False

   if rh:continue

   for r in f[:-1]:
     if not r.count(0):
      wr=r
      cr+=[[f.index(wr),10]]
      f.remove(wr)
      f=[[1]+[0 for x in range(8)]+[1]]+f
      if gv==-1:
       _+=10;
       bt=max(8,bt-1)

   if gv>-1:
    f=cdc(of)

   c=0

   for l in f:
     r=0
     for k in l:
      try:
       if r>=lc[0] and c>=lc[1] and p[r-lc[0]][c-lc[1]]:
        k=b+2
      except:
        pass
      if display:
        sk.fill([x*0.75 for x in cols[k]],brt.move(r*s,c*s))
        sk.fill(cols[k],brt.move(r*s,c*s).inflate(-4,-4))
      r+=1
     c+=1
   
   # cr only has values when a row is completed
   for r in cr:
    if display:
      crs.set_alpha(r[1])
      sk.blit(crs,(100+s,r[0]*s))
    cp=cr.index(r)
    cr[cp][-1]-=5
    if cr[cp][-1]<=0:
      cr.remove(cr[cp])
      it = 1

   if len(cr):
     aux = cr[0]
     if aux[1] == 5:
      lines += 1
      blockLines += 1

   ######################################################################################
   ######################################################################################

   # game over
   if gv>=0:

    if display:
      gs=z.render("GAME OVER",1,(255,255,255))
      gr=gs.get_rect()
      gr.center=(160,120)
      sk.blit(gs,gr)

    if gv==99:
      if display:
        pd.flip()

    # update cntL
    cntL += 1

    # accumulate the lines for the computation of the average
    accumLines += lines

    # weight configuration tested
    if cntL == L:
      print "Game: [%s, %s] -> Lines: %s" % (games, nCnt, float(accumLines) / L)

      # update the performance vector and the counter
      nScore[nCnt] = float(accumLines) / L
      nCnt += 1

      # reset counters
      cntL       = 0
      accumLines = 0

      # all weight configurations tested
      if nCnt == n:

        # update counters
        nCnt   = 0

        # select the best configurations
        idxBest = [0 for x in xrange(0,int(rho*n))]
        accum   = 0
        for x in xrange(0,int(rho*n)):
          index, value = max(enumerate(nScore), key=operator.itemgetter(1))
          accum += value
          idxBest[x] = index
          nScore[index] = -1

        # get the average number of lines for the best configurations
        performance[games] = float(accum) / (rho*n)
        print "Performance:"
        print performance

        # update average and standard deviation
        for x in xrange(0,nFeat):
          accum = 0
          for y in xrange(1,len(idxBest)):
            accum += weights[idxBest[y]][x]
          muVec[games][x] = accum / len(idxBest)

        for x in xrange(0,nFeat):
          accum = 0
          for y in xrange(1,len(idxBest)):
            accum += (weights[idxBest[y]][x] - muVec[games][x])**2
          sigVec[games][x] = np.sqrt(accum / len(idxBest))

        # obtain a new set of weights
        weights = np.zeros((n, nFeat))
        for x in xrange(0,n):
          for y in xrange(0,nFeat):
            weights[x][y] = np.random.normal(muVec[games][y], sigVec[games][y], 1)

        # reset the score matrix
        nScore = [0.0 for x in xrange(0, n)]

        # update counters
        games += 1

    break
    
   if it == 1 and not cr:

     # choose the pose of the new block
     newboard, figLoc, bricksLastPiece = getNewBoard(f, b, p, blockLines, bricksLastPiece, altitudeLast, weights, nCnt)

     # reset the panel
     for h in xrange(0,len(f)):
       for w in xrange(0,len(f[0])):
         f[h][w] = newboard[h][w]
         if f[h][w] == 14:
           f[h][w] = b + 2

     b  = -20
     t  = 1
     rx = 0
     rh = 0
     p  = []
     it = 0
     altitudeLast = figLoc[1]
     blockLines   = 0

     time.sleep(0)

   ######################################################################################
   ######################################################################################

   if gv>=0:
    continue
   if display:
      pd.flip() # update the contents of the entire display
   t+=1
   t2+=1

   # update the number of iterations
   it += 1

with open("pickle.dat", "wb") as f:
    pickle.dump([muVec, sigVec], f)

if display:
  sys.exit(0)