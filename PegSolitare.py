'''
Claudio LoBraico, April 2020 (Quarantine)

This is a script that can be used to play  triangular peg solitaire, as made popular by Cracker Barrel.
The find_solutions function uses  depth-first search (DFS) to 
find all possible solutions (a.k.a one pin left on the board) for a given starting point


'''
import copy
import random
import sys
from timeit import default_timer as timer


def start(start_loc):
    
    
    # Check that starting location is possible
    if (start_loc[1] > start_loc[0]) or (start_loc[0] > 4) or (start_loc[1] > 4) or (start_loc[0] < 0) or (start_loc[1] < 0):
        sys.exit('Not a valid starting location.')
    
    # If so, create the board, with starting_location as the empty spot
    board = []
    for r in range(5):
        board.append([])
        for c in range(r+1):            # col index can't go above row index
            if (r,c) == start_loc:
                board[r].append(0)
                
            else:
                board[r].append(1)
    return board
        
        
        
def show_board(board):
    print_str = ""
    for r in range(len(board)):
        print_str += ((5-r)* " ")
        for c in range(len(board[r])):
            print_str += " " +  str(board[r][c])
        print(print_str)
        print_str = ""   

        
# Function to move pin over another (changes board). Works as a helper for attempt_move
def move(board,jumper,sitter,landing):
    jumper_r = jumper[0]
    jumper_c = jumper[1]
    
    sitter_r = sitter[0]
    sitter_c = sitter[1]
    
    landing_r = landing[0]
    landing_c = landing[1]
        
    board[landing_r][landing_c] = 1
    board[jumper_r][jumper_c] = 0
    board[sitter_r][sitter_c] = 0
    
    return board

# Function to reverse a previous move (changes board). Works as a helper for find_one_winner
def reverse_move(board,jumper,sitter,landing):
    jumper_r = jumper[0]
    jumper_c = jumper[1]
    
    sitter_r = sitter[0]
    sitter_c = sitter[1]
    
    landing_r = landing[0]
    landing_c = landing[1]
        
    board[landing_r][landing_c] = 0
    board[jumper_r][jumper_c] = 1
    board[sitter_r][sitter_c] = 1
    
    return board
    
# Function to check if a requested move is valid. If so, it executes using move helper function
def attempt_move(board,jumper,sitter):
    jumper_r = jumper[0]
    jumper_c = jumper[1]
    
    sitter_r = sitter[0]
    sitter_c = sitter[1]
    landing = (-1,1)
    
    if board[sitter_r][sitter_c] == 0:
        print("JUMP DENIED. NO PIN TO JUMP")
        return board,landing
    elif board[jumper_r][jumper_c] == 0:
        print("JUMP DENIED. NO PIN AT THIS LOCATION")
        return board,landing
    
    else:
        # CASE 1: pins in same row    
        if jumper_r == sitter_r:
            
            # only can jump if they are adjacent and there is another space within that row (at least 3 spaces)
            if (abs(jumper_c - sitter_c) == 1)  &  (len(board[jumper_r]) > 2):
                
                # CASE 1.a if jumper is to the right of sitter
                if jumper_c > sitter_c:
                    
                    # must check the space exists and that space is open 
                    if (sitter_c - 1) > -1:
                        
                        if board[sitter_r][sitter_c-1] == 0:
                            #print("CASE 1.a: jump occured")
                            landing = (sitter_r,sitter_c-1)
                            board = move(board,jumper,sitter,landing)
                         
                        else:
                            print("CASE 1.a: jump denied. space not open")
                    else:
                        print("CASE 1.a: jump denied. space doesn't exist (no column)")
                    
                # CASE 1.b if jumper is to the left of sitter
                elif jumper_c < sitter_c:
                    
                    #checking if space exits and that space is open
                    if (sitter_c + 1) < (sitter_r + 1):
                        if board[sitter_r][sitter_c+1] == 0:
                            landing = (sitter_r, sitter_c+1)
                            board = move(board,jumper,sitter,landing)
                          
                        else:
                            print("CASE 1.b: jump denied. space not open")
                    else:
                        print("CASE 1.b: jump denied. space doesn't exist (no column)")
                    
        # CASE 2: jumper above sitter
        elif jumper_r < sitter_r:
            
            # only can jump if there is a row below the sitter
            if sitter_r < 5:
                
                #CASE 2.a  sitter is to the lower-right (one column over)
                if sitter_c == (jumper_c + 1):
                    
                    #spot to lower-right of sitter must be open
                    if board[sitter_r+1][sitter_c+1] == 0:
                        landing = (sitter_r+1,sitter_c+1)
                        board = move(board,jumper,sitter,landing)
                    
                    else:
                        print("CASE 2.a: jump denied. space not open")
                    
                #CASE 2.b: sitter is to the lower-left (same column)
                elif sitter_c == jumper_c:
                    
                    #spot to lower-left of sitter must be open
                    if board[sitter_r+1][sitter_c] == 0:
                        landing = (sitter_r+1, sitter_c)
                        board = move(board,jumper,sitter,landing)                    
                    else:
                        print("CASE 2.b: jump denied. space not open")
                
                    
            else:
                print("CASE 2: jump denied. space doesn't exist (no row)")
            
        # CASE 3: jumper below sitter
        elif jumper_r > sitter_r:    
            
            # only can jump if there is a row above the sitter
            if sitter_r > 0:
                
                # CASE 3.a: sitter is to upper left (one column over)
                if sitter_c == (jumper_c - 1):
                    
                    #spot to upper-left of sitter must exist and be open
                    if (sitter_c-1 >= 0):
                        if board[sitter_r-1][sitter_c-1] == 0:
                            landing = (sitter_r-1, sitter_c-1)
                            board = move(board,jumper,sitter,landing)
                        
                        else:
                            print("CASE 3.a: jump denied. space not open")
                    else:
                        print("CASE 3.s: jump denied. space doesn't exist (column)")
                     
                # CASE 3.b: sitter is to upper right (same column)
                elif sitter_c == jumper_c:
                    
                    #spot to upper-right of sitter must exist and be open
                    if (sitter_c <= sitter_r-1):
                        if board[sitter_r-1][sitter_c] == 0:
                            landing = (sitter_r-1, sitter_c)
                            board = move(board, jumper,sitter,landing)
                            
                        else:
                            print("CASE 3.b: jump denied. space not open")
                    else:
                        print("CASE 3.b: jump denied. space doesn't exist (column)")
            else:
                print("CASE 3: Jump denied. Space doesn't exist (row)")
            
        return board,landing

