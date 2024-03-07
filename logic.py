import math
import draw

class Stone:
    def __init__(self, color, gameposition,position,blocked=False):
        self.color = color
        self.position = position
        self.blocked = blocked
        self.gameposition= gameposition

    def draw(self):
        # Draw stone on the board
        x, y = self.position
        if self.blocked==True:
            draw.draw_hexagon(x, y, draw.hex_size, self.color)
            draw.draw_circle(x, y, draw.hex_size, draw.BLACK)
            
        else:    
            draw.draw_hexagon(x, y, draw.hex_size, self.color)
    
class Finish_line:
    def __init__(self, color, gameposition,position):
        self.color = color
        self.position = position
        self.gameposition= gameposition
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
        print("movement")
        print(is_line_of_color(self.board,self.selected_piece.gameposition,destination,self.selected_piece.color))
        print(self.selected_piece.blocked==False)
        if self.selected_piece and is_valid_move(self.board, self.selected_piece, destination) and self.selected_piece.blocked==False:
            self.board[destination] = self.selected_piece
            self.board[self.selected_piece.gameposition] = None
            self.selected_piece.gameposition = destination
            self.selected_piece.position = self.get_position_from_gameposition(destination)
            self.selected_piece = None
            self.current_player = draw.RED if self.current_player == draw.BLUE else draw.BLUE

        elif self.selected_piece and is_line_of_color(self.board,self.selected_piece.gameposition,destination,self.selected_piece.color) and is_straight_line(self.selected_piece.gameposition,destination ) and self.selected_piece.blocked==False:
            print("jumping")
            if check_piece_color(self.board,destination,self.selected_piece.color)==False:
                if self.board[destination]!=None:
                    self.board[destination] = self.selected_piece
                    self.board[self.selected_piece.gameposition] = None
                    self.selected_piece.gameposition = destination
                    self.selected_piece.position = self.get_position_from_gameposition(destination)
                    self.selected_piece = None
                    self.current_player = draw.RED if self.current_player == draw.BLUE else draw.BLUE
                
        else:
            print("Invalid move")

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
    def get_gameposition_at_position(self, position):
        x = position[0]
        y = position[1]

        row = (y - (draw.HEIGHT - 9 * draw.vertical_distance) / 2) / draw.vertical_distance
        col = (x - (draw.WIDTH - get_col_number(round(row)) * draw.horizontal_distance) / 2) / draw.horizontal_distance

        return (round(row), round(col))

    def get_piece_at_position(self, position):
        """
        Get the piece at the given position on the board.
        """
        for piece in self.board.values():
            if(piece==None):
                continue
            
            elif math.hypot(piece.position[0] - position[0], piece.position[1] - position[1]) < draw.hex_size:
                print(piece.position,piece.gameposition)
                return piece
        return None
    
    def get_position_from_gameposition(self,gameposition):
        row, col = gameposition
        x = col * draw.horizontal_distance + (draw.WIDTH - get_col_number(row) * draw.horizontal_distance) / 2
        y = row * draw.vertical_distance + (draw.HEIGHT - 9 * draw.vertical_distance) / 2
        return (x,y)
    

    def draw(self):
        """
        Draw the hexagonal board grid.
        """
        draw.WINDOW.fill(draw.WHITE)
        for row in range(9):
            for col in range(get_col_number(row)):
                x = col * draw.horizontal_distance + (draw.WIDTH - get_col_number(row) * draw.horizontal_distance) / 2
                y = row * draw.vertical_distance + (draw.HEIGHT - 9 * draw.vertical_distance) / 2
                draw.draw_hexagon(x, y, draw.hex_size, draw.BLACK)
        for position, stone in self.board.items():
            if stone:

                stone.draw()
        if(self.selected_piece!=None):
            x, y = self.selected_piece.position
            draw.draw_hexagon_border(x, y, draw.hex_size, draw.YELLOW,2)

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
    print(type(board))
    for row in range(9):
        for col in range(get_col_number(row)):
            x = col * draw.horizontal_distance + (draw.WIDTH - get_col_number(row) * draw.horizontal_distance) / 2

            y = row * draw.vertical_distance + (draw.HEIGHT - 9 * draw.vertical_distance) / 2
            gameposition = (row, col)
            position = (x, y)
            if row ==4:
                if col == 0:
                    board[gameposition] = Finish_line(draw.RED,gameposition, position)
                elif col == get_col_number(row) - 1:
                    board[gameposition] = Finish_line(draw.BLUE, gameposition,position)
                elif col == 1:
                    board[gameposition] = Stone(draw.BLUE, gameposition,position)
                elif col == get_col_number(row) - 2:
                    board[gameposition] = Stone(draw.RED, gameposition,position)
                else:
                    board[gameposition] = None        
            elif col == 0:
                board[gameposition] = Stone(draw.BLUE, gameposition,position)
            elif col == get_col_number(row) - 1:
                board[gameposition] = Stone(draw.RED, gameposition,position)
            else:
                board[gameposition] = None
    return board



