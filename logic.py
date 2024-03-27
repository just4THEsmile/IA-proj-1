import math
import draw
import copy
import time
import numpy
import threading
import random
class Node:
    def __init__(self,board, move=None, parent=None):
        self.board = board  # Board state
        self.move = move  # Move that led to this node
        self.parent = parent  # Parent node
        self.children = []  # Child nodes
        self.visits = 0  # Number of times this node has been visited
        self.score = 0  # Accumulated score for this node

def monte_carlo_search(board, num_simulations):
    root = Node(board)
    start_time = time.time()
    timeout = num_simulations / 30
    print("timeout",timeout)

    while time.time() - start_time < timeout and root.visits < num_simulations:

        node = root
        moves = node.board.get_possible_moves(node.board.current_player)
        # Selection phase
        while len(node.children) == len(moves) and len(moves) > 0:
            node = select_child(node)
            if node is None:
                break
            moves = node.board.get_possible_moves(node.board.current_player)
        
        # Expansion phase
        if not node.board.check_win_conditions():  # Expand only if the node is not a end state
            moves = node.board.get_possible_moves(node.board.current_player)
            if len(moves)>0:
                new_moves=[move for move in moves if (move not in [child.move for child in node.children] )]
                move = random.choice(new_moves)
                new_board = copy.deepcopy(node.board)
                new_board.change_piece_position(move.start, move.destiny)
                new_board.check_blocked()
                new_board.current_player = draw.RED if new_board.current_player == draw.BLUE else draw.BLUE
                new_node = Node(new_board,move, node)
                node.children.append(new_node)
                node = new_node
        
            # Simulation phase
            result = simulate_random_game(copy.deepcopy(node.board),1000)
            # Backpropagation phase
            while node:
                node.visits += 1
                if result == board.current_player:
                    node.score += 1
                elif not (result is None):
                    node.score -= 1  # LOSS    
                    pass
                node = node.parent
    # Select the move with the highest average score
    best_move = select_best_move(root)
    return best_move


def select_child(node):
    possible_moves = node.board.get_possible_moves(node.board.current_player)
    # Check if all children have been visited
    if len(node.children) == len(possible_moves):
        # If all children have been visited, select the child with the highest UCB score
        best_ucb = float("-inf")
        selected_child = None
        for child in node.children:
            ucb = (child.score / child.visits) + math.sqrt(2 * math.log(node.visits) / child.visits)
            if ucb > best_ucb:
                best_ucb = ucb
                selected_child = child
        if selected_child==None:
            return node
        return selected_child  # If no child with valid UCB score is found, return the current node itself

    # If there are unvisited children, randomly select one of them
    return node

def simulate_random_game(board, max_moves=1000):
    while (not board.check_win_conditions()) and max_moves > 0:
        moves = board.get_possible_moves(board.current_player)
        if len(moves)>0:
            random_move = random.choice(moves)
            board.change_piece_position(random_move.start, random_move.destiny)
            board.check_blocked()
            board.current_player = draw.RED if board.current_player == draw.BLUE else draw.BLUE
        else:
            # No possible moves, the game is likely to end in a draw
            return None
        max_moves -= 1

    # Return the winner of the game
    return board.get_winner()

def select_best_move(root):
    # Select the move with the highest average score
    best_score = float("-inf")
    best_move = None
    for child in root.children:
        average_score = child.score / child.visits if child.visits > 0 else 0
        print("average score",child.move,average_score)
        if average_score > best_score:
            best_score = average_score
            best_move = child.move
    return best_move

