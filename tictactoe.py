"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math
from shutil import move

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
    - In this state X is always going to get the first move
    - Also needs to check if a terminal state was given then indicate that the game is already over
    """
    # check for a terminal board (game is already finished)
    if terminal(board):
        return EMPTY

    x_count = o_count = 0
    # iterate through entire board to count how many x's and o's there are
    rows, cols = len(board), len(board[0])
    for i in range(rows):
        for j in range(cols):
            element = board[i][j]
            if element == X:
                x_count += 1
            elif element == O:
                o_count += 1

    # check for any errors with turn-switching
    if abs(x_count - o_count) > 1:
        print("There must be some error with turn-switching because there are either too many x's or too many o's")

    # apply turn logic
    if x_count > o_count:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    - Iterate through each square and return the list of square with EMPTY
    """
    moves = []
    rows, cols = len(board), len(board[0])
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == EMPTY:
                moves.append((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    rows, cols = len(board), len(board[0])
    # Check that the action is valid
    # Check if the action is out of bounds
    action_i, action_j = action
    out_of_bounds = action_i < 0 or action_i > rows or action_j < 0 or action_j > cols
    # check if the square for the specified action is already occupied
    is_occupied = board[action_i][action_j] != EMPTY
    if out_of_bounds or is_occupied:  # check if the move is invalid
        return Exception("The specified move is invalid")
    # move is valid so create new board with new specified action and return this board
    new_board = deepcopy(board)
    symbol = player(board)
    new_board[action_i][action_j] = symbol
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    - Check for vertical, horizontal, or diagonal winner
    """
    # Check for vertical winner
    rows, cols = len(board), len(board[0])
    for i in range(rows):
        symbol = board[i][0]
        for j in range(cols):
            if board[i][j] != symbol:
                break
        else:  # Winner found horizonatally
            return symbol

    # check for vertical winner
    for j in range(cols):
        symbol = board[0][j]
        for i in range(rows):
            if board[i][j] != symbol:
                break
        else:  # winner found vertically
            return symbol

    # check for diagonal winner
    # checking the main diagonal (from the top left to bottom right)
    pointer = 0
    symbol = board[0][0]
    three_in_a_row_found = True
    while pointer < 3:
        if board[pointer][pointer] != symbol:
            three_in_a_row_found = False
        # Update pointers
        pointer += 1
    if three_in_a_row_found:
        return symbol

    # check the alternate diagonal (from top right to bottom left)
    three_in_a_row_found = True
    i, j = 0, 2
    symbol = board[i][j]
    for _ in range(3):
        if board[i][j] != symbol:
            three_in_a_row_found = False
        # Update pointers
        i += 1
        j -= 1
    if three_in_a_row_found:
        return symbol

    # There was no winner found
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    - If there are no more empty spots then the game is over
    - We could later improve this to detect stalemates
    """
    if winner(board):
        return True
    rows, cols = len(board), len(board[0])
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    symbol = winner(board)
    if symbol == X:
        return 1
    elif symbol == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    - Use the helper functions max_value and min_value to recursively find the best move 
    for the current player
    """
    # If we are given finished board then just return the results from the board
    if terminal(board):
        return None
    # check which player's turn it is
    player_turn = player(board)
    best_action = None
    if player_turn == X:
        value, best_action = max_value(board)
        print(value)
        print(best_action)
    else:
        value, best_action = min_value(board)
        print(value)
        print(best_action)
    return best_action


def max_value(board):
    """
    Returns the max value possible and corresponding best action given 
    this board and taking the other players moves into consideration
    """
    # If we are given finished board then just return the results from the board
    if terminal(board):
        return utility(board), board
    value = float('-inf')
    best_action, possible_actions = None, actions(board)
    # iterate through all the actions to see which action gives the best value
    for action in possible_actions:
        new_value, _ = min_value(result(board, action))
        if new_value >= value:
            value = new_value
            best_action = action
    return value, best_action


def min_value(board):
    """
    Returns the min value possible and corresponding best action given 
    this board and taking the other players moves into consideration
    """
    # If we are given finished board then just return the results from the board
    if terminal(board):
        return utility(board), board
    value = float('inf')
    best_action, possible_actions = None, actions(board)
    # iterate through all the actions to see which action gives the best value
    for action in possible_actions:
        new_value, _ = max_value(result(board, action))
        if new_value <= value:
            value = new_value
            best_action = action
    return value, best_action