def is_valid_move(board, stone, destination,sizeofside=5):
    (fromx,fromy)=stone.gameposition
    (tox,toy)=destination
    print(get_col_number(tox))
    if(tox<0 or tox>8 or toy<0 or toy>=get_col_number(tox)):
        return False
    if(board[destination]!=None):
        return False
    print((fromx,fromy),"to",(tox,toy))
    print(oddr_to_cube((fromx,fromy)),"to",oddr_to_cube((tox,toy)))
    """
    print(is_straight_line((fromx,fromy),(tox,toy)))
    print("line")
    print(is_line_of_color(board,(fromx,fromy),(tox,toy),stone.color))"""

    dx = tox - fromx
    dy = toy - fromy
    #same row
    if fromx==tox:
        return abs(dy)==1
    else:
        if fromx <=(sizeofside-1) and tox<=(sizeofside-1):
            return (dy==0 and abs(dx)==1) or (dy==1 and dx==1) or (dy==-1 and dx==-1)
        elif fromx >(sizeofside-1) and tox>(sizeofside-1):
            return (dy==0 and abs(dx)==1) or (dy==1 and dx==-1) or (dy==-1 and dx==1)
        else:
            if(fromx<tox):
                print("here")
                print(dy,dx)
                return (dy==0 and abs(dx)==1) or (dy==-1 and dx==1)
            else:
                return (dy==0 and abs(dx)==1) or (dy==1 and dx==-1)


def can_move_piece(board, stone, destination,sizeofside=5):
    print(stone)
    print("\n")
    print(destination)
    (fromx,fromy)=stone.gameposition
    (tox,toy)=destination.gameposition
    dx = fromx - tox
    dy = fromy - toy
    #same row
    if fromx==tox:
        return True;
    else:
        if fromx <=sizeofside and tox<=sizeofside:
            if(dy==0):
                for i in range(1,abs(dx)):
                    if(board.get_piece_at_position):
                        return False
        


def is_neighbour(board,stone1,stone2,sizeofside=5):
    (fromx,fromy)=stone1.gameposition
    (tox,toy)=stone2.gameposition

    dx = fromx - tox
    dy = fromy - toy
    #same row
    if fromx==tox:
        return dy==1
    else:
        if fromx <=sizeofside and tox<=sizeofside:
            return (dy==0 and abs(dx)==1) or (dy==1 and dx==1) or (dy==-1 and dx==-1)
        elif fromx >sizeofside and tox>sizeofside:
            return (dy==0 and abs(dx)==1) or (dy==1 and dx==-1) or (dy==-1 and dx==1)
        else:   
            if(fromx<tox):
                return (dy==0 and abs(dx)==1) or (dy==-1 and dx==1)
            else:
                return (dy==0 and abs(dx)==1) or (dy==1 and dx==-1)

            



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
    print("jvhwg\n\n\n\n")
    for piece in board.values():

        if math.hypot(piece.position[0] - position[0], piece.position[1] - position[1]) < draw.hex_size:
            return piece
    return None


def oddr_to_cube(hex):
    """
    Convert from "odd-r" offset coordinates to cube coordinates.
    hex is a tuple representing the offset coordinates of the hexagon.
    """
    x = hex[1] - (hex[0] - (hex[0] & 1)) // 2
    z = hex[0]
    y = -x - z
    return (x, y, z)

def cube_to_oddr(cube):
    """
    Convert from cube coordinates to "odd-r" offset coordinates.
    cube is a tuple representing the cube coordinates of the hexagon.
    """
    col = cube[0] + (cube[2] - (cube[2] & 1)) // 2
    row = cube[2]
    return (row, col)


def is_straight_line(pos1, pos2,sizeofside=5):
    """
    Check if two positions form a straight line in a hexagonal grid.
    pos1 and pos2 are tuples representing the axial coordinates of the positions.
    """
    # Convert the axial coordinates to cube coordinates
    (fromx,fromy)=pos1
    (tox,toy)=pos2
    realsize=sizeofside-1
    dx = tox - fromx
    dy = toy - fromy
    #same row
    if fromx==tox:
        return True
    else:
        if fromx <=(sizeofside-1) and tox<=(sizeofside-1):
            return (dy==0) or (dy==dx)
        elif fromx >(sizeofside-1) and tox>(sizeofside-1):
            return (dy==0) or (dy==-dx)
        else:
            if(fromx<tox):
                print("here")
                print(dy,dx)
                return (dy==(realsize-fromx)) or (dy==-(tox-realsize))
            else:
                print("ffhere")
                print(dy,dx)
                print(str(fromy-realsize))
                return (dy==-(realsize-tox)) or (dy==(fromx-realsize))

