# Thaimas Andronaco, Clarence Dufault, Carlo Gabarda, Patrick Hwang, Cynthia Nguyen

# IMPORT LIBRARIES
import pygame
import random
from sys import exit

# DEFINE CONSTANTS
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
SCORE_OFFSET = 100
OFFSET = 320
BLOCK_SIZE = 20
SPEED = 10

# INITIALIZE PYGAME
pygame.init()

# MOVEMENT KEY
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4

# INITIALIZE FONTS
score_font = pygame.font.Font('resources/EXEPixelPerfect.ttf', 60)
title_font = pygame.font.Font('resources/EXEPixelPerfect.ttf', 80)
small_font = pygame.font.Font('resources/EXEPixelPerfect.ttf', 40)

class Snake:

  # INITIALIZE GAME
  def __init__(self):
    # Define window height, width, and block size
    self.w = WINDOW_WIDTH
    self.h = WINDOW_HEIGHT
    self.block_size = BLOCK_SIZE

    # Declare pygame display and clock
    self.display = pygame.display.set_mode((self.w, self.h))
    pygame.display.set_caption('Snake')
    self.clock = pygame.time.Clock()

    # Call reset function to start game in initial state
    self.reset()


  # START MENU FUNCTION
  def start_menu(self):
    while True:
      self.display.fill('black')

      # Title
      title_text = title_font.render("SNAKE", True, 'white')
      title_rect = title_text.get_rect(center=(self.w // 2, self.h // 2 - 100))
      self.display.blit(title_text, title_rect)

      # Instructions
      play_text = small_font.render("Press SPACE to Start", True, 'white')
      play_rect = play_text.get_rect(center=(self.w // 2, self.h // 2 + 50))
      self.display.blit(play_text, play_rect)

      pygame.display.update()

      # Event handling
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            return  # leave start menu and begin game

      self.clock.tick(SPEED)


  # GAME OVER MENU FUNCTION
  def game_over_menu(self):
    while True:
      self.display.fill('black')

      # GAME OVER text
      over_text = title_font.render("GAME OVER", True, 'red')
      over_rect = over_text.get_rect(center=(self.w // 2, self.h // 2 - 100))
      self.display.blit(over_text, over_rect)

      # Score
      score_text = small_font.render(f"Score: {self.score}", True, 'white')
      score_rect = score_text.get_rect(center=(self.w // 2, self.h // 2))
      self.display.blit(score_text, score_rect)

      # Restart instructions
      restart_text = small_font.render("Press SPACE to Play Again", True, 'white')
      restart_rect = restart_text.get_rect(center=(self.w // 2, self.h // 2 + 100))
      self.display.blit(restart_text, restart_rect)

      # Quit instructions
      quit_text = small_font.render("Press Q to Quit", True, 'white')
      quit_rect = quit_text.get_rect(center=(self.w // 2, self.h // 2 + 160))
      self.display.blit(quit_text, quit_rect)

      pygame.display.update()

      # Event handling
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            self.reset()
            return  # Exit menu and restart the game

          if event.key == pygame.K_q:
            pygame.quit()
            exit()

      self.clock.tick(SPEED)


  # RESET FUNCTION
  def reset(self):
    # Declare initial state (score, expand_level, offset, direction, snake head, snake body, food, placefood)
    self.score = 0
    self.score_goal = 10
    self.expand_level = 0
    self.offset = OFFSET
    self.direction = RIGHT
    self.next_direction = self.direction
    self.head = [self.w / 2, self.h / 2]
    self.snake = [self.head, [self.head[0] - self.block_size, self.head[1]], [self.head[0] - (self.block_size * 2), self.head[1]]]
    self.food = None
    self.placeFood()


  # MOVE FUNCTION
  def move(self, direction):
    # Store x and y coordinates of snake head
    x = self.head[0]
    y = self.head[1]

    # Update coordinates based on movement direction
    if direction == UP:
      y -= self.block_size
    elif direction == DOWN:
      y += self.block_size
    elif direction == RIGHT:
      x += self.block_size
    elif direction == LEFT:
      x -= self.block_size

    # Store new coordinates as the new snake head
    self.head = (x, y)

  
  # PLACE FOOD FUNCTION
  def placeFood(self):
    # Generate random x and y coordinates where food can spawn
    x = random.randrange(self.offset, (self.w - self.offset), self.block_size)
    y = random.randrange(SCORE_OFFSET + self.offset, (self.h - self.offset), self.block_size)

    # Store food coordinates, generate food coordinates again if food coordinates appear in snake coordinates
    self.food = (x, y)
    if self.food in self.snake:
      self.placeFood()


  # COLLISION DETECTION
  def collision(self):
    # Return true of head collides with body or bumps into the borders
    if (self.head in self.snake[1:]) or (self.head[1] < (self.offset + SCORE_OFFSET)) or (self.head[1] >= (self.h - self.offset)) or (self.head[0] >= (self.w - self.offset)) or (self.head[0] < self.offset):
      return True
    return False


  # EXPAND GRID FUNCTION
  def expand(self):
    # Declare counter and text appear boolean
    num_times = 0
    appear = True

    # Loop to flash text onto screen
    while True:
      if appear:
        self.display.fill('black')
        expand_text = title_font.render('GRID EXPANSION', True, 'White')
        text_rect = expand_text.get_rect(center=(self.h / 2, self.w / 2))
        self.display.blit(expand_text, text_rect)
        appear = False
        num_times += 1
      else:
        self.display.fill('black')
        appear = True

      # Update Display
      pygame.display.update()
      self.clock.tick(SPEED)

      # Break after the text appears 10 times, adjust the offset to make the grid bigger, then return
      if num_times == 10:
        self.offset -= 80
        return
        

  # UPDATE FUNCTION
  def update(self):
    # Fill current frame black
    self.display.fill('black')

    # Create a grid
    for x in range(self.offset, (self.w - self.offset), self.block_size):
      for y in range((SCORE_OFFSET + self.offset), (self.h - self.offset), self.block_size):
        grid_rect = pygame.Rect((x, y), (self.block_size, self.block_size))
        pygame.draw.rect(self.display, 'gray9', grid_rect, 1)

    # Display snake onto the current frame
    for pos in self.snake:
      snake_rect = pygame.Rect((pos[0], pos[1]), (self.block_size, self.block_size))
      pygame.draw.rect(self.display, 'Green', snake_rect)

    # Display food onto current frame
    food_rect = pygame.Rect((self.food[0], self.food[1]), (self.block_size, self.block_size))
    pygame.draw.rect(self.display, 'Red', food_rect)

    # Display player score
    score_text = score_font.render(f'Score: {str(self.score)}', True, 'White')
    self.display.blit(score_text, (25, 25))

    # Display score goal
    if self.expand_level != 4:
      goal_text = score_font.render(f'Next Goal: {str(self.score_goal)}', True, 'White')
      goal_rect = goal_text.get_rect(topright=(self.w - 25, 25))
      self.display.blit(goal_text, goal_rect)

    # Update display
    pygame.display.flip()


  # PLAY FUNCTION
  def play(self):
    # Player input events
    for event in pygame.event.get():
        # Quit game if user closes tab
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Movement key inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and self.direction != DOWN:
                self.next_direction = UP
            elif event.key == pygame.K_s and self.direction != UP:
                self.next_direction = DOWN
            elif event.key == pygame.K_a and self.direction != RIGHT:
                self.next_direction = LEFT
            elif event.key == pygame.K_d and self.direction != LEFT:
                self.next_direction = RIGHT


    # Snake movement implementation (insert new snake head into the front of the snake body array, pop the last element in the snake body array)
    self.direction = self.next_direction
    self.move(self.direction)
    self.snake.insert(0, self.head)

    # Eating mechanic, if head collides with food then we place another food, increase score, and don't pop the snake array (grow snake), else pop the snake array
    if self.head == self.food:
      self.placeFood()
      self.score += 1
    else:
      self.snake.pop()

    # End game if collision happens
    if self.collision():
      return True
    
    if (self.expand_level != 4) and (self.score == self.score_goal):
      if self.expand():
        return True
      self.expand_level += 1
      self.score_goal += 20

    # Update frame & declare frame rate
    self.update()
    self.clock.tick(SPEED)


# Main
if __name__ == '__main__':
  game = Snake()
  game.start_menu()
  while True:
    game_over = game.play()

    if game_over:
      game.game_over_menu()
