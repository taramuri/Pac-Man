import copy
#from boards import board1
import pygame
import math
import chooseboard
import os
from pacmantest import Pacman

pygame.init()
WIDTH = 900
HEIGHT = 950
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
window_x = (screen_width - WIDTH) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},0"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
player_folder = os.path.join('assets', 'player')
# Завантаження картинок
# images = [pygame.image.load(os.path.join(player_folder, f"{i}.png")) for i in range(1, 5)]
# Приклад використання
# pacman_images = [
#     "assets/player/1.png",
#     "assets/player/2.png",
#     "assets/player/3.png",
#     "assets/player/4.png"
# ]

# Завантаження зображень з файлів
# loaded_images = []
# for image_path in pacman_images:
#     image = pygame.image.load(image_path)
#     loaded_images.append(image)

# # Передача завантажених зображень у конструктор класу Pacman
# pacman = Pacman(loaded_images)

# pacman.player_x = 450
# pacman.player_y = 663
# pacman.direction = 0
# pacman.fps = 60
# pacman.player_images = images
# pacman.screen = screen
# pacman.player_speed = 1
# pacman.redy_x = 55
# pacman.redy_y = 55
# pacman.redy_direction = 0
# pacman.yellow_x = 440
# pacman.yellow_y = 438
# pacman.yellow_direction = 2
# pacman.green_x = 440
# pacman.green_y = 388
# pacman.green_direction = 2
# pacman.clyde_x = 440
# pacman.clyde_y = 438
# pacman.clyde_direction = 2
# pacman.counter = 0
# pacman.flicker = False
# pacman.turns_allowed = [False, False, False, False]
# pacman.direction_command = 0
# pacman.score = 0
# pacman.powerup = False
# pacman.power_counter = 0
# pacman.eaten_ghost = [False, False, False, False]
# pacman.targets = [(pacman.player_x, pacman.player_y)] * 4
# pacman.red_dead = False
# pacman.green_dead = False
# pacman.clyde_dead = False
# pacman.yellow_dead = False
# pacman.redy_box = False
# pacman.green_box = False
# pacman.clyde_box = False
# pacman.yellow_box = False
# pacman.moving = False
# pacman.ghost_speeds = [2, 2, 2, 2]
# pacman.startup_counter = 0
# pacman.lives = 3
# pacman.game_over = False
# pacman.game_won = False


board = chooseboard.choose_board()
level = chooseboard.get_board(board)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)

color = 'blue'
PI = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player/{i}.png'), (45, 45)))
red_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/red.png'), (45, 45))
green_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/green.png'), (45, 45))
yellow_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/yellow.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/dead.png'), (45, 45))
player_x = 450
player_y = 663
player_speed = 2
direction = 0
red_x = 56
red_y = 50
red_direction = 0
green_x = 440
green_y = 388
green_direction = 2
yellow_x = 440
yellow_y = 438
yellow_direction = 2
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
red_dead = False
green_dead = False
yellow_dead = False
red_box = False
green_box = False
yellow_box = False
moving = False
ghost_speeds = [2, 2, 2]
startup_counter = 0
lives = 1
game_over = False
game_won = False

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_yellow(self):
        # r, l, u, d
        # yellow is going to turn whenever advantageous for pursuit
        #жовтий збирається повернути, коли буде вигідно для переслідування
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -30
        return self.x_pos, self.y_pos, self.direction

    def move_red(self):
        # r, l, u, d
        # red is going to turn whenever colliding with walls, otherwise continue straight
        #збирається повертати щоразу, коли зіткнеться зі стінами, інакше продовжує рух прямо
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_green(self):
        # r, l, u, d
        # green turns up or down at any point to pursue, but left and right only on collision
        #green збирається повертати ліворуч або праворуч, коли це вигідно, але лише вгору чи вниз у разі зіткнення
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


def draw_misc(): #win or no
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))

def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts

def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def get_targets(red_x, red_y, green_x, green_y, yellow_x, yellow_y):
    red_target = (0, 0)
    green_target = (0, 0)
    yellow_target = (0, 0)
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not red.dead and not eaten_ghost[0]:
            red_target = (runaway_x, runaway_y)
        elif not red.dead and eaten_ghost[0]:
            if 340 < red_x < 560 and 340 < red_y < 500:
                red_target = (400, 100)
            else:
                red_target = (player_x, player_y)
        else:
            red_target = return_target
        if not green.dead and not eaten_ghost[1]:
            green_target = (runaway_x, player_y)
        elif not green.dead and eaten_ghost[1]:
            if 340 < green_x < 560 and 340 < green_y < 500:
                green_target = (400, 100)
            else:
                green_target = (player_x, player_y)
        else:
            green_target = return_target    
    else:
        if not red.dead:
            if 340 < red_x < 560 and 340 < red_y < 500:
                red_target = (400, 100)
            else:
                red_target = (player_x, player_y)
        else:
            red_target = return_target
        if not green.dead:
            if 340 < green_x < 560 and 340 < green_y < 500:
                green_target = (400, 100)
            else:
                green_target = (player_x, player_y)
        else:
            green_target = return_target    
        if not yellow.dead:
            if 340 < yellow_x < 560 and 340 < yellow_y < 500:
                yellow_target = (400, 100)
            else:
                yellow_target = (player_x, player_y)
        else:
            green_target = return_target    
    return [red_target, green_target, yellow_target]

