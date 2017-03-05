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

pg  = pygame
pd  = pg.display 
cdc = copy.deepcopy

#########
# MAIN
#########

# game initialization
pg.init()
pd.set_mode((320,240),RESIZABLE)
sk=pd.get_surface()

# initialization of Q matrix
numPieces = 7
numBH     = 20
numBL     = 2
numSS     = 2
numMS     = 2
numH      = 4
numCombinations = (numPieces**2)*numBH*numBL*numSS*numMS*numH
[Q, Qcheck] = pickle.load( open( "objs.pickle", "r" ) )

# number of games to be playes
games    = 0
numGames = 1
score    = 0
lines    = 0

while games < numGames:

  # definition of variables
  t2   = 0
  nor  = 0
  pc   = [[[1,1],[1,1]],[[1,0],[1,0],[1,1]],[[0,1],[0,1],[1,1]],[[1],[1],[1],[1]],[[0,1,1],[1,1,0]],[[1,1,0],[0,1,1]],[[1,1,1],[0,1,0]]]
  cols = [(0,0,0),(100,100,100),(10,100,225),(0,150,220),(0,220,150),(60,200,10),(180,210,5),(210,180,10),(100,200,170)]

  # f is the current state of the board
  f=[[1]+[0 for x in range(8)]+[1] for x in range(19)]+[[1 for x in range(10)]]

  # game stuff
  of  = cdc(f)
  s   = 12
  brt = Rect((100,0,s,s))
  b   = -1      # figure index (different from f)
  b1  = random.randint(0,6) # figure index in the next timestep(different from f)
  b2  = random.randint(0,6)
  p   = []      # array indicating the orientation of the figure
  lc  = [-9,0]  # position of the leftmost and upmost point of the figure x = [1-8]; y = [0-18];
  t   = 0
  bt  = 60

  pg.key.set_repeat(200,100)
  rh  = 0
  cr  = []
  crs = pg.Surface((8*s,s))
  crs.fill((255,0,0))
  crs.set_alpha(100)
  gv  = -1
  z   = pg.font.Font("c.ttf",14)
  _=0

  it  = 0 # number of iterations

  # music
  # pg.mixer.music.load("t.ogg")
  # pg.mixer.music.play(-1)

  # the game
  while 1:

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
    b  = b1
    b1 = b2
    p  = pc[b];
    lc = [5-len(p)/2,0]
    b2 = random.randint(0,6)

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
      sk.fill([x*0.75 for x in cols[k]],brt.move(r*s,c*s))
      sk.fill(cols[k],brt.move(r*s,c*s).inflate(-4,-4))
      r+=1
     c+=1
   
   # cr only has values when a row is completed
   for r in cr:
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

   # game over
   if gv>=0:
    gs=z.render("GAME OVER",1,(255,255,255))
    gr=gs.get_rect()
    gr.center=(160,120)
    sk.blit(gs,gr)
    if gv==99:
      pd.flip()
      time.sleep(4)

    games += 1
    score += _
    print "Game: %s -> Score: %s, Lines: %s" % (games, score, lines)
    break
    
   ######################################################################################
   ######################################################################################
   if it == 1 and not cr:

     # feature-based state identification
     curFig, nxtFig, boardHeight, boardLevel, singleValley, \
     multipleValley, buriedHoles = features(b, b1, f)

     # create state index
     index = stateIndex(b, b1, boardHeight, boardLevel, \
      singleValley, multipleValley, buriedHoles)


     # high-level actions evaluation
     #     1. minimize buried holes
     #     2. maximize lines

     # choose the action with highest Q value
     maxQ       = -1e6
     maxQaction = -1
     equalQ     = 0
     
     for x in xrange(0,2):
       if Q[index][x] > maxQ:
         maxQ       = Q[index][x]
         maxQaction = x

       if x != 0 and Q[index][x] == maxQ:
        equalQ = 1
       else:
        equalQ = 0

     # in case Q is equal for all the action, choose randomly
     if equalQ == 1:
      maxQaction = random.randint(0,1)
     
     # execute the action selected
     actionCnt[maxQaction] += 1
     newboard = chooseAction(f, curFig, p, maxQaction+1)

     # reset the panel
     for h in xrange(0,len(f)):
       for w in xrange(0,len(f[0])):
         f[h][w] = newboard[h][w]
         if f[h][w] == 10:
           f[h][w] = b + 2

     b  = -20
     t  = 1
     rx = 0
     rh = 0
     p  = []
     it = 0
     time.sleep(2)

   ######################################################################################
   ######################################################################################

   if gv>=0:
    continue

   pd.flip() # update the contents of the entire display
   t+=1
   t2+=1
   time.sleep(0.01) # velocity of the game

   # update the number of iterations
   it += 1 

sys.exit(0)
