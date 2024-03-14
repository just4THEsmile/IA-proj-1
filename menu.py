import pygame
import logic
import sys
import gameloop
import draw

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
def game_mode_selection(size):
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
        hover = None

        for i, mode in enumerate(game_modes):
            mode_y_position = start_y + i * 100
            
            if 100 < mx < WIDTH - 100 and mode_y_position < my < mode_y_position + 100:
                hover = i

                if pygame.mouse.get_pressed()[0]:
                    pygame.event.wait()
                    if mode == "Human vs Human":
                        gameloop.game_pvp(size)
                        main_menu()
                        return
                    elif mode == "Human vs Computer":
                        difficulty = difficulty_select()  
                        gameloop.game_pvb(draw.RED, size, difficulty)  
                        main_menu()
                        return
                    
        WINDOW.fill(BLACK)
        for j, option in enumerate(game_modes):
            color = GREEN if j == hover else WHITE
            menu_y_position = start_y + j * 100
            draw_text(option, FONT, color, WINDOW, menu_y_position)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def difficulty_select():
    difficulties = ["Easy", "Medium", "Hard"]
    menu_height = len(difficulties) * 100
    start_y = (HEIGHT - menu_height) // 2


    while True:
        mx, my = pygame.mouse.get_pos()
        WINDOW.fill(BLACK)  

        for i, level in enumerate(difficulties):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 100:
                draw_text(level, FONT, GREEN, WINDOW, menu_y_position)  
                if pygame.mouse.get_pressed()[0]:  
                    pygame.event.wait()  
                    return i + 1  
            else:
                draw_text(level, FONT, WHITE, WINDOW, menu_y_position)  

        pygame.display.update()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



def size_select():
    sizes = ["3x3", "4x4", "5x5"]  
    menu_height = len(sizes) * 100
    start_y = (HEIGHT - menu_height) // 2

    WINDOW.fill(BLACK)
    for i, size in enumerate(sizes):
        menu_y_position = start_y + i * 100
        draw_text(size, FONT, WHITE, WINDOW, menu_y_position)
    pygame.display.update()

    while True:
        mx, my = pygame.mouse.get_pos()

        for i, size in enumerate(sizes):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 100:
                WINDOW.fill(BLACK)  
                for j, inner_size in enumerate(sizes):
                    text_color = GREEN if i == j else WHITE
                    draw_text(inner_size, FONT, text_color, WINDOW, start_y + j * 100)
                    if pygame.mouse.get_pressed()[0] and size == "3x3":
                        pygame.event.wait()
                        game_mode_selection(3)
                    elif pygame.mouse.get_pressed()[0] and size== "4x4":
                        pygame.event.wait()
                        game_mode_selection(4)
                    elif pygame.mouse.get_pressed()[0] and size == "5x5":
                        pygame.event.wait()
                        game_mode_selection(5)
                pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Main menu function
def main_menu():
    menu_options = ["Start Game", "Quit"]
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
                    size_select()
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