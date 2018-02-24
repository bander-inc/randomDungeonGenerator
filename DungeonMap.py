from random import randint, shuffle

class DungeonMap:
  
  def __init__(self):
    self.data = {}
    self.origins = []
    self.rows = 25
    self.cols = 45
    self.buildMap()
    
    return
    
  def buildMap(self):
    print ("Building map with %s rows and %s cols...\n" % (self.rows, self.cols))
    
    # initialize to 0s
    for y in range(0, self.rows):
      for x in range(0, self.cols):
        self.data[(y,x)] = 0
    
    return
    
  def printMap(self):
    for y in range(0, self.rows):
      for x in range(0, self.cols):
        if self.data[(y,x)] != 0:
          print ("*", end='')
        else:
          print (" ", end='')
      print ("\n", end='')
    return
  
  def getRandomPoint(self, size_x, size_y):
    base_x = randint(1, self.cols-size_x)
    base_y = randint(1, self.rows-size_y)
    
    t= (base_y,base_x)
    return t;
  
  def carveRoom(self):
    size_x = randint(1,3)
    size_y = randint(1,3)
    #base_x = randint(1, self.cols-size_x)
    #base_y = randint(1, self.rows-size_y)
    
    #t= (base_y,base_x)
    t = self.getRandomPoint(size_x=size_x, size_y=size_y)
    # check for colision on existing open spot
    #print (t)
    while self.data[t] == 1:
     # print ("colision!")
      t = self.getRandomPoint(size_x=size_x, size_y=size_y)
      
    
    base_x = t[1]
    base_y = t[0]
    for y in range(base_y-size_y, base_y+size_y+1):
      for x in range(base_x-size_x, base_x+size_x+1):
        #print (y,x)
        self.data[(y,x)] = 1
    
    # carve hallway back to previous origin
    if self.origins:
      # get last object in the origins list
      d = self.origins[-1]
      self.carveBetweenPoints(source=t, dest=d)  
    # keep track of room origins
    self.origins.append(t)
    

    return
    
    
  def carveBetweenPoints(self, source, dest):
    #print (str(source) + " -> " + str(dest))
    
    _r = randint(1,2)
    
    if _r == 1:
      self.carveHorizontal(source, dest)
      self.carveVertical(source, dest)
    else:
      self.carveVertical(source, dest)
      self.carveHorizontal(source, dest)
    
      
    return
    
  def carveHorizontal(self, source, dest):
    
    if source[1] < dest[1]:
      for x in range(source[1], dest[1]+1):
        self.data[(source[0],x)] = 1
    else:
      for x in range(dest[1], source[1]+1):
        self.data[(source[0],x)] = 1
    
    return
  
  def carveVertical(self, source, dest):
    
    if source[0] < dest[0]:
      for y in range(source[0], dest[0]+1):
        self.data[(y,dest[1])] = 1
    else:
      for y in range(dest[0], source[0]+1):
        self.data[(y,dest[1])] = 1
    
    return
    
  def carveHallway(self):
    shuffle(self.origins)
    #print (self.origins)
    for t in range(0, len(self.origins)-1, 2):
      t_from = self.origins[t]
      t_to = self.origins[t+1]
      #print (t_from, t_to)
      
      self.carveBetweenPoints(source=t_from, dest=t_to)
      
      #if t_from[1] < t_to[1]:
      #  for x in range(t_from[1], t_to[1]):
      #    self.data[(t_from[0],x)] = 'x'
      #else:
      #  for x in range(t_to[1], t_from[1]):
      #    self.data[(t_to[0],x)] = 'x'
        
      #for y in range(t_from[0], t_to[0]):
      #  self.data[(y,t_to[1])] = 'y'
        
    return
    
  def carveRooms(self):
    for x in range(0,9):
      self.carveRoom()
      self.printMap()
    return
  
  def getCellValue(self, y, x):
    try:
      rtn_value = self.data[(y,x)]
    except KeyError:
      rtn_value = 0
    return rtn_value
    
  
  def cellularAuto(self):
    #print (self.rows, " | ", self.cols)
    for y in range(0, self.rows):
      for x in range(0, self.cols):
        #print ((y,x))
        _sub_value = 0
        for _sub_y in range (y-1,y+2):
          for _sub_x in range(x-1,x+2):
            _sub_value = _sub_value + self.getCellValue(y=_sub_y,x=_sub_x)
        
          if self.data[(y,x)] == 1:
            if _sub_value == 9:
              _r = randint(0,100)
              if _r < 10:
                self.data[(y,x)] = 0
          elif _sub_value == 3:
            _r = randint(0,100)
            if _r < 10:
              self.data[(y,x)] = 1
        
    return
  
dmap = DungeonMap()
#dmap.buildMap()
dmap.carveRooms()
dmap.printMap()
print ("AFTER")
dmap.carveHallway()
dmap.printMap()

print ("cell magic")
dmap.cellularAuto()
dmap.printMap()

  