def is_valid_piece(board,pos,sizeofside=5):
    (x,y)=pos
    if x<0 or x>=9:
        return False
    if y<0 or y>=get_col_number(x):
        return False
    if board[(x,y)]==None:
        return False
    return True

def check_piece_color(board,pos,color):
    if is_valid_piece(board,pos):
        return board[pos].color==color
    return False

def is_line_of_color(board, pos1, pos2, color,sizeofside=5):
        # Convert the axial coordinates to cube coordinates
    (fromx,fromy)=pos1
    (tox,toy)=pos2
    realsize=sizeofside-1
    dx = tox - fromx
    dy = toy - fromy
    #same row
    if fromx==tox:
        val1=True
        val2=True
        for i in range(1,abs(dy)):
            if check_piece_color(board,(fromx,fromy+i),color)==False:
                val1=False

            if check_piece_color(board,(fromx,fromy-i),color)==False:
                val2=False

        return val1 or val2
    else:
        if fromx <=(sizeofside-1) and tox<=(sizeofside-1):
            val1=True
            val2=True
            val3=True
            val4=True
            for i in range(1,abs(dx)):
                if check_piece_color(board,(fromx+i,fromy+i),color)==False:
                    val1=False

                if check_piece_color(board,(fromx-i,fromy-i),color)==False:
                    val2=False    
   
                if check_piece_color(board,(fromx+i,fromy),color)==False:
                    val3=False    

                if check_piece_color(board,(fromx-i,fromy),color)==False:
                    val4=False
            print (val1 , val2 , val3 , val4)
            return val1 or val2 or val3 or val4   
            #return (dy==0) or (dy==dx)
        elif fromx >(sizeofside-1) and tox>(sizeofside-1):
            val1=True
            val2=True
            val3=True
            val4=True
            for i in range(1,abs(dx)):
                if check_piece_color(board,(fromx+i,fromy),color)==False:
                    val1=False

                if check_piece_color(board,(fromx-i,fromy),color)==False:
                    val2=False
  
                if check_piece_color(board,(fromx+i,fromy-i),color)==False:
                    val3=False

                if check_piece_color(board,(fromx-i,fromy+i),color)==False:
                    val4=False

            print (val1 , val2 , val3 , val4)
            return val1 or val2 or val3 or val4
            #return (dy==0) or (dy==-dx)
        else:
            if(fromx<tox):
                print("here")
                print(dy,dx)
                val1=True
                val2=True
                for i in range(1,abs(dx)):
                    if fromx+i<=realsize:
                        if check_piece_color(board,(fromx+i,fromy+i),color)==False:
                            val1=False

                        if check_piece_color(board,(fromx+i,fromy),color)==False:
                            val2=False

                    else:
                        if check_piece_color(board,(fromx+i,fromy+(realsize-fromx)),color)==False:
                            val1=False

                        if check_piece_color(board,(fromx-i,fromy-(fromx+i-realsize)),color)==False:  
                            val2=False  
 
                print (val1 , val2)             
                return val1 or val2    
                #return (dy==(realsize-fromx)) or (dy==-(tox-realsize))
            else:
                print("ffhere")
                print(dy,dx)
                print(str(fromy-realsize))
                val1=True
                val2=True
                for i in range(1,abs(dx)):
                    if fromx-i>=realsize:
                        if check_piece_color(board,(fromx-i,fromy),color)==False: 
                            val1=False

                        if check_piece_color(board,(fromx-i,fromy+i),color)==False:
                            val2=False

                    else:
                        if check_piece_color(board,(fromx-i,fromy-(i+fromx-realsize)),color)==False:
                            val1=False

                        if check_piece_color(board,(fromx-i,fromy+(fromx-realsize)),color)==False:
                            val2=False    

                print (val1 , val2)            
                return val1 or val2           
      
                #return (dy==-(realsize-tox)) or (dy==(fromx-realsize))


def axial_to_cube(pos):
    """
    Convert axial coordinates to cube coordinates.
    pos is a tuple representing the axial coordinates of the position.
    """
    x = pos[0]
    y = pos[1] - (pos[0] // 2)
    z = -x - y
    return (x, y, z)