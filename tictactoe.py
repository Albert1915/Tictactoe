"""
Tic Tac Toe Player
"""
# library that we use to
import pygame
import copy
import random

X = "X"                                 #for user selection             
O = "O"
i = None
EMPTY = None    

# int random number generator                   Line 13 - 29 function to generate music
i = random.randint(0,2)

# Starting the mixer
pygame.mixer.init()

# Loading Random Song in txt file
with open('Music/song.txt', 'r') as f:
    song = f.read().splitlines()
    pygame.mixer.music.load(song[i])


# Setting the volume
pygame.mixer.music.set_volume(1.0)

# Start playing the song
pygame.mixer.music.play()    


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],     #board is a 3x3 matrix
            [EMPTY, EMPTY, EMPTY],     #each cell is either X, O, or EMPTY
            [EMPTY, EMPTY, EMPTY]]     #board is a list of lists


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0                     #count the number of X and O
    o_count = 0                     #X always goes first

    for row in board:               #iterate through the board
        for cell in row:            #iterate through each cell
            if cell == X:           #if cell is X
                x_count += 1        #increment x_count
            if cell == O:           #if cell is O
                o_count += 1        #increment o_count

    if x_count <= o_count:          #if x_count is less than or equal to o_count
        return X                    #return X
    else:                           #if x_count is greater than o_count
        return O                    #return O



def actions(board):                 
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()                        #create an empty set

    for i, row in enumerate(board):                 #iterate through the board
        for j, cell in enumerate(row):              #iterate through each cell
            if cell == EMPTY:                       #if cell is EMPTY
                possible_actions.add((i, j))        #add (i, j) to possible_actions

    return possible_actions                         #return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):                #if action is not in actions(board)
        raise ValueError                            #raise ValueError

    new_board = copy.deepcopy(board)                #create a deep copy of board
    new_board[action[0]][action[1]] = player(new_board)     #make the move

    return new_board


def winner(board):                                  
    """
    Returns the winner of the game, if there is one.
    """
    wins = [[(0, 0), (0, 1), (0, 2)],           #list of all possible winning combinations
            [(1, 0), (1, 1), (1, 2)],           #each combination is a list of 3 tuples
            [(2, 0), (2, 1), (2, 2)],           #each tuple is a coordinate on the board
            [(0, 0), (1, 0), (2, 0)],           
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]]

    for combination in wins:                    #iterate through each combination
        checks_x = 0                            #count the number of X and O
        checks_o = 0                            #in each combination
        for i, j in combination:                #iterate through each tuple in the combination
            if board[i][j] == X:                #if the cell is X
                checks_x += 1                   #increment checks_x
            if board[i][j] == O:                #if the cell is O
                checks_o += 1                   #increment checks_o
        if checks_x == 3:
            return X
        if checks_o == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or not actions(board):             #if there is a winner or there are no actions
        return True             
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)                                   #get the winner
    if winner_player == X:                                          
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0

# Minimax Algorithm with Alpha-Beta Pruning Optimization by Hardcoding the First Move and Optimizing the Utility Function for Tic-Tac-Toe 
# (https://www.youtube.com/watch?v=l-hh51ncgDI) 
# komplexity: O(b^m) where b is the branching factor and m is the depth of the game tree
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):                                #if the game is over             
        return None

    # Optimization by hardcoding the first move
    if board == initial_state():                        
        return 0, 1

    current_player = player(board)
    best_value = float("-inf") if current_player == X else float("inf")     #set best_value to -inf if X, +inf if O

    for action in actions(board):                                           
        new_value = minimax_value(result(board, action), best_value)        #get the new value

        if current_player == X:                                             #if X, update best_value if new_value is greater
            new_value = max(best_value, new_value)                         

        if current_player == O:                                             #if O, update best_value if new_value is less
            new_value = min(best_value, new_value)

        if new_value != best_value:                                         #if new_value is better than best_value
            best_value = new_value                                          #update best_value
            best_action = action                                            #update best_action

    return best_action


# Helper function for minimax function to avoid code duplication in the loop 
# and to optimize using Alpha-Beta Pruning
def minimax_value(board, best_value):
    """
    Returns the best value for each recursive minimax iteration.
    Optimized using Alpha-Beta Pruning: If the new value found is better
    than the best value then return without checking the others.
    """
    if terminal(board):
        return utility(board)

    current_player = player(board)
    value = float("-inf") if current_player == X else float("inf")

    for action in actions(board):
        new_value = minimax_value(result(board, action), value)

        if current_player == X:                                         #if X, return new_value if it is greater than best_value
            if new_value > best_value:                                  #this is the optimization
                return new_value
            value = max(value, new_value)                               

        if current_player == O:
            if new_value < best_value:
                return new_value
            value = min(value, new_value)

    return value

