import copy


def start(start_loc):
    board = []
    i = 0
    for r in range(5):
        board.append([])
        for c in range(r+1):
            if (r,c) == start_loc[i]:
                board[r].append(0)
                if i < len(start_loc) -1:
                    i+=1
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
     
        

def attempt_move(board,jumper,sitter):
    jumper_r = jumper[0]
    jumper_c = jumper[1]
    
    sitter_r = sitter[0]
    sitter_c = sitter[1]
    
    if board[sitter_r][sitter_c] == 0:
        print("JUMP DENIED. NO PIN TO JUMP")
        return board
    elif board[jumper_r][jumper_c] == 0:
        print("JUMP DENIED. NO PIN AT THIS LOCATION")
        return board
    
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
                        '''   
                        else:
                            print("CASE 1.a: jump denied. space not open")
                    else:
                        print("CASE 1.a: jump denied. space doesn't exist (no column)")
                    '''
                # CASE 1.b if jumper is to the left of sitter
                elif jumper_c < sitter_c:
                    
                    #checking if space exits and that space is open
                    if (sitter_c + 1) < (sitter_r + 1):
                        if board[sitter_r][sitter_c+1] == 0:
                            #print("CASE 1.b: jump occured")
                            landing = (sitter_r, sitter_c+1)
                            board = move(board,jumper,sitter,landing)
                        '''    
                        else:
                            print("CASE 1.b: jump denied. space not open")
                    else:
                        print("CASE 1.b: jump denied. space doesn't exist (no column)")
                    '''
        # CASE 2: jumper above sitter
        elif jumper_r < sitter_r:
            
            # only can jump if there is a row below the sitter
            if sitter_r < 5:
                
                #CASE 2.a  sitter is to the lower-right (one column over)
                if sitter_c == (jumper_c + 1):
                    
                    #spot to lower-right of sitter must be open
                    if board[sitter_r+1][sitter_c+1] == 0:
                        #print("CASE 2.a: jump occured")
                        landing = (sitter_r+1,sitter_c+1)
                        board = move(board,jumper,sitter,landing)
                        return board
                    '''
                    else:
                        print("CASE 2.a: jump denied. space not open")
                    '''
                #CASE 2.b: sitter is to the lower-left (same column)
                elif sitter_c == jumper_c:
                    
                    #spot to lower-left of sitter must be open
                    if board[sitter_r+1][sitter_c] == 0:
                        #print("CASE 2.b: jump occured")
                        landing = (sitter_r+1, sitter_c)
                        board = move(board,jumper,sitter,landing)
                        return board
                    '''
                    else:
                        print("CASE 2.b: jump denied. space not open")
                
                    
            else:
                print("CASE 2: jump denied. space doesn't exist (no row)")
            '''
        # CASE 3: jumper below sitter
        elif jumper_r > sitter_r:    
            
            # only can jump if there is a row above the sitter
            if sitter_r > 0:
                
                # CASE 3.a: sitter is to upper left (one column over)
                if sitter_c == (jumper_c - 1):
                    
                    #spot to upper-left of sitter must exist and be open
                    if (sitter_c-1 >= 0):
                        if board[sitter_r-1][sitter_c-1] == 0:
                            #print("CASE 3.a: jump occured")
                            landing = (sitter_r-1, sitter_c-1)
                            board = move(board,jumper,sitter,landing)
                        '''
                        else:
                            print("CASE 3.a: jump denied. space not open")
                    else:
                        print("CASE 3.s: jump denied. space doesn't exist (column)")
                    '''  
                # CASE 3.b: sitter is to upper right (same column)
                elif sitter_c == jumper_c:
                    
                    #spot to upper-right of sitter must exist and be open
                    if (sitter_c <= sitter_r-1):
                        if board[sitter_r-1][sitter_c] == 0:
                            #print("CASE 3.b: jump occured")
                            landing = (sitter_r-1, sitter_c)
                            board = move(board, jumper,sitter,landing)
                            '''
                        else:
                            print("CASE 3.b: jump denied. space not open")
                    else:
                        print("CASE 3.b: jump denied. space doesn't exist (column)")
            else:
                print("CASE 3: Jump endied. Space doesn't exist (row)")
            '''
        return board

def finished(moves):
    for move in moves:
        if moves[move] != []:
            return False
    else:
        return True
        


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
                    elif(board[r+1][c+1] ==1):
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


def count_pins(board):
    pins = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 1:
                pins += 1
    return pins

# Function to find 
def find_winners(board,jumped_pins,winners):
        moves = find_moves(board)    
        #show_board(board)
        if count_pins(board) == 1:
            winning_pins = copy.deepcopy(jumped_pins)
            winners.append(winning_pins)
            #print(jumped_pins)   
            jumped_pins.pop()
            return 
        
        elif finished(moves):
            #show_board(board)
            jumped_pins.pop()
            return 
        
        for jumper in moves:
            for sitter in moves[jumper]:
                boardcopy = copy.deepcopy(board)
                next_board = attempt_move(boardcopy,jumper,sitter)
                jumped_pins.append((jumper,sitter))
                copy_pins = copy.deepcopy(jumped_pins)
                #print(len(copy_pins))   
                #show_board(boardcopy)                                
                find_winners(next_board,copy_pins,winners)
                jumped_pins.pop()
    

if __name__ == "__main__":
    b1 = start([(2,1)])
    show_board(b1)
    path = []
    winners =[]
    find_winners(b1,path,winners)

    
    for solution in winners:
        print(solution)  

