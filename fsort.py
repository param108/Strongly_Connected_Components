from multiprocessing import Pool
import os
import sys 

def mergesort(l,s,e,nidx):
  llen = e - s
  if llen == 1:
    return [l[s]]
  if llen == 2:
    if l[s][nidx] > l[s+1][nidx]:
      return [l[s+1],l[s]]
    return [l[s],l[s+1]]
  e1idx = 0
  e2idx = 0
  s1idx = 0
  s2idx = 0
  if llen%2 == 0:
    s1idx = s
    e1idx = s + llen/2 
    s2idx = e1idx
    e2idx = e1idx + llen/2
  else:
    s1idx = s
    e1idx = s + (llen+1)/2 
    s2idx = e1idx
    e2idx = s + llen
  left = mergesort(l,s1idx,e1idx,nidx)
  right = mergesort(l,s2idx,e2idx,nidx)
  j = 0 
  k = 0
  result = []
  for i in xrange(e - s):
    if k >= len(right) or (j < len(left) and left[j][nidx] <= right[k][nidx]):
      result.append(left[j])
      j+=1
      continue
    if j >= len(left) or (k < len(right) and left[j][nidx] >= right[k][nidx]):
      result.append(right[k])
      k+=1
      continue
  return result

def partsort(args):
  fname = args[0]
  offset = int(args[1])
  partlength = int(args[2])
  outname=args[3]
  nidx = int(args[4])
  #print "Starting %s"%(outname)

  inp = []
  with open(fname, "r") as fp:
    idx = 0
    if offset != 0:
      fp.seek(offset-1)
      # if the character before the start of the block
      # is a "\n" then dont ignore the line
      if fp.read(1) != "\n":
        idx+=len(fp.readline())
    else:
      fp.seek(0)

    # start the loop
    l = fp.readline()
    while len(l) > 0 and idx < partlength:
      idx += len(l)
      if l != "\n":
        a = [ int(x.strip()) for x in l.split(" ") if x != "\n" and len(x) != 0]
        inp.append((a[0],a[1]))
      l = fp.readline()
  # close the file now
  inp = mergesort(inp,0, len(inp), nidx)

  with open(outname,"w") as ofp:
    for l in inp:
      ofp.write("%d %d\n"%(l[0],l[1]))
  print "Done %s"%(outname)
  return True

def allended(lended):
  for e in lended:
    if not e:
      return False 
  return True
  
def nfilemerge(lfp,ofname,nidx):
  print "Entering merge with %d files"%(len(lfp))
  with open(ofname,"w") as ofp:
    topmost = [None]*len(lfp)
    ended =[False]*len(lfp)
    lineswritten = 0
    while not allended(ended):
      mini = -1
      minval = 1000000000
      for i,fp in enumerate(lfp):
        if not ended[i]:
          if topmost[i] == None:
            a = fp.readline()
            if len(a) == 0:
              ended[i] = True
              continue
            inp = [int(x.strip()) for x in a.split(" ")]
            topmost[i] = (inp[0],inp[1])
          if minval > topmost[i][nidx]:
            minval = topmost[i][nidx]
            mini = i
      if mini != -1:
        ofp.write("%d %d\n"%(topmost[mini][0],topmost[mini][1]))
        #lineswritten+=1
        #if lineswritten % 100000 == 0:
        #  print "%d %d\n"%(topmost[mini][0],topmost[mini][1])
        topmost[mini] = None

def largefilesort(fname,length,ofname,idx):
  p = Pool(20)
  DIV_FACTOR=1000000
  print p.map(partsort,[(fname,x,DIV_FACTOR,str(x)+".part",idx) for x in xrange(0,length,DIV_FACTOR)])
  nfilemerge([open(str(x)+".part") for x in xrange(0,length,DIV_FACTOR)],ofname,idx)
  print "Num Processes:%s"%(sys.argv[1])

#basic mergesort test
#inpeven = [(1,2),(3,5),(1,4),(3,7),(4,8),(1,9),(2,6)]
#inpodd = [(1,2),(3,5),(1,4),(3,7),(4,8),(1,9),(2,6),(6,5)]
#print inpeven
#print mergesort(inpeven, 0, len(inpeven))
#print inpodd
#print mergesort(inpodd, 0, len(inpodd))

#largefilesort("SCC.txt",os.stat("SCC.txt").st_size,"final.txt")
