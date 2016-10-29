
class FoundCache:
  def __init__(self):
    self.cache = {}

  def setfound(self,n,v=1):
    if self.cache.has_key(n):
      if v > self.cache[n]:
        self.cache[n] = v
    else:
      self.cache[n] = v

  def found(self,n):
    if self.cache.has_key(n):
      return True
    else:
      return False

  def getfound(self,n):
    return self.cache[n]

class NodeCache:
  def __init__(self,fp,size,reverse, cachesize, threshold):
    self.nidx = reverse
    self.size = size
    self.fp = fp
    self.cachesize = cachesize
    self.threshold = threshold
    self.findcache = {}
    self.findage = 0

  def getMaxNodes(self):
    check={}
    numNodes = 0
    self.fp.seek(0)
    l = self.fp.readline()
    while(len(l)):
      if l != "\n":
        data = [ int(x.strip()) for x in l.split(" ") if len(x.strip()) != 0 ]
        if data[0] not in check:
          check[data[0]] = 1
          numNodes+=1
        if data[1] not in check:
          check[data[1]] = 1
          numNodes+=1
      l = self.fp.readline()
    self.maxnum = numNodes
    print "Maxnodes %d"%(self.maxnum)
          
  def getIdxAtOffset(self,offset):
    self.fp.seek(offset)
    a = self.fp.readline()
    while len(a) == 0:
      offset -= 50
      if offset < 0:
        offset = 0
        break
      self.fp.seek(offset)
      a = self.fp.readline()
    self.fp.seek(offset)
    if offset != 0:
      # ignore the first line
      self.fp.readline()

    data = [ int(x.strip()) for x in self.fp.readline().split(" ") if len(x.strip()) != 0 ]
    if len(data) == 0:
      return -1
    #print "%d %d %d"%(offset,len(data),self.size)
    return data[self.nidx]

  def binsearch(self,idx,start,end):
    fidx = -1
    median = -1
    while fidx != idx:
      if end - start == 1:
        return -1 
      median = (start + end)/2 
      fidx = self.getIdxAtOffset(median)

      if fidx == -1:
        return -1

      if fidx > idx:
        end = median
      elif fidx < idx:
        start = median 
    return median
 
  def getIdxData(self, median, idx, which):
    fidx = self.getIdxAtOffset(median)
    while fidx == idx:
      median -= 50
      if median < 0:
        median = 0
        break
      fidx = self.getIdxAtOffset(median)

    self.fp.seek(median)
    if median != 0:
      self.fp.readline()

    self.degree = []
    self.empty = True
    while fidx <= idx:
      data = [ int(x.strip()) for x in self.fp.readline().split(" ") if len(x.strip()) != 0 ]
      if len(data) == 0:
        break
      fidx = data[self.nidx]
      if fidx == idx:
        self.empty = False 
        if self.nidx == 0:
          self.degree.append(data[1])
        else:
          self.degree.append(data[0])
    self.findage+=1
    self.findcache[idx]={"age":self.findage,"degree":self.degree}
    if len(self.findcache) > self.cachesize:
      dlist = []
      for k in self.findcache:
        if self.findcache[k]["age"] < self.findage - self.threshold: 
          dlist.append(k)
      for k in dlist:
        del(self.findcache[k])
    if which < 0:
      return None
    else:
      return self.degree[which]

  def find(self,idx,which=-1):
    if idx in self.findcache:
      self.degree = self.findcache[idx]["degree"]
      self.findage += 1
      self.findcache[idx]["age"] = self.findage
      if which < 0:
        return None
      else:
        return self.degree[which]
    median = self.binsearch(idx,0,self.size) 
    if median < 0:
      self.empty = True
      self.degree = []
      return None
    else:
      return self.getIdxData(median, idx, which)
