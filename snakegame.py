# Game over scenario and pausing a game (fixed & portable)

import os
import random
import pygame
from pygame.locals import *

# ---------- Settings ----------
SIZE = 40
WINDOW_W, WINDOW_H = 1000, 800
BACKGROUND_COLOR = (24, 4, 24)

# Resource base (portable paths)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(BASE_DIR, "resources")

# Assets
IMG_APPLE = os.path.join(RES, "apple.jpg")
IMG_BLOCK = os.path.join(RES, "block.jpg")
SND_BG = os.path.join(RES, "1_snake_game_resources_bg_music_1.mp3")
SND_CRASH = os.path.join(RES, "1_snake_game_resources_crash.mp3")
SND_DING = os.path.join(RES, "1_snake_game_resources_ding.mp3")


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(IMG_APPLE).convert()
        # Start on-grid
        self.x = 3 * SIZE
        self.y = 3 * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        # Keep within grid bounds
        max_x_cells = (WINDOW_W // SIZE) - 1
        max_y_cells = (WINDOW_H // SIZE) - 1
        self.x = random.randint(0, max_x_cells) * SIZE
        self.y = random.randint(0, max_y_cells) * SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(IMG_BLOCK).convert()

        self.direction = "down"
        self.length = 1
        self.x = [5 * SIZE]
        self.y = [5 * SIZE]

    # Direction controls
    def move_left(self):  self.direction = "left"
    def move_right(self): self.direction = "right"
    def move_up(self):    self.direction = "up"
    def move_down(self):  self.direction = "down"

    def walk(self):
        # update body (from tail to head)
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == "left":
            self.x[0] -= SIZE
        elif self.direction == "right":
            self.x[0] += SIZE
        elif self.direction == "up":
            self.y[0] -= SIZE
        elif self.direction == "down":
            self.y[0] += SIZE

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        # placeholders; will be set on next walk()
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game (Fixed)")
        self.surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pygame.time.Clock()

        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

        self.play_background_music()

    # ----- Audio -----
    def play_background_music(self):
        try:
            pygame.mixer.music.load(SND_BG)
            pygame.mixer.music.play(-1, 0)
        except Exception as e:
            print("Background music load error:", e)

    def play_sound(self, sound_name):
        try:
            if sound_name == "crash":
                sound = pygame.mixer.Sound(SND_CRASH)
            elif sound_name == "ding":
                sound = pygame.mixer.Sound(SND_DING)
            else:
                return
            sound.play()
        except Exception as e:
            print("Sound load/play error:", e)

    # ----- Mechanics -----
    @staticmethod
    def is_collision(x1, y1, x2, y2):
        return (x1 >= x2 and x1 < x2 + SIZE) and (y1 >= y2 and y1 < y2 + SIZE)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        # score equals snake length
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (WINDOW_W - 150, 10))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press Enter to play again. Press Escape to exit.", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def draw_everything(self):
        self.surface.fill(BACKGROUND_COLOR)
        self.snake.draw()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

    def check_collisions(self):
        # Snake eats apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
            self.play_sound("ding")

        # Snake hits itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise Exception("Self Collision")

        # Snake hits wall
        head_x, head_y = self.snake.x[0], self.snake.y[0]
        if head_x < 0 or head_x >= WINDOW_W or head_y < 0 or head_y >= WINDOW_H:
            self.play_sound("crash")
            raise Exception("Wall Collision")

    def play(self):
        self.snake.walk()
        self.check_collisions()
        self.draw_everything()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT and self.snake.direction != "right":
                            self.snake.move_left()
                        elif event.key == K_RIGHT and self.snake.direction != "left":
                            self.snake.move_right()
                        elif event.key == K_UP and self.snake.direction != "down":
                            self.snake.move_up()
                        elif event.key == K_DOWN and self.snake.direction != "up":
                            self.snake.move_down()

            try:
                if not pause:
                    self.play()
            except Exception:
                self.show_game_over()
                pause = True
                self.reset()

            # Control speed (about 10 FPS similar to time.sleep(0.1~0.25))
            self.clock.tick(10)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()

    
    
