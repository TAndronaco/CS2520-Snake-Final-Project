# Thaimas Andronaco, Clarence Dufault, Carlo Gabarda, Patrick Hwang, Cynthia Nguyen

# IMPORT LIBRARIES
import pygame
import random
from sys import exit
from scores import save_score, get_top_scores

# DEFINE CONSTANTS
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
SCORE_OFFSET = 100
OFFSET = 320
BLOCK_SIZE = 20

# SPEED SYSTEM
BASE_SPEED = 10
MAX_SPEED = 25

# SPIKE SYSTEM
MAX_SPIKE_DELAY = 8000
MIN_SPIKE_DELAY = 3000
INITIAL_SPIKE_THRESHOLD = 3

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


# ------------------------
# REVIVAL SYSTEM
# ------------------------
revive_base = 50
revive_step = 10
revive_chance = revive_base

def reset_revive():
    global revive_chance
    revive_chance = revive_base

def try_revive():
    global revive_chance
    roll = random.randint(1, 100)
    chance_now = revive_chance
    print(f"Revive chance: {chance_now}% | Roll: {roll}")

    if roll <= chance_now:
        revive_chance = max(0, revive_chance - revive_step)
        return True, chance_now
    return False, chance_now


# ------------------------
# SNAKE GAME CLASS
# ------------------------
class Snake:

    def __init__(self):
        self.w = WINDOW_WIDTH
        self.h = WINDOW_HEIGHT
        self.block_size = BLOCK_SIZE

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        self.reset()

    # -------------
    # START MENU
    # -------------
    def start_menu(self):
        menu_options = ["Play", "High Scores", "Exit"]
        selected = 0

        while True:
            self.display.fill("black")

            title_text = title_font.render("SNAKE", True, "white")
            title_rect = title_text.get_rect(center=(self.w // 2, self.h // 2 - 200))
            self.display.blit(title_text, title_rect)

            for i, option in enumerate(menu_options):
                color = "yellow" if i == selected else "white"
                text = small_font.render(option, True, color)
                rect = text.get_rect(center=(self.w // 2, self.h // 2 + i * 60))
                self.display.blit(text, rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        selected = (selected - 1) % len(menu_options)
                    elif event.key == pygame.K_s:
                        selected = (selected + 1) % len(menu_options)
                    elif event.key == pygame.K_SPACE:
                        if menu_options[selected] == "Play":
                            return
                        elif menu_options[selected] == "High Scores":
                            self.high_scores_menu()
                        elif menu_options[selected] == "Exit":
                            pygame.quit()
                            exit()

            self.clock.tick(BASE_SPEED)

    # ------------------
    # HIGH SCORES MENU
    # ------------------
    def high_scores_menu(self):
        top_scores = get_top_scores(0)

        while True:
            self.display.fill("black")

            hs_title = title_font.render("HIGH SCORES", True, "white")
            hs_rect = hs_title.get_rect(center=(self.w // 2, 150))
            self.display.blit(hs_title, hs_rect)

            for i, s in enumerate(top_scores):
                text = small_font.render(f"{i+1}. {s}", True, "white")
                rect = text.get_rect(center=(self.w // 2, 250 + i * 50))
                self.display.blit(text, rect)

            back_text = small_font.render("Press Q to Return to Main Menu", True, "yellow")
            back_rect = back_text.get_rect(center=(self.w // 2, self.h - 150))
            self.display.blit(back_text, back_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    return

            self.clock.tick(BASE_SPEED)


    # ------------------------
    # GAME OVER MENU
    # ------------------------
    def game_over_menu(self):
        save_score(self.score)
        top_score = get_top_scores(self.score)

        while True:
            self.display.fill('black')

            over_text = title_font.render("GAME OVER", True, 'red')
            over_rect = over_text.get_rect(center=(self.w // 2, self.h // 2 - 150))
            self.display.blit(over_text, over_rect)

            score_text = small_font.render(f"Score: {self.score}", True, 'white')
            score_rect = score_text.get_rect(center=(self.w // 2, self.h // 2 - 80))
            self.display.blit(score_text, score_rect)

            hs_title = small_font.render("High Scores:", True, 'white')
            hs_rect = hs_title.get_rect(center=(self.w // 2, self.h // 2))
            self.display.blit(hs_title, hs_rect)

            for i, s in enumerate(top_score):
                text = small_font.render(f"{i+1}. {s}", True, 'white')
                rect = text.get_rect(center=(self.w // 2, self.h // 2 + 40 + i * 40))
                self.display.blit(text, rect)

            restart_text = small_font.render("Press SPACE to Play Again", True, 'white')
            restart_rect = restart_text.get_rect(center=(self.w // 2, self.h // 2 + 40 + len(top_score)*40 + 40))
            self.display.blit(restart_text, restart_rect)

            menu_text = small_font.render("Press Q to Return to Main Menu", True, 'white')
            menu_rect = menu_text.get_rect(center=(self.w // 2, self.h // 2 + 40 + len(top_score)*40 + 100))
            self.display.blit(menu_text, menu_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "restart"
                    if event.key == pygame.K_q:
                        return "menu"

            self.clock.tick(BASE_SPEED)



    # ------------------------
    # RESET GAME STATE
    # ------------------------
    def reset(self):
        self.score = 0
        self.score_goal = 10
        self.expand_level = 0
        self.offset = OFFSET

        self.direction = RIGHT
        self.next_direction = RIGHT

        self.head = (self.w // 2, self.h // 2)
        self.snake = [
            self.head,
            (self.head[0] - BLOCK_SIZE, self.head[1]),
            (self.head[0] - BLOCK_SIZE*2, self.head[1])
        ]

        self.food = None
        self.spikes = []

        # Spike difficulty settings
        self.spikeTimer = MAX_SPIKE_DELAY
        self.spikeThreshold = INITIAL_SPIKE_THRESHOLD
        self.time = 0

        # Speed system
        self.speed = BASE_SPEED
        self.speed_level = 0

        # Expansion rules
        self.just_wrapped = False
        self.pending_expand = False

        self.placeFood()


    # ------------------------
    # MOVE WITH WRAPPING
    # ------------------------
    def move(self, direction):
        x, y = self.head
        self.just_wrapped = False

        if direction == UP:
            y -= BLOCK_SIZE
        elif direction == DOWN:
            y += BLOCK_SIZE
        elif direction == RIGHT:
            x += BLOCK_SIZE
        elif direction == LEFT:
            x -= BLOCK_SIZE

        wrapped = False

        if x < self.offset:
            x = self.w - self.offset - BLOCK_SIZE
            wrapped = True
        elif x >= self.w - self.offset:
            x = self.offset
            wrapped = True

        if y < self.offset + SCORE_OFFSET:
            y = self.h - self.offset - BLOCK_SIZE
            wrapped = True
        elif y >= self.h - self.offset:
            y = self.offset + SCORE_OFFSET
            wrapped = True

        self.head = (x, y)
        self.just_wrapped = wrapped


    # ------------------------
    # SAFE-TO-EXPAND CHECK
    # ------------------------
    def safe_to_expand(self):
        if self.just_wrapped:
            return False

        for x, y in self.snake:
            if x <= self.offset or x >= (self.w - self.offset - BLOCK_SIZE):
                return False
            if y <= (self.offset + SCORE_OFFSET) or y >= (self.h - self.offset - BLOCK_SIZE):
                return False

        return True


    # ------------------------
    # FOOD AND SPIKE PLACEMENT
    # ------------------------
    def placeFood(self):
        x = random.randrange(self.offset, self.w - self.offset, BLOCK_SIZE)
        y = random.randrange(self.offset + SCORE_OFFSET, self.h - self.offset, BLOCK_SIZE)

        self.food = (x, y)
        if self.food in self.snake or self.food in self.spikes:
            self.placeFood()

    def placeSpike(self):
        x = random.randrange(self.offset, self.w - self.offset, BLOCK_SIZE)
        y = random.randrange(self.offset + SCORE_OFFSET, self.h - self.offset, BLOCK_SIZE)

        pos = (x, y)
        if pos in self.snake or pos == self.food:
            return self.placeSpike()

        # Keep spikes away from head
        if abs(pos[0] - self.head[0]) < 60 and abs(pos[1] - self.head[1]) < 60:
            return self.placeSpike()

        self.spikes.append(pos)


    # ------------------------
    # COLLISION CHECK
    # ------------------------
    def collision(self):
        return (self.head in self.snake[1:] or self.head in self.spikes)


    # ------------------------
    # EXPAND GRID EFFECT
    # ------------------------
    def expand(self):
        num_times = 0
        flash = True

        while num_times < 10:
            self.display.fill("black")
            if flash:
                txt = title_font.render("GRID EXPANSION", True, "white")
                rect = txt.get_rect(center=(self.w//2, self.h//2))
                self.display.blit(txt, rect)
                num_times += 1
            flash = not flash

            pygame.display.update()
            self.clock.tick(self.speed)

        self.offset -= 80


    # ------------------------
    # UPDATE FRAME
    # ------------------------
    def update(self):
        self.display.fill("black")

        # Grid
        for x in range(self.offset, self.w - self.offset, BLOCK_SIZE):
            for y in range(self.offset + SCORE_OFFSET, self.h - self.offset, BLOCK_SIZE):
                pygame.draw.rect(self.display, "gray9", (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Snake
        for pos in self.snake:
            pygame.draw.rect(self.display, "green", (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

        # Food
        pygame.draw.rect(self.display, "red", (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))

        # Spikes
        for pos in self.spikes:
            pygame.draw.rect(self.display, "white", (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

        score_text = score_font.render(f"Score: {self.score}", True, "white")
        self.display.blit(score_text, (25, 25))

        if self.expand_level != 4:
            goal_text = score_font.render(f"Next Goal: {self.score_goal}", True, "white")
            rect = goal_text.get_rect(topright=(self.w - 25, 25))
            self.display.blit(goal_text, rect)

        pygame.display.flip()


    # ------------------------
    # MAIN GAME LOGIC
    # ------------------------
    def play(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_s and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_a and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_d and self.direction != LEFT:
                    self.next_direction = RIGHT

        # Movement
        self.direction = self.next_direction
        self.move(self.direction)
        self.snake.insert(0, self.head)

        # Eating
        if self.head == self.food:
            self.placeFood()
            self.score += 1

            # SPEED UP every 3 apples
            if self.score % 3 == 0 and self.speed < MAX_SPEED:
                self.speed += 1
                print(f"Speed increased to {self.speed}")

        else:
            self.snake.pop()

        # Spike timing
        self.time += self.clock.get_time()
        if self.time > self.spikeTimer:
            self.time -= self.spikeTimer
            self.placeSpike()

        # Spike difficulty scaling
        if len(self.spikes) > self.spikeThreshold:
            self.spikeThreshold += INITIAL_SPIKE_THRESHOLD
            if self.spikeTimer > MIN_SPIKE_DELAY:
                self.spikeTimer -= 500
            print("Spike timer:", self.spikeTimer)

        # Collision
        if self.collision():
            return True

        # Expansion rules
        if self.expand_level != 4 and self.score >= self.score_goal:
            self.pending_expand = True

        if self.pending_expand and self.safe_to_expand():
            self.expand()
            self.expand_level += 1
            self.score_goal += 20
            self.pending_expand = False

        self.update()
        self.clock.tick(self.speed)


# ------------------------
# MAIN LOOP (With Revive)
# ------------------------
if __name__ == "__main__":
    game = Snake()

    while True:
        game.start_menu()
        game.reset()

        playing = True
        while playing:
            died = game.play()

            if died:

                # Attempt revive first
                success, percent = try_revive()

                if success:
                    # Display revive popup
                    game.display.fill("black")
                    msg = title_font.render(f"REVIVED! ({percent}%)", True, "green")
                    rect = msg.get_rect(center=(game.w//2, game.h//2))
                    game.display.blit(msg, rect)
                    pygame.display.update()
                    pygame.time.delay(1500)

                    # Soft revive
                    length = len(game.snake)

                    game.direction = RIGHT
                    game.next_direction = RIGHT

                    game.head = (game.w//2, game.h//2)
                    game.snake = []

                    #fits snake onto play area by filling the row above once we can not extend further in the current row
                    #going the opposite direction so sequential snake segments stay connected 
                    yOffset = 0
                    bounce = 0
                    longestRowSegment = game.head[0]
                    for i in range(0,length):
                        if yOffset % 2 == 0:
                            game.snake.append((longestRowSegment - bounce*BLOCK_SIZE, game.head[1] + yOffset*BLOCK_SIZE ))
                            if(longestRowSegment - (bounce +1 ) *BLOCK_SIZE ) <= game.offset:
                                yOffset += 1
                                longestRowSegment = game.offset
                                bounce = 0
                            else:
                                bounce += 1
                        else:
                            game.snake.append(( longestRowSegment + (bounce*BLOCK_SIZE)  , game.head[1] + yOffset*BLOCK_SIZE ))
                            if( longestRowSegment + (bounce +1 ) *BLOCK_SIZE) >= game.w - game.offset:
                                yOffset += 1
                                longestRowSegment = game.w - game.offset
                                bounce = 0
                            else:
                                bounce += 1

                    

                    game.spikes = []
                    game.time = 0
                    game.placeFood()

                    # Keep speed, spike difficulty, expansion, score
                    continue

                # If revive fails
                reset_revive()
                result = game.game_over_menu()

                if result == "menu":
                    playing = False
                elif result == "restart":
                    game.reset()
                else:
                    playing = False