class Move:
    def __init__(self,start,destiny):
        self.start=start
        self.destiny=destiny
    def add(self):
        self.a+=1
    def __str__(self):
        return 'Move' + str(self.start) +'->'+ str(self.destiny)
    def __repr__(self) -> str:
        return 'move' + str(self.start) +'->'+ str(self.destiny)

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
        (self.red_pieces, self.blue_pieces,self.finish_lines) = initialize_board(sizeofside)
        self.size=sizeofside

    def draw(self):
        draw.WINDOW.fill(draw.WHITE)
        for row in range((self.size*2-1)):
            for col in range(get_col_number(row,self.size)):
                x = col * draw.horizontal_distance + (draw.WIDTH - get_col_number(row,self.size) * draw.horizontal_distance) / 2
                y = row * draw.vertical_distance + (draw.HEIGHT - 9 * draw.vertical_distance) / 2
                draw.draw_hexagon(x, y, draw.hex_size, draw.BLACK)
        for pieces in self.red_pieces:
            pieces.draw()  
        for pieces in self.blue_pieces:
            pieces.draw()      
        for finish in self.finish_lines:
            finish.draw()
        if(self.selected_piece!=None):
            x, y = self.selected_piece.position
            draw.draw_hexagon_border(x, y, draw.hex_size, draw.YELLOW,2)    

    def has_friendly_neighbours(self,piece,color):
        if color==draw.BLUE:
            for piece2 in self.blue_pieces:
                if is_neighbour(piece,piece2,self.size):
                    return True
            return False
        else:
            for piece2 in self.red_pieces:
                if is_neighbour(piece,piece2,self.size):
                    return True
            return False
    
    def get_neighbouring_possibilities(self,piece,color):    
        (fromx,fromy,fromz)=coord_to_cube(piece.gameposition,self.size)
        possibilities=numpy.array([])
        #get opponent color
        if color==draw.BLUE:
            opponent=draw.RED
        else:
            opponent=draw.BLUE    
        #calculates every move in the 6 directions
        maxrow=self.size*2-2
        
        for var in numpy.arange(1,maxrow):
            if fromx+var>=self.size or fromy-var <= -self.size:
                break
            if self.can_move(piece.gameposition,cube_to_coord((fromx+var,fromy-var,fromz),self.size),color,self.size):
                possibilities = numpy.append(possibilities,Move(piece.gameposition,cube_to_coord((fromx+var,fromy-var,fromz),self.size)))
                break
        for var in numpy.arange(1,maxrow):
            if fromx-var<=-self.size or fromy+var >= self.size:
                break
            if self.can_move(piece.gameposition,cube_to_coord((fromx-var,fromy+var,fromz),self.size),color,self.size):
                possibilities = numpy.append(possibilities,Move(piece.gameposition,cube_to_coord((fromx-var,fromy+var,fromz),self.size)))
                break
        for var in numpy.arange(1,maxrow):
            if fromy+var>=self.size or fromz-var <= -self.size:
                break
            if self.can_move(piece.gameposition,cube_to_coord((fromx,fromy+var,fromz-var),self.size),color,self.size):
                possibilities = numpy.append(possibilities,Move(piece.gameposition,cube_to_coord((fromx,fromy+var,fromz-var),self.size)))
                break    
        for var in numpy.arange(1,maxrow):
            if fromy-var<=-self.size or fromz+var >= self.size:
                break
            if self.can_move(piece.gameposition,cube_to_coord((fromx,fromy-var,fromz+var),self.size),color,self.size):
                possibilities = numpy.append(possibilities,Move(piece.gameposition,cube_to_coord((fromx,fromy-var,fromz+var),self.size)))
                break    
        for var in numpy.arange(1,maxrow):
            if fromz-var>=self.size or fromx+var <= -self.size:
                break
            if self.can_move(piece.gameposition,cube_to_coord((fromx+var,fromy,fromz-var),self.size),color,self.size):
                possibilities = numpy.append(possibilities,Move(piece.gameposition,cube_to_coord((fromx+var,fromy,fromz-var),self.size)))
                break
        for var in numpy.arange(1,maxrow):
            if fromz+var<=-self.size or fromx-var >= self.size:
                break
            if self.can_move(piece.gameposition,cube_to_coord((fromx-var,fromy,fromz+var),self.size),color,self.size):
                possibilities = numpy.append(possibilities,Move(piece.gameposition,cube_to_coord((fromx-var,fromy,fromz+var),self.size)))
                break  
        return possibilities   

                

    def get_possible_moves(self,color):
        moves=numpy.array([])
        if color==draw.BLUE:
            for piece in self.blue_pieces:
                if piece.blocked==False:
                    moves= numpy.append(moves,self.get_neighbouring_possibilities(piece,color))
        else:
            for piece in self.red_pieces:
                if piece.blocked==False:
                    moves= numpy.append(moves,self.get_neighbouring_possibilities(piece,color))
        return moves 
    
    
    def avail_board(self,color):
        value=0
        if color==draw.RED:
            value=100*(len(self.red_pieces) -len(self.blue_pieces))
            value+=20*(self.blocked_Blue - self.blocked_Red) 
            for piece in self.red_pieces:
                if piece.gameposition[0]==(self.size-1) and  piece.gameposition[1]==0:
                    return float('inf')
                value -= get_pieces_distance(piece,self.finish_lines[0])
                if self.has_friendly_neighbours(piece,draw.RED):
                    value+=20
            for piece in self.blue_pieces:
                if piece.gameposition[0]==(self.size-1) and  piece.gameposition[1]==get_col_number((self.size-1),self.size)-1:
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
            value+=20*(self.blocked_Red - self.blocked_Blue)
            for piece in self.blue_pieces:
                if piece.gameposition[0]==(self.size-1) and  piece.gameposition[1]==get_col_number((self.size-1),self.size)-1:
                    return  float('inf')
                value -= get_pieces_distance(piece,self.finish_lines[1])
                if self.has_friendly_neighbours(piece,draw.BLUE):
                    value+=20
            for piece in self.red_pieces:
                if piece.gameposition[0]==(self.size-1) and  piece.gameposition[1]==0:
                    return float('inf')
                value += get_pieces_distance(piece,self.finish_lines[0])   
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
                new_board.change_piece_position(move.start,move.destiny)
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
                new_board.change_piece_position(move.start,move.destiny)
                aval= new_board.minimax(beta,alpha,depth-1,player,True)
                min_aval = min(min_aval,aval)
                beta = min(beta, aval)
                if beta <= alpha:
                    break 
                
            return min_aval
        
    def find_best_move(self, depth):    
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        print("possible moves",self.get_possible_moves(self.current_player))
        for move in self.get_possible_moves(self.current_player):
            new_board = copy.deepcopy(self)
            new_board.change_piece_position(move.start,move.destiny)
            new_board.check_blocked()
            eval = new_board.minimax(beta,alpha,depth, self.current_player,False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        ## monte carlos test     
        
        print("color",self.current_player,"score",max_eval,"best move",best_move)        
        return best_move

    def play_best_move(self,dificulty=1):
        if dificulty==1:

            time1 = time.time()
            move = self.find_best_move(2)
            time2 = time.time()
            delta= time2-time1
            print("Time to calculate the best move,mode 1: ",delta)
            print("Best move: ",move)
        elif dificulty==2:
            time1 = time.time()
            move =monte_carlo_search(self, 100)
            print(type(move))
            print("carlos, mode 2:",move)  
            time2 = time.time() 
            delta= time2-time1
            print("Time to calculate the best move: ",delta)
        elif dificulty==3:
            time1 = time.time()
            move = monte_carlo_search(self, 200)
            print(move)  
            time2 = time.time() 
            delta= time2-time1
            print("Time to calculate the best move: ",delta)

        self.change_piece_position(move.start,move.destiny)


    #checks if the position has a piece
    def check_pos(self,pos):
        if pos[0]<0 or pos[0]>(self.size*2-1) or pos[1]<0 or pos[1]>=get_col_number(pos[0],self.size):
            return False
        else:
            for piece in self.blue_pieces:
                if piece.gameposition==pos:
                    return piece
            for piece in self.red_pieces:
                if piece.gameposition==pos:
                    return piece
        return None
    
    #checks if the position has a piece of the color
    def check_pos_color(self,pos,color):
        if pos[0]<0 or pos[0]>(self.size*2-1) or pos[1]<0 or pos[1]>=get_col_number(pos[0],self.size):
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
        if pos[0]<0 or pos[0]>(self.size*2-1) or pos[1]<0 or pos[1]>=get_col_number(pos[0],self.size):
            return False
        return True
    
    def check_can_move_finishing_line(self,pos,color):
        if pos[0]==(self.size-1):
            if pos[1]==0 and color==draw.BLUE:
                return False
            elif pos[1]==get_col_number((self.size-1),self.size)-1 and color==draw.RED:
                return False
            
        return True
    def remove_piece(self,pos):

        for piece in self.red_pieces:
            if piece.gameposition==pos:
                self.red_pieces= numpy.delete(self.red_pieces,numpy.where(self.red_pieces == piece)[0])

        for piece in self.blue_pieces:
            if piece.gameposition==pos:
                self.blue_pieces= numpy.delete(self.blue_pieces,numpy.where(self.blue_pieces == piece)[0])
                  

    def change_piece_position(self,start,destination):
        for piece in self.red_pieces:
            if destination==piece.gameposition:
                self.red_pieces= numpy.delete(self.red_pieces,numpy.where(self.red_pieces == piece)[0])
                break
        for piece in self.blue_pieces:
            if destination==piece.gameposition:
                self.blue_pieces= numpy.delete(self.blue_pieces,numpy.where(self.blue_pieces == piece)[0])
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
                (fromx,fromy,fromz)=coord_to_cube(piece.gameposition,self.size)

                (tox,toy,toz)=coord_to_cube(piece2.gameposition,self.size)
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
        (fromx,fromy,fromz)=coord_to_cube(from_pos,sizeofside)

        (tox,toy,toz)=coord_to_cube(to_pos,sizeofside)
        dx = tox - fromx
        dy = toy - fromy
        dz = toz - fromz
        realsize=sizeofside-1
        #getopponent color
        if color==draw.BLUE:
            opponent=draw.RED
            if to_pos[0]==(self.size-1) and to_pos[1]==0:
                return False
        else:
            opponent=draw.BLUE
            if to_pos[0]==(self.size-1) and to_pos[1]==get_col_number((self.size-1),self.size)-1:
                return False
        check= self.check_pos(cube_to_coord((tox,toy,toz),self.size))    
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
                if self.check_pos(cube_to_coord((tox,toy,toz),self.size))==None:

                    return True
                return False
            else:
                if(dx>0):
                    xrange=numpy.arange(fromx,tox)
                else:
                    xrange=numpy.arange(fromx,tox,-1)
                if dy>0:
                    yrange=numpy.arange(fromy,toy)
                else:
                    yrange=numpy.arange(fromy,toy,-1)    
                if dz>0:
                    zrange=numpy.arange(fromz,toz)
                else:
                    zrange=numpy.arange(fromz,toz,-1)    

                if dx==0:
                    for i in numpy.arange(1,abs(dy)):
                        if self.check_pos_color(cube_to_coord((fromx,yrange[i],zrange[i]),self.size),color)==False:
                            return False
                    return True    
                elif dy==0:
                    for i in numpy.arange(1,abs(dx)):
                        if self.check_pos_color(cube_to_coord((xrange[i],fromy,zrange[i]),self.size),color)==False:
                            return False
                    return True
                elif dz==0:
                    for i in numpy.arange(1,abs(dx)):
                        if self.check_pos_color(cube_to_coord((xrange[i],yrange[i],fromz),self.size),color)==False:
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
        print(coord_to_cube(self.selected_piece.gameposition,self.size),coord_to_cube(destination,self.size))
        if self.selected_piece and self.can_move(self.selected_piece.gameposition,destination,self.selected_piece.color,self.size) and self.selected_piece.blocked==False:
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

    def get_winner(self):
        """
        Get the winner of the game.
        """
        if self.check_win_conditions():
            if len(self.blue_pieces)==self.blocked_Blue and len(self.red_pieces)==self.blocked_Red:
                return None
            elif len(self.red_pieces)==self.blocked_Red:
                return draw.BLUE
            elif len(self.blue_pieces)==self.blocked_Blue:
                return draw.RED
            elif self.check_pos_color(((self.size-1),0),draw.RED)==True:
                return draw.RED
            elif self.check_pos_color(((self.size-1),get_col_number((self.size-1),self.size)-1),draw.BLUE)==True:
                return draw.BLUE
        return None

    def check_win_conditions(self):
        """
        Check win conditions to determine if a player has won or if the game has ended in a stalemate.
        """
        if self.check_pos_color(((self.size-1),0),draw.RED)==True:
            #print("Red wins")
            return True
        elif self.check_pos_color(((self.size-1),get_col_number((self.size-1),self.size)-1),draw.BLUE)==True:
            #print("Blue wins")
            return True
        elif len(self.red_pieces)==self.blocked_Red:
            #print("Blue wins")
            return True
        elif len(self.blue_pieces)==self.blocked_Blue:
            #print("Red wins")
            return True 
        return False
    
    def get_gameposition_at_position(self, position):
        x = position[0]
        y = position[1]

        row = (y - (draw.HEIGHT - 9 * draw.vertical_distance) / 2) / draw.vertical_distance
        col = (x - (draw.WIDTH - get_col_number(round(row),self.size) * draw.horizontal_distance) / 2) / draw.horizontal_distance

        return (round(row), round(col))

    def get_piece_at_position(self, position):
        """
        Get the piece at the given position on the board.
        """
        for piece in self.blue_pieces:
            
            if math.hypot(piece.position[0] - position[0], piece.position[1] - position[1]) < draw.hex_size:
                print(piece.position,piece.gameposition)
                return piece
        for piece in self.red_pieces:
            if math.hypot(piece.position[0] - position[0], piece.position[1] - position[1]) < draw.hex_size:
                print(piece.position,piece.gameposition)
                return piece   
        return None
    
    def get_position_from_gameposition(self,gameposition):
        row, col = gameposition
        x = col * draw.horizontal_distance + (draw.WIDTH - get_col_number(row,self.size) * draw.horizontal_distance) / 2
        y = row * draw.vertical_distance + (draw.HEIGHT - 9 * draw.vertical_distance) / 2
        return (x,y)
    


def get_col_number(row,sizeofside=5):
    if row<sizeofside:
        return row+sizeofside
    else:
        return ((3*(sizeofside-1))+1)-row
    
def initialize_board(sizeofside=5):
    """
    Initialize the board state with stones placed according to the game rules.
    """
    board = {}
    red_pieces=[]
    blue_pieces=[]
    Finish_lines=[]
    
    for row in range((sizeofside*2-1)):
        for col in range(get_col_number(row,sizeofside)):
            x = col * draw.horizontal_distance + (draw.WIDTH - get_col_number(row,sizeofside) * draw.horizontal_distance) / 2

            y = row * draw.vertical_distance + (draw.HEIGHT - 9 * draw.vertical_distance) / 2
            gameposition = (row, col)
            position = (x, y)
            if row ==(sizeofside-1):
                if col == 0:
                    board[gameposition] = Finish_line(draw.RED,gameposition, position)
                    Finish_lines.append(Finish_line(draw.RED,gameposition, position))
                elif col == get_col_number(row,sizeofside) - 1:
                    board[gameposition] = Finish_line(draw.BLUE, gameposition,position)
                    Finish_lines.append(Finish_line(draw.BLUE,gameposition, position))
                elif col == 1:
                    board[gameposition] = Stone(draw.BLUE, gameposition,position)
                    blue_pieces.append(Stone(draw.BLUE, gameposition,position))
                elif col == get_col_number(row,sizeofside) - 2:
                    board[gameposition] = Stone(draw.RED, gameposition,position)
                    red_pieces.append(Stone(draw.RED, gameposition,position))
                else:
                    board[gameposition] = None        
            elif col == 0:
                board[gameposition] = Stone(draw.BLUE, gameposition,position)
                blue_pieces.append(Stone(draw.BLUE, gameposition,position))
            elif col == get_col_number(row,sizeofside) - 1:
                board[gameposition] = Stone(draw.RED, gameposition,position)
                red_pieces.append(Stone(draw.RED, gameposition,position))
            else:
                board[gameposition] = None
            
    return (numpy.array(red_pieces),numpy.array(blue_pieces),numpy.array(Finish_lines))





def is_neighbour(stone1,stone2,sizeofside=5):
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

            




def get_piece_at_position(board, position):
    """
    Get the piece at the given position on the board.
    """
    for piece in board.values():

        if math.hypot(piece.position[0] - position[0], piece.position[1] - position[1]) < draw.hex_size:
            return piece
    return None








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
