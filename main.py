import draw
import logic
import math
import pygame
# Initialize Pygame
draw.pygame.init()
print
# Set up display
def main():
    # Initialize Pygame
    pygame.init()

    # Initialize the board state
    board = logic.Board()



    # Main game loop
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

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()


    
