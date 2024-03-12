import math
import draw
import copy
import time

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
    def __init__(self,sizeofside=5):
        self.current_player = draw.BLUE
        self.selected_piece = None
        self.blocked_Red = 0
        self.blocked_Blue = 0
        (self.red_pieces, self.blue_pieces,self.finish_lines) = initialize_board()
        self.size=sizeofside

    def draw(self):
        draw.WINDOW.fill(draw.WHITE)
        for row in range((self.size*2-1)):
            for col in range(get_col_number(row)):
                x = col * draw.horizontal_distance + (draw.WIDTH - get_col_number(row) * draw.horizontal_distance) / 2
                y = row * draw.vertical_distance + (draw.HEIGHT - 9 * draw.vertical_distance) / 2
                draw.draw_hexagon(x, y, draw.hex_size, draw.BLACK)
        for pieces in self.red_pieces+self.blue_pieces:
            pieces.draw()    
        for finish in self.finish_lines:
            finish.draw()
        if(self.selected_piece!=None):
            x, y = self.selected_piece.position
            draw.draw_hexagon_border(x, y, draw.hex_size, draw.YELLOW,2)    

    def has_friendly_neighbours(self,piece,color):
        if color==draw.BLUE:
            for piece2 in self.blue_pieces:
                if is_neighbour(self,piece,piece2,self.size):
                    return True
            return False
        else:
            for piece2 in self.red_pieces:
                if is_neighbour(self,piece,piece2,self.size):
                    return True
            return False
    
    def get_neighbouring_possibilities(self,piece,color):    
        (fromx,fromy,fromz)=coord_to_cube(piece.gameposition)
        possibilities=[]
        #get opponent color
        if color==draw.BLUE:
            opponent=draw.RED
        else:
            opponent=draw.BLUE    
        #calculates every move in the 6 directions
        
        for var in range(1,8):
            if self.can_move(piece.gameposition,cube_to_coord((fromx+var,fromy-var,fromz)),color,self.size):
                possibilities.append((piece.gameposition,cube_to_coord((fromx+var,fromy-var,fromz))))
                break
        for var in range(1,8):
            if self.can_move(piece.gameposition,cube_to_coord((fromx-var,fromy+var,fromz)),color,self.size):
                possibilities.append((piece.gameposition,cube_to_coord((fromx-var,fromy+var,fromz))))
                break
        for var in range(1,8):
            if self.can_move(piece.gameposition,cube_to_coord((fromx,fromy+var,fromz-var)),color,self.size):
                possibilities.append((piece.gameposition,cube_to_coord((fromx,fromy+var,fromz-var))))
                break    
        for var in range(1,8):
            if self.can_move(piece.gameposition,cube_to_coord((fromx,fromy-var,fromz+var)),color,self.size):
                possibilities.append((piece.gameposition,cube_to_coord((fromx,fromy-var,fromz+var))))
                break    
        for var in range(1,8):
            if self.can_move(piece.gameposition,cube_to_coord((fromx+var,fromy,fromz-var)),color,self.size):
                possibilities.append((piece.gameposition,cube_to_coord((fromx+var,fromy,fromz-var))))
                break
        for var in range(1,8):
            if self.can_move(piece.gameposition,cube_to_coord((fromx-var,fromy,fromz+var)),color,self.size):
                possibilities.append((piece.gameposition,cube_to_coord((fromx-var,fromy,fromz+var))))
                break  
        return possibilities   

                

    def get_possible_moves(self,color):
        moves=[]
        if color==draw.BLUE:
            for piece in self.blue_pieces:
                if piece.blocked==False:
                    moves.extend(self.get_neighbouring_possibilities(piece,color))
        else:
            for piece in self.red_pieces:
                if piece.blocked==False:
                    moves.extend(self.get_neighbouring_possibilities(piece,color))
        return moves 
    
    
    def avail_board(self,color):
        value=0
        if color==draw.RED:
            value=100*(len(self.red_pieces) -len(self.blue_pieces))
            value+=50*(self.blocked_Blue - self.blocked_Red) 
            for piece in self.red_pieces:
                if piece.gameposition[0]==4 and  piece.gameposition[1]==0:
                    return float('inf')
                value -= get_pieces_distance(piece,self.finish_lines[0])
                if self.has_friendly_neighbours(piece,draw.RED):
                    value+=20
            for piece in self.blue_pieces:
                if piece.gameposition[0]==4 and  piece.gameposition[1]==8:
                    return float('inf')
                value += get_pieces_distance(piece,self.finish_lines[1])
                if self.has_friendly_neighbours(piece,draw.BLUE):
                    value-=20
            if len(self.red_pieces)==0 or self.blocked_Red==len(self.red_pieces):
                return  float('-inf')
            elif len(self.blue_pieces)==0 or self.blocked_Blue==len(self.blue_pieces):
                return float('inf')            

        else:
            value=100*(len(self.blue_pieces) -len(self.red_pieces))
            value+=50*(self.blocked_Red - self.blocked_Blue)
            for piece in self.blue_pieces:
                if piece.gameposition[0]==4 and  piece.gameposition[1]==8:
                    return  float('inf')
                value -= get_pieces_distance(piece,self.finish_lines[0])
                if self.has_friendly_neighbours(piece,draw.BLUE):
                    value+=20
            for piece in self.red_pieces:
                if piece.gameposition[0]==4 and  piece.gameposition[1]==0:
                    return float('inf')
                value += get_pieces_distance(piece,self.finish_lines[1])   
                if self.has_friendly_neighbours(piece,draw.RED):
                    value-=20
            if len(self.red_pieces)==0 or self.blocked_Red==len(self.red_pieces):
                return  float('inf')
            elif len(self.blue_pieces)==0 or self.blocked_Blue==len(self.blue_pieces):
                return float('-inf')     
        return value
    
    
    def minimax(self,beta,alpha,depth,player,maximaxing):
        if depth==0 or self.check_win_conditions():
            return self.avail_board(player)
        
        if maximaxing:
            max_aval = float('-inf')
            for move in self.get_possible_moves(player):
                new_board = copy.deepcopy(self)
                new_board.change_piece_position(move[0],move[1])
                aval= new_board.minimax(beta,alpha,depth-1,player,False)
                max_aval = max(max_aval,aval)
                alpha = max(alpha, aval)
                if beta <= alpha:
                    break
                
            return max_aval
        else:
            min_aval = float('inf')
            for move in self.get_possible_moves(player):
                new_board = copy.deepcopy(self)
                new_board.change_piece_position(move[0],move[1])
                aval= new_board.minimax(beta,alpha,depth-1,player,True)
                min_aval = min(min_aval,aval)
                beta = min(beta, aval)
                if beta <= alpha:
                    break 
                
            return min_aval
        
    def find_best_move(self, depth):    
        print(len(self.red_pieces))
        print(self.blocked_Red)
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        print("possible moves",self.get_possible_moves(self.current_player))
        for move in self.get_possible_moves(self.current_player):
            new_board = copy.deepcopy(self)
            new_board.change_piece_position(move[0],move[1])
            eval = new_board.minimax(beta,alpha,depth, self.current_player,False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        print("score",max_eval)        
        return best_move

    def play_best_move(self):
        time1 = time.time()
        move = self.find_best_move(2)
        time2 = time.time()
        delta= time2-time1
        print("Time to calculate the best move: ",delta)
        print("Best move: ",move)
        self.change_piece_position(move[0],move[1])


    #checks if the position has a piece
    def check_pos(self,pos):
        if pos[0]<0 or pos[0]>8 or pos[1]<0 or pos[1]>=get_col_number(pos[0]):
            return False
        else:
            for piece in self.blue_pieces+self.red_pieces:
                if piece.gameposition==pos:
                    return piece
        return None
    
    #checks if the position has a piece of the color
    def check_pos_color(self,pos,color):
        if pos[0]<0 or pos[0]>8 or pos[1]<0 or pos[1]>=get_col_number(pos[0]):
            return False
        else:
            if color==draw.BLUE:
                for piece in self.blue_pieces:
                    if piece.gameposition==pos:
                        return True
            else:
                for piece in self.red_pieces:
                    if piece.gameposition==pos:
                        return True        
        return False
    
    def check_bounds(self,pos):
        if pos[0]<0 or pos[0]>(self.size*2-1) or pos[1]<0 or pos[1]>=get_col_number(pos[0]):
            return False
        return True
    
    def check_can_move_finishing_line(self,pos,color):
        if pos[0]==4:
            if pos[1]==0 and color==draw.BLUE:
                return False
            elif pos[1]==get_col_number(4)-1 and color==draw.RED:
                return False
            
        return True
    def remove_piece(self,pos):

        for piece in self.red_pieces:
            if piece.gameposition==pos:
                self.red_pieces.remove(piece)

        for piece in self.blue_pieces:
            if piece.gameposition==pos:
                self.blue_pieces.remove(piece)
                  

    def change_piece_position(self,start,destination):
        for piece in self.red_pieces:
            if destination==piece.gameposition:
                self.red_pieces.remove(piece)
                break
        for piece in self.blue_pieces:
            if destination==piece.gameposition:
                self.blue_pieces.remove(piece)
                break        
        piece=self.check_pos(start)
        if type(piece)!=Stone:
            print("error changing position")
            print(start,destination)
            return False
        piece.gameposition=destination
        piece.position=self.get_position_from_gameposition(destination)

    def check_blocked(self):
        self.blocked_Blue=0
        self.blocked_Red=0
        for piece in self.red_pieces:
            piece.blocked=False
        for piece in self.blue_pieces:
            piece.blocked=False    

        for piece in self.red_pieces:
            for piece2 in self.blue_pieces:
                (fromx,fromy,fromz)=coord_to_cube(piece.gameposition)

                (tox,toy,toz)=coord_to_cube(piece2.gameposition)
                dx = tox - fromx
                dy = toy - fromy
                dz = toz - fromz
                if(dx==0 or dy==0 or dz==0):
                    if(dx==1 or dy==1 or dz==1):
                        if piece.blocked==False:
                            piece.blocked=True
                            self.blocked_Red+=1
                        if piece2.blocked==False:
                            piece2.blocked=True
                            self.blocked_Blue+=1    

    def can_move(self,from_pos,to_pos,color,sizeofside=5):
        (fromx,fromy,fromz)=coord_to_cube(from_pos)

        (tox,toy,toz)=coord_to_cube(to_pos)
        dx = tox - fromx
        dy = toy - fromy
        dz = toz - fromz
        realsize=sizeofside-1
        #getopponent color
        if color==draw.BLUE:
            opponent=draw.RED
            if to_pos[0]==4 and to_pos[1]==0:
                return False
        else:
            opponent=draw.BLUE
            if to_pos[0]==4 and to_pos[1]==get_col_number(4)-1:
                return False
        check= self.check_pos(cube_to_coord((tox,toy,toz)))    
        if check==None:  
            pass
        elif check==False:
            return False
        elif check.color==opponent:
            pass
        else:
            return False
        #check if the move is in line
        if(dx==0 or dy==0 or dz==0):
            #single distance movement
            if(dx==1 or dy==1 or dz==1):
                if self.check_pos(cube_to_coord((tox,toy,toz)))==None:

                    return True
                return False
            else:
                if(dx>0):
                    xrange=range(fromx,tox)
                else:
                    xrange=range(fromx,tox,-1)
                if dy>0:
                    yrange=range(fromy,toy)
                else:
                    yrange=range(fromy,toy,-1)    
                if dz>0:
                    zrange=range(fromz,toz)
                else:
                    zrange=range(fromz,toz,-1)    

                if dx==0:
                    for i in range(1,abs(dy)):
                        if self.check_pos_color(cube_to_coord((fromx,yrange[i],zrange[i])),color)==False:
                            return False
                    return True    
                elif dy==0:
                    for i in range(1,abs(dx)):
                        if self.check_pos_color(cube_to_coord((xrange[i],fromy,zrange[i])),color)==False:
                            return False
                    return True
                elif dz==0:
                    for i in range(1,abs(dx)):
                        if self.check_pos_color(cube_to_coord((xrange[i],yrange[i],fromz)),color)==False:
                            return False
                    return True
        return False    
                    
    


    def move_piece(self, destination):
        """
        Move a piece to the specified destination if the move is valid.
        """
        print("movement")
        if self.check_pos_color(destination,self.selected_piece.color)==True or self.check_bounds(destination)==False or self.check_can_move_finishing_line(destination,self.selected_piece.color)==False:
            return False
        print(self.check_can_move_finishing_line(destination,self.selected_piece.color))
        print(self.get_possible_moves(self.selected_piece.color))
        if self.selected_piece and self.can_move(self.selected_piece.gameposition,destination,self.selected_piece.color) and self.selected_piece.blocked==False:
            print("valid move")
            piece=self.check_pos(destination)
            if piece!=None :
                print("removing")
                self.remove_piece(destination)
            print(self.selected_piece.gameposition)    
            self.change_piece_position(self.selected_piece.gameposition,destination)
            print(self.selected_piece.gameposition)    
            """
            self.board[destination] = self.selected_piece
            self.board[self.selected_piece.gameposition] = None
            self.board[destination].gameposition = destination
            self.board[destination].position = self.get_position_from_gameposition(destination)"""
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



    def check_win_conditions(self):
        """
        Check win conditions to determine if a player has won or if the game has ended in a stalemate.
        """
        if self.check_pos_color((4,0),draw.RED)==True:
            print("Red wins")
            return True
        elif self.check_pos_color((4,get_col_number(4)-1),draw.BLUE)==True:
            print("Blue wins")
            return True
        elif len(self.red_pieces)==self.blocked_Red:
            print("Blue wins")
            return True
        elif len(self.blue_pieces)==self.blocked_Blue:
            print("Red wins")
            return True 
        return False
    
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
        for piece in self.blue_pieces+self.red_pieces:
            
            if math.hypot(piece.position[0] - position[0], piece.position[1] - position[1]) < draw.hex_size:
                print(piece.position,piece.gameposition)
                return piece
        return None
    
    def get_position_from_gameposition(self,gameposition):
        row, col = gameposition
        x = col * draw.horizontal_distance + (draw.WIDTH - get_col_number(row) * draw.horizontal_distance) / 2
        y = row * draw.vertical_distance + (draw.HEIGHT - 9 * draw.vertical_distance) / 2
        return (x,y)
    


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
    red_pieces=[]
    blue_pieces=[]
    Finish_lines=[]
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
                    Finish_lines.append(Finish_line(draw.RED,gameposition, position))
                elif col == get_col_number(row) - 1:
                    board[gameposition] = Finish_line(draw.BLUE, gameposition,position)
                    Finish_lines.append(Finish_line(draw.BLUE,gameposition, position))
                elif col == 1:
                    board[gameposition] = Stone(draw.BLUE, gameposition,position)
                    blue_pieces.append(Stone(draw.BLUE, gameposition,position))
                elif col == get_col_number(row) - 2:
                    board[gameposition] = Stone(draw.RED, gameposition,position)
                    red_pieces.append(Stone(draw.RED, gameposition,position))
                else:
                    board[gameposition] = None        
            elif col == 0:
                board[gameposition] = Stone(draw.BLUE, gameposition,position)
                blue_pieces.append(Stone(draw.BLUE, gameposition,position))
            elif col == get_col_number(row) - 1:
                board[gameposition] = Stone(draw.RED, gameposition,position)
                red_pieces.append(Stone(draw.RED, gameposition,position))
            else:
                board[gameposition] = None
    return (red_pieces,blue_pieces,Finish_lines)





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




def coord_to_cube(pos,sizeofside=5):
    (x,y)=pos
    realsize=sizeofside-1
    yy=x-realsize
    if x<=realsize:
        xx=y-x
        zz=-xx-yy
    else:
        xx=y-realsize
        zz=-xx-yy




    return (xx, yy, zz)

def cube_to_coord(cube,sizeofside=5):
    (x,y,z)=cube
    realsize=sizeofside-1
    if y<0:
        xx=y+realsize
        yy=xx+x
    else:
        xx=y+realsize
        yy=realsize+x

    return (xx,yy)

def get_pieces_distance(piece1,piece2):
    (fromx,fromy,fromz)=coord_to_cube(piece1.gameposition)
    (tox,toy,toz)=coord_to_cube(piece2.gameposition)
    return (abs(fromx-tox)+abs(fromy-toy)+abs(fromz-toz))/2
