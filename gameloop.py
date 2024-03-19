import main 
import draw
import logic
import math
import pygame
   # Initialize the board state



def game_pvp(size):    
    board = logic.Board(size)
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif board.check_win_conditions():
                running = False    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (board.selected_piece==None):
                    x, y = event.pos
                    selpiece = board.get_piece_at_position((x, y))
                    
                    if(selpiece==None or selpiece.color!=board.current_player):
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

        
        board.check_blocked()
        board.draw()
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

def game_pvb(botcolor,size=5,dificulty=1):
    board = logic.Board(size)
    # Main game loop
    running = True

    ## test performance
    
    while running:
        if board.check_win_conditions():
            running = False   
        elif board.current_player == botcolor:
            board.play_best_move(dificulty)
            if board.current_player==draw.RED:
                board.current_player=draw.BLUE
            else:   
                board.current_player=draw.RED    
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif board.check_win_conditions():
                print("WINEER",board.get_winner())
                running = False    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (board.selected_piece==None):
                    x, y = event.pos
                    selpiece = board.get_piece_at_position((x, y))
                    
                    if(selpiece==None or selpiece.color!=board.current_player):
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

        
        board.check_blocked()
        board.draw()
        pygame.display.flip()

    # Quit Pygame
