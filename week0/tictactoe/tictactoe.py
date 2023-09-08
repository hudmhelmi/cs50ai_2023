"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    cell_count, x_count, o_count, empty_count = 0, 0, 0, 0

    # Count number of Xs, Os, and empty cells
    for row in board:
        for cell in row:
            cell_count += 1
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
            else:
                empty_count += 1

    # If there are no empty cells, the game is over
    if empty_count == 0:
        return None

    # If all cells are empty or if there are equal number of Xs and Os, it's X's turn
    if cell_count == empty_count or x_count == o_count:
        return X

    # If there are more Xs than Os, it's O's turn
    if x_count > o_count:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    # Loop through all cells
    for row in range(len(board)):
        for cell in range(len(board)):
            # If cell is empty, add it to the set of possible actions
            if board[row][cell] == EMPTY:
                possible_actions.add((row, cell))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # If the action is not valid, raise an exception
    if action not in actions(board):
        raise Exception("Invalid action")

    # Make a deep copy of the board
    board_copy = deepcopy(board)

    # Get the current player
    current_player = player(board)

    # Get the row and cell of the action
    row, cell = action

    # Update the board with the current player
    board_copy[row][cell] = current_player

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]

    # Check columns
    for cell in range(len(board)):
        if (
            board[0][cell] == board[1][cell] == board[2][cell]
            and board[0][cell] != EMPTY
        ):
            return board[0][cell]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if player(board) is None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(board):
        """
        Return a list containing the max value and optimal action
        """
        if terminal(board):
            return [utility(board), None]
        v = -math.inf
        for action in actions(board):
            v_new = max(v, min_value(result(board, action))[0])
            if v_new > v:
                v = v_new
                optimal_action = action
        return [v, optimal_action]

    def min_value(board):
        """
        Return a list containing the min value and optimal action
        """
        if terminal(board):
            return [utility(board), None]
        v = math.inf
        for action in actions(board):
            v_new = min(v, max_value(result(board, action))[0])
            if v_new < v:
                v = v_new
                optimal_action = action
        return [v, optimal_action]

    # If the game is over, return None
    if terminal(board):
        return None

    # If the player is X, attempt to play the maximising optimal action
    if player(board) == X:
        return max_value(board)[1]

    # If the player is O, attempt to play the minimising optimal action
    if player(board) == O:
        return min_value(board)[1]
