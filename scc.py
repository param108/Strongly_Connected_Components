import sys
import subprocess
from fsort import largefilesort
from cache import NodeCache,FoundCache
import os
from itertools import compress

# initialize globals
nodecache = None
foundcache = None

tmeasure=0
def timemeasure():
  global tmeasure
  tmeasure+=1
  return tmeasure

def iterDFS(n):
  q=[n]
  result = []
  while len(q):
    home = q[-1]
    if not foundcache.found(home):
      foundcache.setfound(home)
      nodecache.find(home)
      found_valid_branch = False
      for vb in compress(nodecache.degree,[ not foundcache.found(x) for x in nodecache.degree ]):
        q.append(vb)  
        found_valid_branch = True
      if not found_valid_branch:
        result.append(home)
        foundcache.setfound(home,2)
        print "%d %d"%(timemeasure(),home)
        q.pop()
    else:
      if foundcache.getfound(home) != 2:
        result.append(home)
        foundcache.setfound(home,2)
        print "%d %d"%(timemeasure(),home)
      q.pop()
  return result 
    
def DFS(n,measure,reverse=False):
  #print "Entering %d"%(n)
  foundcache.setfound(n)
  nodecache.find(n)
  lstlen = len(nodecache.degree)
  for i in xrange(lstlen):
    nextnode = nodecache.find(n,i)
    if not foundcache.found(nextnode):
      DFS(nextnode,measure,reverse)
  measure()
  #if tmeasure % 10000 == 0:
  print "%d %d %d"%(n,tmeasure,nodecache.maxnum) 

def initDFS(fname,reverse):
  global foundcache, nodecache, tmeasure
  # initialize the beginning of time
  tmeasure = 0
  nodefp = open(fname,"r")
  nodecache = NodeCache(nodefp,os.stat(fname).st_size,reverse, 10000, 9000)
  foundcache = FoundCache()

def runDFS(reversefile, forwardfile):
  global foundcache, nodecache
  initDFS(reversefile,1)
  nodecache.getMaxNodes()       
  maxnodes = nodecache.maxnum
  ret = []
  for i in xrange(1,maxnodes+1):
    if not foundcache.found(i):
      ret.extend(iterDFS(i))
  nodecache.fp.close()
  del(nodecache)
  del(foundcache)  
  initDFS(forwardfile,0)
  maxsizes=[]
  ret.reverse()
  for i in ret:
    if not foundcache.found(i):
      a = iterDFS(i)
      maxsizes.append(len(a))
    if len(maxsizes) > 5:
      maxsizes.sort(reverse=True)
      maxsizes=maxsizes[:5]
  print ",".join([ str(x) for x in maxsizes ])


# initialize maxnodes
# actual algorithm
largefilesort("SCC.txt",os.stat("SCC.txt").st_size,"reverse.txt",1)
largefilesort("SCC.txt",os.stat("SCC.txt").st_size,"forward.txt",0)
runDFS("reverse.txt", "forward.txt")
subprocess.check_call(["rm","reverse.txt","forward.txt"])
