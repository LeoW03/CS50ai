"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counter = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                counter = counter + 1
    if counter % 2 == 0:
        return "O"
    else:
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                moves.append((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not None:
        raise ActionError('Invalid Action')

    move = player(board)
    newboard = copy.deepcopy(board)
    newboard[action[0]][action[1]] = move
    return newboard



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checks for wins involving top left square
    if board[0][0] is not None:
        player = board[0][0]
        if board[0][1] == player and board[0][2] == player or board[1][0] == player and board[2][0] == player:
            return player
    
    # Checks for wins involving middle square
    if board[1][1] is not None:   
        player = board[1][1]
        if board[0][1] == player and board[2][1] == player or board[1][0] == player and board[1][2] == player or board[0][0] == player and board[2][2] == player or board[2][0] == player and board[0][2] == player:
            return player 

    # Checks for wins involving bottom right square
    if board[2][2] is not None:    
        player = board[2][2]
        if board[2][0] == player and board[2][1] == player or board[0][2] == player and board[1][2] == player:
            return player

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                return False
                
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    if winner(board) == "X":
        return 1

    if winner(board) == "O":
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # If player is 'X' / Playing for max score
    if player(board) == "X":
        optimal = {"action": None, "value": -math.inf}
        for action in actions(board):
            value = minvalue(result(board, action))
            if value > optimal["value"]:
                optimal["action"] = action
                optimal["value"] = value
        return optimal["action"]

    # If player is 'O' / Playing for min score
    else:
        optimal = {"action": None, "value": math.inf}
        for action in actions(board):
            value = maxvalue(result(board, action))
            if value < optimal["value"]:
                optimal["action"] = action
                optimal["value"] = value
        return optimal["action"]


def maxvalue(board):
    """
    Returns max score given action
    """

    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        new = minvalue(result(board, action))
        v = max(v, new)
    return v


def minvalue(board):
    """
    Returns min score given action
    """

    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        new = maxvalue(result(board, action))
        v = min(v, new)
    return v