# Function to check if there are no additional moves possible. Helper function for find_winners
def finished(moves):
    for move in moves:
        if moves[move] != []:
            return False
    
    return True
        

# Finds all possible moves given a certain board state
def find_moves(board):
    moves = {}
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 1:
                moves[(r,c)] = []
                
                #CHECK BELOW   
                #Can only move down if in rows 0-3
                if r < 3:
                    #check lower-left
                    if (board[r+1][c] == 1):
                        if board[r+2][c] == 0:
                            sitter = (r+1, c)
                            moves[(r,c)].append(sitter)  
                            
                        
                    #check lower_right
                    if(board[r+1][c+1] ==1):
                        if board[r+2][c+2] == 0:
                            sitter = (r+1,c+1)
                            moves[(r,c)].append(sitter)
                            
                        
                
                #CHECK ABOVE AND SIDES
                #Can only check above and to sides if in rows 2-4
                if r > 1:
                
                    #can only jump left if in column 2 or greater
                    if c >= 2:
                        # Check up-left
                        if board[r-1][c-1] == 1:
                            if board[r-2][c-2] == 0:
                                sitter = (r-1,c-1)
                                moves[(r,c)].append(sitter)
                                
                        # Check left
                        if board[r][c-1] == 1:
                            if board[r][c-2] == 0:
                                sitter = (r,c-1)
                                moves[(r,c)].append(sitter)
                            
                    
                            
                    #can only move right if r-c >=2
                    if (r-c) >= 2:
                        # Check up-right
                        if board[r-1][c] == 1:
                            if board[r-2][c] == 0:
                                sitter = (r-1,c)
                                moves[(r,c)].append(sitter)
                                
                        # Check right
                        if board[r][c+1] == 1:
                            if board[r][c+2] == 0:
                                sitter = (r,c+1)
                                moves[(r,c)].append(sitter)
    return moves

# Counts total number of pins on a given board. Helper function for find_winners
def count_pins(board):
    pins = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 1:
                pins += 1
    return pins

# Function to find all possible winning sequences with a given board
# Uses Depth-first search
def find_all_winners(board,jumped_pins,winners):
        moves = find_moves(board)   
        
        # base case 1: a single pin left on the board
        if count_pins(board) == 1:
            winning_pins = copy.deepcopy(jumped_pins)
            winners.append(winning_pins)
            jumped_pins.pop()
            return 
        
        # base case 2: no more possible moves, but not a winner
        elif finished(moves):
            jumped_pins.pop()
            return 
        
         
        for jumper in moves:
            for sitter in moves[jumper]:
               
                board_copy = copy.deepcopy(board)
                next_board,landing = attempt_move(board_copy,jumper,sitter)
                
                # Record new jump
                jumped_pins.append((jumper,sitter))
                copy_pins = copy.deepcopy(jumped_pins)
                
                # Recurse on resulting board
                find_all_winners(next_board,copy_pins,winners)
                jumped_pins.pop()
    

def find_one_winner(board,jumped_pins,winners):
    
        moves = find_moves(board) 
        
        # base case 1: a single pin left on the board
        if count_pins(board) == 1:
            winners.append(copy.deepcopy(jumped_pins))
            jumped_pins.pop()
            return True
                
        for jumper in moves:
            for sitter in moves[jumper]:
                next_board,landing = attempt_move(board,jumper,sitter)
                jumped_pins.append((jumper,sitter))
                if find_one_winner(next_board,jumped_pins,winners):
                    return True
                
                jumped_pins.pop()
                board = reverse_move(next_board, jumper, sitter, landing)

        return False
    
if __name__ == "__main__":
    rand_r = random.randrange(0,5,1)
    rand_c = random.randrange(0,rand_r+1,1)

    b1 = start((rand_r,rand_c))
    b1_copy = start((rand_r,rand_c))

    print('Starting point:\n')
    show_board(b1)
    print()


    # finding single solution    
    path = []
    winners =[]
    start = timer()
    find_one_winner(b1,path,winners)
    end = timer()
    print("Time taken by find_one_winner:", end - start,"seconds\n")
    
    # finding all solutions
    path2 = []
    winners2 =[]
    start = timer()
    find_all_winners(b1_copy,path2,winners2)
    end = timer()
    print("Time taken by find_all_winners:", end - start,"seconds\n")
    

    # walking through a randomly selected solution
    if len(winners2) > 0:
        rand_i = random.randrange(0,len(winners2),1)
        print('_______________Showing solution number',rand_i,'____________________\n')
        for step in winners2[rand_i]:
            print(step[0],'over',step[1])
            b1_copy,landing = attempt_move(b1_copy, step[0],step[1])
            show_board(b1_copy)
            print()
    

