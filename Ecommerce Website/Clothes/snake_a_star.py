import time
from queue import Queue
import random

# Initialize Board
def init_board():
    return ['.'] * 9  # Empty 3x3 board

# Print Board
def print_board(board):
    for i in range(0, 9, 3):
        print(' '.join(board[i:i + 3]))
    print()

# Check Winner
def check_winner(board):
    win_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),   # Rows
                     (0, 3, 6), (1, 4, 7), (2, 5, 8),   # Columns
                     (0, 4, 8), (2, 4, 6)]              # Diagonals

    for a, b, c in win_positions:
        if board[a] == board[b] == board[c] and board[a] != '.':
            return board[a]

    if '.' not in board:
        return "Draw"
    
    return None

# Get Valid Moves
def get_moves(board):
    return [i for i in range(9) if board[i] == '.']

# BFS Algorithm
def bfs(board, player):
    queue = Queue()
    queue.put((board, player))
    nodes_explored = 0

    while not queue.empty():
        board, player = queue.get()
        nodes_explored += 1

        winner = check_winner(board)
        if winner:
            return winner, nodes_explored

        for move in get_moves(board):
            new_board = board.copy()
            new_board[move] = player
            queue.put((new_board, 'O' if player == 'X' else 'X'))

    return "Draw", nodes_explored

# DFS Algorithm
def dfs(board, player):
    stack = [(board, player)]
    nodes_explored = 0

    while stack:
        board, player = stack.pop()
        nodes_explored += 1

        winner = check_winner(board)
        if winner:
            return winner, nodes_explored

        for move in get_moves(board):
            new_board = board.copy()
            new_board[move] = player
            stack.append((new_board, 'O' if player == 'X' else 'X'))

    return "Draw", nodes_explored

# A* Algorithm
def evaluate(board):
    """ Heuristic Function """
    winner = check_winner(board)
    if winner == 'O':
        return 10
    elif winner == 'X':
        return -10
    elif winner == "Draw":
        return 0
    return 0

def a_star(board, player):
    pq = [(0, board, player)]
    nodes_explored = 0

    while pq:
        _, board, player = pq.pop(0)
        nodes_explored += 1

        winner = check_winner(board)
        if winner:
            return winner, nodes_explored

        for move in get_moves(board):
            new_board = board.copy()
            new_board[move] = player

            heuristic = evaluate(new_board)
            pq.append((heuristic, new_board, 'O' if player == 'X' else 'X'))
            pq.sort()  # Sort by heuristic value

    return "Draw", nodes_explored

# Main Execution
board = init_board()

# Simulating Random Moves for the Start
board[random.randint(0, 8)] = 'X'
board[random.randint(0, 8)] = 'O'
print("\nInitial Board:")
print_board(board)

# BFS Execution
start = time.time()
bfs_winner, bfs_nodes = bfs(board, 'X')
bfs_time = time.time() - start

# DFS Execution
start = time.time()
dfs_winner, dfs_nodes = dfs(board, 'X')
dfs_time = time.time() - start

# A* Execution
start = time.time()
astar_winner, astar_nodes = a_star(board, 'X')
astar_time = time.time() - start

# Results
print("\n--- Search Strategy Comparison ---")
print(f"BFS: Winner = {bfs_winner}, Nodes = {bfs_nodes}, Time = {bfs_time:.4f}s")
print(f"DFS: Winner = {dfs_winner}, Nodes = {dfs_nodes}, Time = {dfs_time:.4f}s")
print(f"A*:  Winner = {astar_winner}, Nodes = {astar_nodes}, Time = {astar_time:.4f}s")
