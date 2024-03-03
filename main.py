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
                if (board.selected_piece==None):
                    x, y = event.pos
                    selpiece = board.get_piece_at_position((x, y))
                    
                    if(selpiece==None or selpiece.color==board.current_player):
                        print(selpiece)
                        print(board.get_gameposition_at_position((x, y)))
                        print("error sel piece")
                    else:
                        board.selected_piece =selpiece
                else:
                    x, y = event.pos
                    destination = board.get_piece_at_position((x, y))
                    if(destination == board.selected_piece):
                        board.selected_piece = None
                    elif(board.selected_piece!=None):
                        print(board.get_gameposition_at_position((x, y)))
                        print("\n\n\n")
                        board.move_piece(board.get_gameposition_at_position((x, y)))
                    elif(destination==None):
                        print("error destination")
                    

                pass

        
        
        board.draw()
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()


    
