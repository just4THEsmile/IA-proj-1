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

def game_pvb(botcolor, size=5, difficulty=1):
    board = logic.Board(size)
    minimax_depth = difficulty

    running = True
    while running:
        if board.check_win_conditions():
            running = False   
        elif board.current_player == botcolor:
            move = board.find_best_move(minimax_depth)
            if move:
                board.play_best_move()
                board.current_player = draw.RED if board.current_player == draw.BLUE else draw.BLUE    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and board.current_player != botcolor:
                x, y = event.pos
                selected_piece = board.get_piece_at_position((x, y))
                
                if selected_piece and selected_piece.color == board.current_player:
                    board.selected_piece = selected_piece
                else:
                    game_position = board.get_gameposition_at_position((x, y))
                    if board.selected_piece:
                        board.move_piece(game_position)

        board.check_blocked()
        board.draw()
        pygame.display.flip()

    pygame.quit()

    # Quit Pygame
