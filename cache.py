
class FoundCache:
  def __init__():
    self.cache = {}

  def setfound(n,v=1):
    self.cache[n]=v
  
  def found(n):
    if self.cache.has_key(n):
      return True
    else
      return False

  def getfound(n):
    return self.cache[n]

class NodeCache:
  def __init__(fp,size,reverse, cachesize, threshold):
    self.nidx = reverse
    self.size = size
    self.fp = fp
    self.cachesize = cachesize
    self.threshold = threshold

  def getIdxAtOffset(offset):
    self.fp.seek(offset)
    a = self.fp.readline()
    while len(a) == 0:
      offset -= 50
      if (offset < 0):
        offset = 0

    if offset != 0:
      # ignore the first line
      self.fp.readline()

    data = [ int(x.strip()) for x in self.fp.readline().split(" ") if len(x.strip()) == 0 ]
    return data[self.nidx]

  def find(idx,which=-1):
    if idx in self.findcache:
      self.degree = self.findcache[idx]["degree"]
      self.findage += 1
      self.findcache[idx]["age"] = self.findage
      if which < 0:
        return None
      else:
        return self.degree[which]
      return
    start = 0
    end = self.size
    fidx = -1
    median = -1
    while fidx != idx:
      median = (start + end)/2 
      fidx = self.getIdxAtOffset(median)

      if fidx > idx:
        end = median
      elif fidx < idx:
        start = median 

    while fidx == idx:
      median -= 50
      fidx = self.getIdxAtOffset(median)
      if median < 0:
        median = 0
        break

    self.fp.seek(median)
    if median != 0:
      self.fp.seek.readline()

    self.degree = []
    self.empty = True
    while fidx <= idx:
      data = [ int(x.strip()) for x in self.fp.readline().split(" ") if len(x.strip()) == 0 ]
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
