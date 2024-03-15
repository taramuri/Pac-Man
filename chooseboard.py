import pygame
from boards import board1, board2, board3
import copy

def choose_board():
    pygame.init()

    WIDTH, HEIGHT = 1050, 600
    WINDOW_SIZE = (WIDTH, HEIGHT)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)

    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    window_x = (WIDTH - WIDTH) // 2
    window_y = (HEIGHT - HEIGHT) // 2

    # Download and resize map images
    card1 = pygame.image.load('assets/boards/1.jpg')
    card1 = pygame.transform.scale(card1, (300, 300))

    card2 = pygame.image.load('assets/boards/2.jpg')
    card2 = pygame.transform.scale(card2, (300, 300))

    card3 = pygame.image.load('assets/boards/3.jpg')
    card3 = pygame.transform.scale(card3, (300, 300))

    cards = [card1, card2, card3]
    card_rects = []

    # Location of cards on the screen
    total_width = len(cards) * 300 + (len(cards) - 1) * 50
    starting_x = (WIDTH - total_width) // 2
    y = 200
    for card in cards:
        screen.blit(card, (starting_x, y))
        card_rect = pygame.Rect(starting_x, y, card.get_width(), card.get_height())
        pygame.draw.rect(screen, YELLOW, card_rect, 5)
        card_rects.append(card_rect)
        starting_x += card.get_width() + 50

    # Adding text
    font = pygame.font.SysFont(None, 36)
    text = font.render("Select a board to play", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(text, text_rect)
    
    pygame.display.flip()
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos):
                        return i + 1

        clock.tick(60)
            
def get_board(chosen_card):
    
    if chosen_card == 1:
        return copy.deepcopy(board1)
    if chosen_card == 2:
        return copy.deepcopy(board2)
    if chosen_card == 3:
        return copy.deepcopy(board3)
    else:
        raise ValueError("You didn't choose the map.")
