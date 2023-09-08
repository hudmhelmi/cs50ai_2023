from tictactoe import initial_state, player, actions, result, winner, terminal, utility, minimax
import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

board = initial_state()
print(board)
print(minimax(board))