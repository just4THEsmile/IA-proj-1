import math
import draw

class Stone:
    def __init__(self, color, position,blocked=False):
        self.color = color
        self.position = position
        self.blocked = blocked

    def draw(self):
        # Draw stone on the board
        x, y = self.position
        if self.blocked==True:
            draw.draw_hexagon(x, y, draw.hex_size, self.color)
            draw.draw_circle(x, y, draw.hex_size, draw.BLACK)
            
        else:    
            draw.draw_hexagon(x, y, draw.hex_size, self.color)
    
class Finish_line:
    def __init__(self, color, position):
        self.color = color
        self.position = position
    def draw(self):
        # Draw finish line on the board
        x, y = self.position
        draw.draw_hexagon(x, y, draw.hex_size, draw.BLACK)
        draw.draw_circle(x, y, draw.hex_size, self.color)

class Board:
    def __init__(self):
        self.board = initialize_board()
        self.current_player = draw.BLUE
        self.selected_piece = None

    def move_piece(self, destination):
        """
        Move a piece to the specified destination if the move is valid.
        """
        if self.selected_piece and is_valid_move(self.board, self.selected_piece, destination):
            self.board[destination] = self.selected_piece
            del self.board[self.selected_piece.position]
            self.selected_piece.position = destination
            self.check_and_block_stones()
            self.selected_piece = None
            self.current_player = draw.RED if self.current_player == draw.BLUE else draw.BLUE

    def is_valid_move(self, stone, destination):
        """
        Check if a move is valid.
        """
        # Implement move validation logic here
        pass

    def check_and_block_stones(self):
        """
        Check for blocked stones and update their status.
        """
        # Implement logic to check for blocked stones and update their status
        pass

    def check_win_conditions(self):
        """
        Check win conditions to determine if a player has won or if the game has ended in a stalemate.
        """
        # Implement win condition checking logic
        pass

    def get_piece_at_position(self, position):
        """
        Get the piece at the given position on the board.
        """
        for piece in self.board.values():
            if math.hypot(piece.position[0] - position[0], piece.position[1] - position[1]) < draw.hex_size:
                return piece
        return None

    def draw(self):
        """
        Draw the hexagonal board grid.
        """
        draw.WINDOW.fill(draw.WHITE)
        for position, stone in self.board.items():
            if stone:
                stone.draw()
            else:
                x, y = position
                draw.draw_hexagon(x, y, draw.hex_size, draw.BLACK)

def get_col_number(row):
    if row<5:
        return row+5
    else:
        return 13-row
def initialize_board():
    """
    Initialize the board state with stones placed according to the game rules.
    """
    board = {}
    for row in range(9):
        for col in range(get_col_number(row)):
            x = col * draw.horizontal_distance + (draw.WIDTH - get_col_number(row) * draw.horizontal_distance) / 2

            y = row * draw.vertical_distance + (draw.HEIGHT - 9 * draw.vertical_distance) / 2
            position = (x, y)
            if row ==4:
                if col == 0:
                    board[position] = Finish_line(draw.RED, position)
                elif col == get_col_number(row) - 1:
                    board[position] = Finish_line(draw.BLUE, position)
                elif col == 1:
                    board[position] = Stone(draw.BLUE, position)
                elif col == get_col_number(row) - 2:
                    board[position] = Stone(draw.RED, position)
                else:
                    board[position] = None        
            elif col == 0:
                board[position] = Stone(draw.BLUE, position)
            elif col == get_col_number(row) - 1:
                board[position] = Stone(draw.RED, position)
            else:
                board[position] = None
    return board

def move_stone(board, stone, destination):
    """
    Move a stone to the specified destination if the move is valid.
    """
    if is_valid_move(board, stone, destination):
        board[destination] = stone
        del board[stone.position]
        stone.position = destination
        check_and_block_stones(board)

def is_valid_move(board, stone, destination):
    """
    Check if a move is valid.
    """
    # Implement move validation logic here
    pass

def check_and_block_stones(board):
    """
    Check for blocked stones and update their status.
    """
    # Implement logic to check for blocked stones and update their status
    pass

def check_win_conditions(board):
    """
    Check win conditions to determine if a player has won or if the game has ended in a stalemate.
    """
    # Implement win condition checking logic
    pass

def get_piece_at_position(board, position):
    """
    Get the piece at the given position on the board.
    """
    for piece in board.values():
        if math.hypot(piece.position[0] - position[0], piece.position[1] - position[1]) < draw.hex_size:
            return piece
    return None