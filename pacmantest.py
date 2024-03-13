import pygame

class Pacman:
    def __init__(self, x, y, direction, speed, images, screen, level, width, height):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.images = images
        self.screen = screen
        self.level = level
        self.width = width
        self.height = height
        self.center_x = x + 23
        self.center_y = y + 24
        self.counter = 0
        self.score = 0
        self.powerup = False
        self.power_counter = 0
        self.eaten_ghosts = [False, False, False, False]
        self.turns_allowed = [True, True, True, True]
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.ghosts = []  # List of ghost objects
        self.blinky = None  # Blinky object
        self.inky = None  # Inky object
        self.pinky = None  # Pinky object
        self.clyde = None  # Clyde object
        self.targets = []  # List of target points for ghosts
        self.level_num = 1
        self.game_over = False
        self.lives = 3
        self.reset_positions()

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
        if self.direction == 0:
            screen.blit(pygame.transform.scale(self.images[self.counter // 5], (self.width, self.height)), (self.x, self.y))
        elif self.direction == 1:
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.images[self.counter // 5], True, False), (self.width, self.height)), (self.x, self.y))
        elif self.direction == 2:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(self.images[self.counter // 5], 90), (self.width, self.height)), (self.x, self.y))
        elif self.direction == 3:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(self.images[self.counter // 5], 270), (self.width, self.height)), (self.x, self.y))


    def move(self):
        num1 = (self.screen_height - 50) // 32
        num2 = self.screen_width // 30
        num3 = 15

        center_x = self.x + 23
        center_y = self.y + 24

        if self.direction == 0 and self.turns_allowed[0]:
            self.x += self.speed
        elif self.direction == 1 and self.turns_allowed[1]:
            self.x -= self.speed
        if self.direction == 2 and self.turns_allowed[2]:
            self.y -= self.speed
        elif self.direction == 3 and self.turns_allowed[3]:
            self.y += self.speed

        if 0 < self.center_x < self.screen_width - 30:
            if self.level[self.center_y // num1][self.center_x // num2] == 1:
                self.level[self.center_y // num1][self.center_x // num2] = 0
                self.score += 10
            if self.level[self.center_y // num1][self.center_x // num2] == 2:
                self.level[self.center_y // num1][self.center_x // num2] = 0
                self.score += 50
                self.powerup = True
                self.power_counter = 0
                self.eaten_ghosts = [False, False, False, False]

        self.blinky.update_target(self.targets[0])
        self.inky.update_target(self.targets[1])
        self.pinky.update_target(self.targets[2])
        self.clyde.update_target(self.targets[3])

        self.check_collisions()

    def check_collisions(self):
        num1 = (self.screen_height - 50) // 32
        num2 = self.screen_width // 30
        num3 = 15

        center_x = self.x + 23
        center_y = self.y + 24

        for ghost in self.ghosts:
            ghost_center_x = ghost.x + 15
            ghost_center_y = ghost.y + 15
            if abs(center_x - ghost_center_x) < num3 and abs(center_y - ghost_center_y) < num3:
                if self.powerup:
                    self.eaten_ghosts[self.ghosts.index(ghost)] = True
                else:
                    self.lives -= 1
                    self.reset_positions()
                    return

        for i in range(4):
            if self.eaten_ghosts[i]:
                self.ghosts[i].x = 13 * num2
                self.ghosts[i].y = 11 * num1
                self.eaten_ghosts[i] = False

        if self.score == 3520:
            self.level_num += 1
            self.load_level()
            self.score = 0
        if self.lives == 0:
            self.game_over = True

    def check_position(self):
        turns = [False, False, False, False]
        num1 = (self.screen_height - 50) // 32
        num2 = self.screen_width // 30
        num3 = 15

        if self.center_x // 30 < 29:
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
