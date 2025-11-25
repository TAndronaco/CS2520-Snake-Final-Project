class Snake:
  def __init__(self, headIndex=3, headDirection=0, body = [ [3,3], [4,3], [5,3], [6,3] ], gameState = True) #head d
    self.headIndex = headIndex
    self.headDirection = headDirection #0=right, 1=up, 2=left, 3=down
    self.body = body
    self.gameState = gameState #True = ongoing, False = lost

  def updateHead(self, eatFood = False):
    if(eatFood):
      self.body.append()
      for i in range(self.headIndex+1,len(self.body)):   #can be optimized
        self.body[i] = self.body[i-1]

    newHeadIndex = (self.headIndex+1) % len(body)
    self.body[newHeadIndex] = self.body[self.headIndex]
    match self.headDirection:    #using case-switch equivalent from https://docs.python.org/3.10/whatsnew/3.10.html#pep-634-structural-pattern-matching
      case 0:
        self.body[newHeadIndex][0] = self.body[newHeadIndex][0]+1
      case 1:
        self.body[newHeadIndex][1] = self.body[newHeadIndex][1]+1
      case 2:
        self.body[newHeadIndex][0] = self.body[newHeadIndex][0]-1
      case _:
        self.body[newHeadIndex][1] = self.body[newHeadIndex][1]-1

    self.headIndex = newHeadIndex
    self.checkCollision()
  
  def checkCollision(self, maxXVal, maxYVal):
    head = self.body[self.headIndex]
    if(head[0] > maxXVal or head[1] > maxYVal):
      for i in range(len(self.body)):
        if ( self.body[i] == head and i != self.headIndex ):
          self.gameState = False

      #checking spikes code can go here

