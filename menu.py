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
    menu_options = ["Human vs Human", "Human vs Computer", "Computer vs Computer"]
    menu_height = len(menu_options) * 100
    start_y = (HEIGHT - menu_height) // 2
    while True:
        WINDOW.fill(BLACK)
        mx, my = pygame.mouse.get_pos()
        hover = None

        for i, option in enumerate(menu_options):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 50:
                draw_text(option, FONT, GREEN, WINDOW, menu_y_position)
                if pygame.mouse.get_pressed()[0] and option == "Human vs Human":
                    pygame.event.wait()
                    winner=gameloop.game_pvp(size)
                    game_over(winner)
                    main_menu()
                elif pygame.mouse.get_pressed()[0] and option == "Human vs Computer":
                    pygame.event.wait()
                    print("Human vs Computer")
                    difficulty_select_PVB(size)
                    main_menu()
                elif pygame.mouse.get_pressed()[0] and option == "Computer vs Computer":
                    pygame.event.wait()
                    difficulty_select_BVB(size)
                    game_over(winner)
                    main_menu()
            else:
                draw_text(option, FONT, WHITE, WINDOW, menu_y_position)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# to select the difficulty of the bot on the bot vs bot mode
def difficulty_select_BVB(size):
    menu_options = ["Easy", "Medium", "Hard"]
    menu_height = len(menu_options) * 100
    start_y = (HEIGHT - menu_height) // 2
    while True:
        WINDOW.fill(BLACK)
        mx, my = pygame.mouse.get_pos()
        for i, option in enumerate(menu_options):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 50:
                draw_text(option, FONT, GREEN, WINDOW, menu_y_position)
                if pygame.mouse.get_pressed()[0] and option == "Easy":
                    pygame.event.wait()
                    winner=gameloop.game_bvb(size,1)
                    game_over(winner)
                    main_menu()
                elif pygame.mouse.get_pressed()[0] and option == "Medium":
                    pygame.event.wait()
                    winner=gameloop.game_bvb(size,2)
                    game_over(winner)
                    main_menu()
                elif pygame.mouse.get_pressed()[0] and option == "Hard":
                    pygame.event.wait()
                    winner=gameloop.game_bvb(size,3)
                    game_over(winner)
                    main_menu()
            else:
                draw_text(option, FONT, WHITE, WINDOW, menu_y_position)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Function to handle difficulty selection for player vs bot mode
def difficulty_select_PVB(size):
    menu_options = ["Easy", "Medium", "Hard"]
    menu_height = len(menu_options) * 100
    start_y = (HEIGHT - menu_height) // 2
    while True:
        WINDOW.fill(BLACK)
        mx, my = pygame.mouse.get_pos()
        for i, option in enumerate(menu_options):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 50:
                draw_text(option, FONT, GREEN, WINDOW, menu_y_position)
                if pygame.mouse.get_pressed()[0] and option == "Easy":
                    pygame.event.wait()
                    first_move_select(size,1)

                    main_menu()
                elif pygame.mouse.get_pressed()[0] and option == "Medium":
                    pygame.event.wait()
                    first_move_select(size,2)
                    main_menu()
                elif pygame.mouse.get_pressed()[0] and option == "Hard":
                    pygame.event.wait()
                    first_move_select(size,3)
                    main_menu()
            else:
                draw_text(option, FONT, WHITE, WINDOW, menu_y_position)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# to select whether the player wants to move first or second
def first_move_select(size,difficulty):
    menu_options = ["Move First", "Move Second"]
    menu_height = len(menu_options) * 100
    start_y = (HEIGHT - menu_height) // 2
    while True:
        WINDOW.fill(BLACK)
        mx, my = pygame.mouse.get_pos()
        for i, option in enumerate(menu_options):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 50:
                draw_text(option, FONT, GREEN, WINDOW, menu_y_position)
                if pygame.mouse.get_pressed()[0] and option == "Move First":
                    pygame.event.wait()
                    winner=gameloop.game_pvb(draw.RED,size,difficulty)

                    game_over(winner)
                elif pygame.mouse.get_pressed()[0] and option == "Move Second":
                    pygame.event.wait()
                    winner=gameloop.game_pvb(draw.BLUE,size,difficulty)
                    game_over(winner)
            else:
                draw_text(option, FONT, WHITE, WINDOW, menu_y_position)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def game_over(winner):
    WINDOW.fill(BLACK)
    print(winner)
    if winner == draw.RED:
        draw_text("Red wins!", FONT, RED, WINDOW, HEIGHT // 2)
    elif winner == draw.BLUE:
        draw_text("Blue wins!", FONT, draw.BLUE, WINDOW, HEIGHT // 2)
    else:
        draw_text("It's a tie!", FONT, WHITE, WINDOW, HEIGHT // 2)    
    menu_options = ["Play Again","Exit"]
    menu_height = len(menu_options) * 100
    start_y = (HEIGHT - menu_height)+100 // 2
    while True:
        mx, my = pygame.mouse.get_pos()
        for i, option in enumerate(menu_options):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 50:
                draw_text(option, FONT, GREEN, WINDOW, menu_y_position)
                if pygame.mouse.get_pressed()[0] and option == "Play Again":
                    pygame.event.wait()
                    main_menu()
                elif pygame.mouse.get_pressed()[0] and option == "Exit":
                    sys.exit()  
            else:
                draw_text(option, FONT, WHITE, WINDOW, menu_y_position)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



def size_select():
    menu_options = ["3x3", "4x4", "5x5"]  
    menu_height = len(menu_options) * 100
    start_y = (HEIGHT - menu_height) // 2
    while True:
        WINDOW.fill(BLACK)
        mx, my = pygame.mouse.get_pos()

        for i, option in enumerate(menu_options):
            menu_y_position = start_y + i * 100
            if 100 < mx < WIDTH - 100 and menu_y_position < my < menu_y_position + 50:
                draw_text(option, FONT, GREEN, WINDOW, menu_y_position)
                if pygame.mouse.get_pressed()[0] and option == "3x3":
                    pygame.event.wait()
                    game_mode_selection(3)
                elif pygame.mouse.get_pressed()[0] and option == "4x4":
                    pygame.event.wait()
                    game_mode_selection(4)
                elif pygame.mouse.get_pressed()[0] and option == "5x5":
                    pygame.event.wait()
                    game_mode_selection(5)   
            else:
                draw_text(option, FONT, WHITE, WINDOW, menu_y_position)

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