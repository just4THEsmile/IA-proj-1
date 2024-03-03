import pygame
import logic
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font
FONT = pygame.font.SysFont('arial', 60)

# Menu options
menu_options = ['Start Game', 'Quit']
options_functions = {}  # This will later be used to map options to functions

def draw_text(text, font, color, surface, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(WIDTH / 2, y))
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        WINDOW.fill(BLACK)

        mx, my = pygame.mouse.get_pos()

        # Draw menu options
        for i, option in enumerate(menu_options):
            menu_y_position = 150 + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 50:
                draw_text(option, FONT, GREEN, WINDOW, menu_y_position)
                if pygame.mouse.get_pressed()[0]:
                    if option == "Start Game":
                        board = logic.Board()
                        running = True
                        while running:
                            # Handle events
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    pass

                            
                            
                            board.draw()
                            pygame.display.flip()
                    elif option == "Quit":
                        pygame.quit()
                        sys.exit()
            else:
                draw_text(option, FONT, WHITE, WINDOW, menu_y_position)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main_menu()
