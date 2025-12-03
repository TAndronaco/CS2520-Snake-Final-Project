# Thaimas Andronaco, Clarence Dufault, Carlo Gabarda, Patrick Hwang, Cynthia Nguyen

# IMPORT LIBRARIES
import pygame
import random
from sys import exit

# DEFINE CONSTANTS
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
HEIGHT_OFFSET = 100
BLOCK_SIZE = 20 # Possible method to increase map size (decreasing block size)
SPEED = 10
SPIKE_DELAY = 10000

# INITIALIZE PYGAME
pygame.init()

# MOVEMENT KEY
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4

# INITIALIZE FONT
font = pygame.font.Font('resources/EXEPixelPerfect.ttf', 60)

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

    # Call reset function to start game in initial state
    self.reset()


  # MOVE FUNCTION
  def move(self, direction):
    # Store x and y coordinates of snake head
    x = self.head[0]
    y = self.head[1]

    # Update coordinates based on movement direction
    if direction == UP:
      y -= BLOCK_SIZE
    elif direction == DOWN:
      y += BLOCK_SIZE
    elif direction == RIGHT:
      x += BLOCK_SIZE
    elif direction == LEFT:
      x -= BLOCK_SIZE

    # Store new coordinates as the new snake head
    self.head = (x, y)

  
  # PLACE FOOD FUNCTION
  def placeFood(self):
    # Generate random x and y coordinates where food can spawn
    x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
    y = random.randrange(HEIGHT_OFFSET, WINDOW_HEIGHT, BLOCK_SIZE)

    # Store food coordinates, generate food coordinates again if food coordinates appear in snake coordinates
    self.food = (x, y)
    if (self.food in self.snake) or (self.food in self.spikes):
      self.placeFood()

  #PLACE SPIKE FUNCTION
  def placeSpike(self):
    # Generate random x and y coordinates where spike can spawn
    x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
    y = random.randrange(HEIGHT_OFFSET, WINDOW_HEIGHT, BLOCK_SIZE)

    #stores new spike cordinate unless it is inside the snake, where food already is, or is close to the snake head (within 2 squares)
    self.spikes.append((x,y))
    if (self.spikes[-1] in self.snake) or (self.spikes[-1] == self.food) or ((self.spikes[-1][0] < self.head[0]+3) and (self.spikes[-1][0] > self.head[0]-3)) or ((self.spikes[-1][1] < self.head[1]+3) and (self.spikes[-1][1] > self.head[1]-3)):
      self.spikes.pop()
      self.placeSpike()


  # COLLISION DETECTION
  def collision(self):
    # Return true of head collides with body, bumps into the borders, or collides with a spike
    if (self.head in self.snake[1:]) or (self.head[1] < HEIGHT_OFFSET) or (self.head[1] >= WINDOW_HEIGHT) or (self.head[0] >= WINDOW_WIDTH) or (self.head[0] < 0) or (self.head in self.spikes):
      return True
    return False


  # RESET FUNCTION
  def reset(self):
    # Declare initial state (score, direction, snake head, snake body, food, placefood)
    self.score = 0
    self.direction = 1
    self.head = [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]
    self.snake = [self.head, [self.head[0] - BLOCK_SIZE, self.head[1]], [self.head[0] - (BLOCK_SIZE * 2), self.head[1]]]
    self.food = None
    self.spikes = []
    self.time = 0
    self.placeFood()


  # UPDATE FUNCTION
  def update(self):
    # Fill current frame black
    self.display.fill('black')

    # Create a grid
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
      for y in range(HEIGHT_OFFSET, WINDOW_HEIGHT, BLOCK_SIZE):
        grid_rect = pygame.Rect((x, y), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, 'gray9', grid_rect, 1)

    # Display snake onto the current frame
    for pos in self.snake:
      snake_rect = pygame.Rect((pos[0], pos[1]), (BLOCK_SIZE, BLOCK_SIZE))
      pygame.draw.rect(self.display, 'Green', snake_rect)

    # Display food onto current frame
    food_rect = pygame.Rect((self.food[0], self.food[1]), (BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(self.display, 'Red', food_rect)

    #Display spikes onto current frame
    for spikePos in self.spikes:
      spike_rect = pygame.Rect((spikePos[0], spikePos[1]), (BLOCK_SIZE, BLOCK_SIZE))
      pygame.draw.rect(self.display, 'White', spike_rect )

    # Display player score
    score_text = font.render('Score: ' + str(self.score), True, 'White')
    self.display.blit(score_text, (25, 25))

    # Update display
    pygame.display.flip()


  # PLAY FUNCTION
  def play(self):

    for event in pygame.event.get():
      # Quit Event
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()

      # Player input events
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w and self.direction != DOWN:
          self.direction = UP
        elif event.key == pygame.K_s and self.direction != UP:
          self.direction = DOWN
        elif event.key == pygame.K_a and self.direction != RIGHT:
          self.direction = LEFT
        elif event.key == pygame.K_d and self.direction != LEFT:
          self.direction = RIGHT

    # Snake movement implementation (insert new snake head into the front of the snake body array, pop the last element in the snake body array)
    self.move(self.direction)
    self.snake.insert(0, self.head)

    # Eating mechanic, if head collides with food then we place another food, increase score, and don't pop the snake array (grow snake), else pop the snake array
    if self.head == self.food:
      self.placeFood()
      self.score += 1
    else:
      self.snake.pop()

    # Spike generation as an additional obstacle within the game instead of just the snake itself and the walls. will be called every 10 seconds
    self.time += self.clock.get_time()
    if(self.time > SPIKE_DELAY):
      self.time -= SPIKE_DELAY
      self.placeSpike()

    # End game if collision happens
    if self.collision():
      return True

    # Update frame & declare frame rate
    self.update()
    self.clock.tick(SPEED)
    

if __name__ == '__main__':
  game = Snake()
  while True:
    game_over = game.play()

    if game_over:
      break
  
  pygame.quit()
  exit()