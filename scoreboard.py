import pygame

class Scoreboard:
    def __init__(self, x, y, font_size=36, font_color=(255, 255, 255), bg_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.font_color = font_color
        self.bg_color = bg_color
        self.score = 0
        self.lives = 3
        self.font = pygame.font.Font('freesansbold.ttf', font_size)

    def increase_score(self, points):
        self.score += points
    
    def decrease_lives(self):
        self.lives -= 1

    def reset_score(self):
        self.score = 0

    def draw(self, screen):
        score_text = self.font.render("Score: " + str(self.score), True, self.font_color, self.bg_color)
        lives_text = self.font.render("Lives: " + str(self.lives), True, self.font_color, self.bg_color)
        score_rect = score_text.get_rect()
        lives_rect = lives_text.get_rect()
        score_rect.topleft = (self.x, self.y)
        lives_rect.topleft = (self.x+760, self.y)  # Зміщення тексту кількості життів вниз відносно рахунку
        screen.blit(score_text, score_rect)
        screen.blit(lives_text, lives_rect)
