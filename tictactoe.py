"""
Tic Tac Toe Player
"""

import math
import numpy as np
from copy import deepcopy

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
    temp = np.array(board)
    count_x = (temp == X).sum()
    count_o = (temp == O).sum()
    if count_x == count_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                action.add((i, j))
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid Move...")
    mark = player(board)
    new_board = deepcopy(board)
    new_board[i][j] = mark
    return new_board


def row_winner(board, mark):
    return any(all(item == mark for item in row) for row in board)


def diagonal_winner(board, mark):
    return all(board[i][i] == mark for i in range(3)) or all(board[i][2-i] == mark for i in range(3))


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if row_winner(board, X) or row_winner(np.transpose(board), X) or diagonal_winner(board, X):
        return X
    if row_winner(board, O) or row_winner(np.transpose(board), O) or diagonal_winner(board, O):
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return utility(board) != 0 or all(all(item != EMPTY for item in row) for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def max_value_alpha_beta(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    v = -math.inf
    best = None
    for action in actions(board):
        min_v = min_value_alpha_beta(result(board, action), alpha, beta)[0]
        if min_v > v:
            v = min_v
            best = action
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v, best


def min_value_alpha_beta(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    v = math.inf
    best = None
    for action in actions(board):
        max_v = max_value_alpha_beta(result(board, action), alpha, beta)[0]
        if max_v < v:
            v = max_v
            best = action
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v, best


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        return max_value_alpha_beta(board, -math.inf, math.inf)[1]
    elif player(board) == O:
        return min_value_alpha_beta(board, -math.inf, math.inf)[1]
    else:
        raise Exception("problem in algorithm...")
