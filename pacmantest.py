import pygame
from board import board1
import math

class Pacman:
    def __init__(self, x, y, direction, speed, images, screen):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.images = images
        self.screen = screen
        self.center_x = x + 23
        self.center_y = y + 24
        self.counter = 0
        self.flicker = False

    def draw(self):
        pacman_image = self.images[self.direction]
        if self.flicker:
            self.counter += 1
            if self.counter % 6 == 0:
                pacman_image = None
            if self.counter == 30:
                self.counter = 0
                self.flicker = False
        if pacman_image:
            self.screen.blit(pacman_image, (self.x, self.y))


    def move(self):
        num1 = (self.screen_height - 50) // 32
        num2 = self.screen_width // 30
        num3 = 15

        # Визначаємо центральну точку Пакмена
        center_x = self.x + 23
        center_y = self.y + 24

        # Перевірка можливих напрямків руху та зміна координат
        if self.direction == 0 and self.turns_allowed[0]:
            self.x += self.speed
        elif self.direction == 1 and self.turns_allowed[1]:
            self.x -= self.speed
        if self.direction == 2 and self.turns_allowed[2]:
            self.y -= self.speed
        elif self.direction == 3 and self.turns_allowed[3]:
            self.y += self.speed

        # Перевірка зіткнення з об'єктами на полі гри та оновлення гри
        if 0 < self.x < self.screen_width - 30:
            if self.level[center_y // num1][center_x // num2] == 1:
                self.level[center_y // num1][center_x // num2] = 0
                self.score += 10
            if self.level[center_y // num1][center_x // num2] == 2:
                self.level[center_y // num1][center_x // num2] = 0
                self.score += 50
                self.powerup = True
                self.power_counter = 0
                self.eaten_ghosts = [False, False, False, False]

        # Оновлення атрибутів об'єктів blinky, inky, pinky та clyde
        self.blinky.update_target(self.targets[0])
        self.inky.update_target(self.targets[1])
        self.pinky.update_target(self.targets[2])
        self.clyde.update_target(self.targets[3])

        # Перевірка колізій з привидами та оновлення гри
        self.check_collisions()


    def check_collisions(self):
        num1 = (self.screen_height - 50) // 32
        num2 = self.screen_width // 30
        num3 = 15

        # Визначаємо центральну точку Пакмена
        center_x = self.x + 23
        center_y = self.y + 24

        # Перевірка колізій з привидами
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

        # Оновлення привидів у разі з'їдання Пакменом сили розуму
        for i in range(4):
            if self.eaten_ghosts[i]:
                self.ghosts[i].x = 13 * num2
                self.ghosts[i].y = 11 * num1
                self.eaten_ghosts[i] = False

        # Перевірка виграшу або програшу
        if self.score == 3520:
            self.level_num += 1
            self.load_level()
            self.score = 0
        if self.lives == 0:
            self.game_over = True


    def check_collisions(self):
        # Implementation of the check_collisions function to check collisions
        num1 = (self.screen.get_height() - 50) // 32
        num2 = self.screen.get_width() // 30
        if 0 < self.center_x < 870:
            if self.level[self.center_y // num1][self.center_x // num2] == 1:
                self.level[self.center_y // num1][self.center_x // num2] = 0
                self.score += 10  # Increase score for regular pellet
            if self.level[self.center_y // num1][self.center_x // num2] == 2:
                self.level[self.center_y // num1][self.center_x // num2] = 0
                self.score += 50  # Increase score for bonus pellet



    def update(self):
        # Переміщення Пакмена
        self.move()

        # Перевірка колізій
        self.check_collisions()

        # Перевірка позиції Пакмена
        self.check_position()


    def handle_input(self, event):
        # Handle user input for controlling Pacman
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.change_direction('left')
            elif event.key == pygame.K_RIGHT:
                self.change_direction('right')
            elif event.key == pygame.K_UP:
                self.change_direction('up')
            elif event.key == pygame.K_DOWN:
                self.change_direction('down')

