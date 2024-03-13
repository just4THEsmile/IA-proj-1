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

# Function to draw text on the screen
def draw_text(text, font, color, surface, y):
    textobj = font.render(text, True, color)  
    textrect = textobj.get_rect(center=(WIDTH / 2, y))
    surface.blit(textobj, textrect)

# Function to handle game mode selection and start the game
def game_mode_selection():
    game_modes = ["Human vs Human", "Human vs Computer", "Computer vs Computer"]
    menu_height = len(game_modes) * 100
    start_y = (HEIGHT - menu_height) // 2

    WINDOW.fill(BLACK)
    for i, option in enumerate(game_modes):
        menu_y_position = start_y + i * 100
        draw_text(option, FONT, WHITE, WINDOW, menu_y_position)
    pygame.display.update()

    while True:
        mx, my = pygame.mouse.get_pos()

        for i, option in enumerate(game_modes):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 100:
                WINDOW.fill(BLACK)  
                for j, inner_option in enumerate(game_modes):
                    text_color = GREEN if i == j else WHITE
                    draw_text(inner_option, FONT, text_color, WINDOW, start_y + j * 100)
                pygame.display.update()

                if pygame.mouse.get_pressed()[0]:
                    pygame.time.wait(200)  
                    difficulty_select()
                    return  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



def difficulty_select():
    difficulties = ["Easy", "Medium", "Hard"]  
    menu_height = len(difficulties) * 100
    start_y = (HEIGHT - menu_height) // 2

    WINDOW.fill(BLACK)
    for i, level in enumerate(difficulties):
        menu_y_position = start_y + i * 100
        draw_text(level, FONT, WHITE, WINDOW, menu_y_position)
    pygame.display.update()

    while True:
        mx, my = pygame.mouse.get_pos()

        for i, level in enumerate(difficulties):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 100:
                WINDOW.fill(BLACK)  
                for j, inner_level in enumerate(difficulties):
                    text_color = GREEN if i == j else WHITE
                    draw_text(inner_level, FONT, text_color, WINDOW, start_y + j * 100)
                pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Main menu function
def main_menu():
    menu_options = ["Start Game","Options", "Quit"]
    menu_height = len(menu_options) * 100
    start_y = (HEIGHT - menu_height) // 2
    while True:
        WINDOW.fill(BLACK)
        mx, my = pygame.mouse.get_pos()

        for i, option in enumerate(menu_options):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 50:
                draw_text(option, FONT, GREEN, WINDOW, menu_y_position)
                if pygame.mouse.get_pressed()[0] and option == "Start Game":
                    pygame.event.wait()
                    game_mode_selection()
                elif pygame.mouse.get_pressed()[0] and option == "Options":
                    pygame.quit()
                    sys.exit()
                elif pygame.mouse.get_pressed()[0] and option == "Quit":
                    pygame.quit()
                    sys.exit()
            else:
                draw_text(option, FONT, WHITE, WINDOW, menu_y_position)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Start the main menu
main_menu()