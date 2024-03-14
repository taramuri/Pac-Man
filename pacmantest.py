import pygame
import math
import chooseboard

class Pacman:
    def __init__(self, images):
        pygame.init()

        self.WIDTH = 900
        self.HEIGHT = 950
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        
        self.color = 'blue'
        self.PI = math.pi
        self.current_image_index = 0
        self.current_image = self.images[self.current_image_index]
        self.player_images = [pygame.transform.scale(pygame.image.load(f'assets/player/{i}.png'), (45, 45)) for i in range(1, 5)]
        self.blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/red.png'), (45, 45))
        self.pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/pink.png'), (45, 45))
        self.inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/blue.png'), (45, 45))
        self.clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/orange.png'), (45, 45))
        self.spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/powerup.png'), (45, 45))
        self.dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghosts/dead.png'), (45, 45))
        board = chooseboard.choose_board()
        self.level = chooseboard.get_board(board)
        self.player_x = 450
        self.player_y = 663
        self.direction = 0
        self.blinky_x = 56
        self.blinky_y = 58
        self.blinky_direction = 0
        self.inky_x = 440
        self.inky_y = 388
        self.inky_direction = 2
        self.pinky_x = 440
        self.pinky_y = 438
        self.pinky_direction = 2
        self.clyde_x = 440
        self.clyde_y = 438
        self.clyde_direction = 2
        self.counter = 0
        self.flicker = False
        self.turns_allowed = [False, False, False, False]
        self.direction_command = 0
        self.player_speed = 2
        self.score = 0
        self.powerup = False
        self.power_counter = 0
        self.eaten_ghost = [False, False, False, False]
        self.targets = [(self.player_x, self.player_y)] * 4
        self.blinky_dead = False
        self.inky_dead = False
        self.clyde_dead = False
        self.pinky_dead = False
        self.blinky_box = False
        self.inky_box = False
        self.clyde_box = False
        self.pinky_box = False
        self.moving = False
        self.ghost_speeds = [2, 2, 2, 2]
        self.startup_counter = 0
        self.lives = 3
        self.game_over = False
        self.game_won = False
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()
        self.center_x = self.player_x 
        self.center_y = self.player_y
        self.images = []
        self.images = images
        self.width = self.current_image.get_width()
        self.height = self.current_image.get_height()


    def draw_misc(self):
        # Drawing score
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Drawing lives
        for i in range(self.lives):
            life_image = pygame.transform.scale(self.player_images[0], (30, 30))
            self.screen.blit(life_image, (10 + i * 40, 40))

        # Drawing game over message if the game is over
        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.WIDTH // 2 - 50, self.HEIGHT // 2))

        # Drawing victory message if the game is won
        if self.game_won:
            victory_text = self.font.render('You Win!', True, (0, 255, 0))
            self.screen.blit(victory_text, (self.WIDTH // 2 - 50, self.HEIGHT // 2))

        # Drawing other messages or elements as needed

    # Додайте цей код в клас вашої гри Pacman і використовуйте його в основному циклі гри для відображення інформації на екрані.


    def reset_positions(self):
        # Reset Pacman and ghost positions
        self.x = 15 * (self.screen_width // 30)
        self.y = 23 * ((self.screen_height - 50) // 32)
        self.direction = 0

    def load_level(self):
        # Load a new level
        pass  # Implement loading a new level

    def change_direction(self, direction):
        # Change Pacman's direction
        if direction == 'left':
            self.direction = 1
        elif direction == 'right':
            self.direction = 0
        elif direction == 'up':
            self.direction = 2
        elif direction == 'down':
            self.direction = 3

    def draw(self, screen):
        image_index = self.counter // 5
        if 0 <= image_index < len(self.images):
            if self.direction == 0:
                screen.blit(pygame.transform.scale(self.images[image_index], (self.width, self.height)), (self.x, self.y))
            elif self.direction == 1:
                screen.blit(pygame.transform.scale(pygame.transform.flip(self.images[image_index], True, False), (self.width, self.height)), (self.x, self.y))
            elif self.direction == 2:
                screen.blit(pygame.transform.scale(pygame.transform.rotate(self.images[image_index], 90), (self.width, self.height)), (self.x, self.y))
            elif self.direction == 3:
                screen.blit(pygame.transform.scale(pygame.transform.rotate(self.images[image_index], 270), (self.width, self.height)), (self.x, self.y))



    def move(self):
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH - 50) // 32
        if self.direction_command == 1:
            if not self.check_wall(self.player_x - 1, self.player_y):
                self.direction = 1
        elif self.direction_command == 2:
            if not self.check_wall(self.player_x + 1, self.player_y):
                self.direction = 2
        elif self.direction_command == 3:
            if not self.check_wall(self.player_x, self.player_y - 1):
                self.direction = 3
        elif self.direction_command == 4:
            if not self.check_wall(self.player_x, self.player_y + 1):
                self.direction = 4
        if self.direction == 1 and not self.check_wall(self.player_x - 1, self.player_y):
            self.player_x -= self.player_speed
        elif self.direction == 2 and not self.check_wall(self.player_x + 1, self.player_y):
            self.player_x += self.player_speed
        elif self.direction == 3 and not self.check_wall(self.player_x, self.player_y - 1):
            self.player_y -= self.player_speed
        elif self.direction == 4 and not self.check_wall(self.player_x, self.player_y + 1):
            self.player_y += self.player_speed

    def check_collisions(self):
        num1 = (self.HEIGHT - 50) // 32
        num2 = self.WIDTH // 30
        center_x = self.player_x + 23
        center_y = self.player_y + 24

        if 0 < self.player_x < 870:
            if self.level[center_y // num1][center_x // num2] == 1:
                self.level[center_y // num1][center_x // num2] = 0
                self.score += 10
            if self.level[center_y // num1][center_x // num2] == 2:
                self.level[center_y // num1][center_x // num2] = 0
                self.score += 50
                self.powerup = True
                self.power_counter = 0
                self.eaten_ghosts = [False, False, False, False]


    def check_position(self):
        turns = [False, False, False, False]
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH - 50) // 29
        num3 = (self.WIDTH % 29) // 2

        if 0 <= self.center_x // num2 < 29:
            if self.direction == 0:
                if self.level[self.center_y // num1][(self.center_x - num3) // num2] < 3:
                    turns[1] = True
            if self.direction == 1:
                if self.level[self.center_y // num1][(self.center_x + num3) // num2] < 3:
                    turns[0] = True
            if self.direction == 2:
                if self.level[(self.center_y + num3) // num1][self.center_x // num2] < 3:
                    turns[3] = True
            if self.direction == 3:
                if self.level[(self.center_y - num3) // num1][self.center_x // num2] < 3:
                    turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if self.level[(self.center_y + num3) // num1][self.center_x // num2] < 3:
                        turns[3] = True
                    if self.level[(self.center_y - num3) // num1][self.center_x // num2] < 3:
                        turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if self.level[self.center_y // num1][(self.center_x - num2) // num2] < 3:
                        turns[1] = True
                    if self.level[self.center_y // num1][(self.center_x + num2) // num2] < 3:
                        turns[0] = True
            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if self.level[(self.center_y + num1) // num1][self.center_x // num2] < 3:
                        turns[3] = True
                    if self.level[(self.center_y - num1) // num1][self.center_x // num2] < 3:
                        turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if self.level[self.center_y // num1][(self.center_x - num3) // num2] < 3:
                        turns[1] = True
                    if self.level[self.center_y // num1][(self.center_x + num3) // num2] < 3:
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True

        return turns

    def update(self):
        self.handle_input(pygame.event.get())  # обробляємо введення
        self.move()  # рухаємо пакмена
        # оновлюємо гру
        self.check_collisions()
        self.check_position()


    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.change_direction('left')
                elif event.key == pygame.K_RIGHT:
                    self.change_direction('right')
                elif event.key == pygame.K_UP:
                    self.change_direction('up')
                elif event.key == pygame.K_DOWN:
                    self.change_direction('down')