run = True
while run:
    timer.tick(fps)

    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    #pacman.update()  # Оновлення координат та напрямку пакмена
    #pacman.draw(screen)  
    center_x = player_x + 23
    center_y = player_y + 24



    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if red_dead:
        ghost_speeds[0] = 4
    if green_dead:
        ghost_speeds[1] = 4
    if yellow_dead:
        ghost_speeds[2] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False


    
    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)  
    draw_player() 
    red = Ghost(red_x, red_y, targets[0], ghost_speeds[0], red_img, red_direction, red_dead,
                   red_box, 0)
    green = Ghost(green_x, green_y, targets[1], ghost_speeds[1], green_img, green_direction, green_dead,
                 green_box, 1)
    yellow = Ghost(yellow_x, yellow_y, targets[2], ghost_speeds[2], yellow_img, yellow_direction, yellow_dead,
                  yellow_box, 2)
    draw_misc()
    targets = get_targets(red_x, red_y, green_x, green_y, yellow_x, yellow_y)
    
    turns_allowed = check_position(center_x, center_y)
    if moving:
        if not red_dead and not red.in_box:
            red_x, red_y, red_direction = red.move_red()
        else:
            red_x, red_y, red_direction = red.move_yellow()
        if not green_dead and not green.in_box:
            green_x, green_y, green_direction = green.move_green()
        else:
            green_x, green_y, green_direction = green.move_yellow()
        yellow_x, yellow_y, yellow_direction = yellow.move_yellow()
    # add to if not powerup to check if eaten ghosts
    

    if not powerup:
        if (player_circle.colliderect(red.rect) and not red.dead) or \
                (player_circle.colliderect(green.rect) and not green.dead) or \
                (player_circle.colliderect(yellow.rect) and not yellow.dead):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                green_x = 440
                green_y = 388
                green_direction = 2
                yellow_x = 440
                yellow_y = 438
                yellow_direction = 2
                eaten_ghost = [False, False, False, False]
                red_dead = False
                green_dead = False
                clyde_dead = False
                yellow_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(red.rect) and eaten_ghost[0] and not red.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            green_x = 440
            green_y = 388
            green_direction = 2
            yellow_x = 440
            yellow_y = 438
            yellow_direction = 2
            eaten_ghost = [False, False, False, False]
            red_dead = False
            green_dead = False
            clyde_dead = False
            yellow_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(green.rect) and eaten_ghost[1] and not green.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            green_x = 440
            green_y = 388
            green_direction = 2
            yellow_x = 440
            yellow_y = 438
            yellow_direction = 2
            eaten_ghost = [False, False, False, False]
            red_dead = False
            green_dead = False
            clyde_dead = False
            yellow_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(yellow.rect) and eaten_ghost[2] and not yellow.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            green_x = 440
            green_y = 388
            green_direction = 2
            yellow_x = 440
            yellow_y = 438
            yellow_direction = 2
            eaten_ghost = [False, False, False, False]
            red_dead = False
            green_dead = False
            clyde_dead = False
            yellow_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(red.rect) and not red.dead and not eaten_ghost[0]:
        red_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(green.rect) and not green.dead and not eaten_ghost[1]:
        green_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(yellow.rect) and not yellow.dead and not eaten_ghost[2]:
        yellow_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction_command = 0
                if event.key == pygame.K_LEFT:
                    direction_command = 1
                if event.key == pygame.K_UP:
                    direction_command = 2
                if event.key == pygame.K_DOWN:
                    direction_command = 3
                if event.key == pygame.K_SPACE and (game_over or game_won):
                    powerup = False
                    power_counter = 0
                    lives -= 1
                    startup_counter = 0
                    player_x = 450
                    player_y = 663
                    direction = 0
                    direction_command = 0
                    redy_x = 56
                    redy_y = 58
                    redy_direction = 0
                    green_x = 440
                    green_y = 388
                    green_direction = 2
                    yellow_x = 440
                    yellow_y = 438
                    yellow_direction = 2
                    clyde_x = 440
                    clyde_y = 438
                    clyde_direction = 2
                    eaten_ghost = [False, False, False, False]
                    red_dead = False
                    green_dead = False
                    clyde_dead = False
                    yellow_dead = False
                    score = 0
                    lives = 3
                    level = copy.deepcopy(boards)
                    game_over = False
                    game_won = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and direction_command == 0:
                    direction_command = direction
                if event.key == pygame.K_LEFT and direction_command == 1:
                    direction_command = direction
                if event.key == pygame.K_UP and direction_command == 2:
                    direction_command = direction
                if event.key == pygame.K_DOWN and direction_command == 3:
                    direction_command = direction

      
    if red.in_box and red_dead:
        red_dead = False
    if green.in_box and green_dead:
        green_dead = False
    if yellow.in_box and yellow_dead:
        yellow_dead = False

    pygame.display.flip()
pygame.quit()
