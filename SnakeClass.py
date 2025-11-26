# IMPORT LIBRARIES
import pygame
import random
from sys import exit

# DEFINE CONSTANTS
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
BLOCK_SIZE = 20
SPEED = 10

# INITIALIZE PYGAME
pygame.init()

class Snake:

  # INITIALIZE GAME
  def __init__(self):
    # Define window height and width
    self.w = WINDOW_WIDTH
    self.h = WINDOW_HEIGHT

    # Declare pygame display and clock
    self.display = pygame.display.set_mode((self.w, self.h))
    pygame.display.set_caption('Snake')
    self.clock = pygame.time.Clock()

    # Call reset function to start game
    self.reset()


  # RESET FUNCTION
  def reset(self):
    self.head = [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]
    self.snake = [self.head, [self.head[0] - BLOCK_SIZE, self.head[1]], [self.head[0] - (BLOCK_SIZE * 2), self.head[1]]]
    
  # PLAY FUNCTION
  def play(self):
    for event in pygame.event.get():
      # Quit Event
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    self.update()

  def update(self):
    # Fill current frame black
    self.display.fill('black')

    # Display snake onto the current frame
    for pos in self.snake:
      snake_rect = pygame.Rect((pos[0], pos[1]), (BLOCK_SIZE, BLOCK_SIZE))
      pygame.draw.rect(self.display, 'Green', snake_rect)

    # Update display
    pygame.display.flip()

    

  # def updateHead(self, eatFood = False):
  #   if(eatFood):
  #     self.body.append()
  #     for i in range(self.headIndex+1,len(self.body)):   #can be optimized
  #       body[i] = body[i-1]

  #   newHeadIndex = (self.headIndex+1) % len(body)
  #   self.body[newHeadIndex] = self.body[self.headIndex]
  #   match headDirection:    #using case-switch equivalent from https://docs.python.org/3.10/whatsnew/3.10.html#pep-634-structural-pattern-matching
  #     case 0:
  #       self.body[newHeaderIndex][0] = self.body[newHeaderIndex][0]+1
  #     case 1:
  #       self.body[newHeaderIndex][1] = self.body[newHeaderIndex][1]+1
  #     case 2:
  #       self.body[newHeaderIndex][0] = self.body[newHeaderIndex][0]-1
  #     case _:
  #       self.body[newHeaderIndex][1] = self.body[newHeaderIndex][1]-1

  #   self.headIndex = newHeaderIndex
  #   self.checkCollision()
  
  # def checkCollision(self, maxXVal, maxYVal):
  #   head = self.body[self.headIndex]
  #   if(head[0] > maxXVal or head[1] > maxYVal):
  #     for i in range(len(self.body)):
  #       if ( self.body[i] == head and i != self.headIndex ):
  #         self.gameState = False

  #     #checking spikes code can go here

if __name__ == '__main__':
  game = Snake()
  while True:
    game_over = game.play()

    if game_over:
      break
  
  pygame.quit()
  exit()