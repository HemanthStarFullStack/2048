import random
from mygame.models import Cell

def add_new_tile(matrix):
    # Find empty cells
    all_cells = Cell.objects.filter(matrix=matrix)
    occupied_cells = set((cell.row, cell.col) for cell in all_cells)
    empty_cells = []
    for r in range(4):
        for c in range(4):
            if (r, c) not in occupied_cells:
                empty_cells.append((r, c))

    if not empty_cells:
        return # Board is full

    row, col = random.choice(empty_cells)
    # 90% chance of 2, 10% chance of 4
    value = 2 if random.random() < 0.9 else 4
    Cell.objects.create(matrix=matrix, row=row, col=col, val=value)

def get_board(matrix):
    cells = Cell.objects.filter(matrix=matrix)
    board = [[0] * 4 for _ in range(4)]
    score = 0
    for cell in cells:
        board[cell.row][cell.col] = cell.val
        score += cell.val
    return board, score

def start_game(matrix):
    # Clear existing cells for the matrix
    Cell.objects.filter(matrix=matrix).delete()
    # Add two initial tiles
    add_new_tile(matrix)
    add_new_tile(matrix)

def transpose(board):
    return [list(row) for row in zip(*board)]

def reverse(board):
    return [row[::-1] for row in board]

def compress(board):
    new_board = [[0]*4 for _ in range(4)]
    for r in range(4):
        pos = 0
        for c in range(4):
            if board[r][c] != 0:
                new_board[r][pos] = board[r][c]
                pos += 1
    return new_board

def merge(board):
    score_add = 0
    for r in range(4):
        for c in range(3):
            if board[r][c] == board[r][c+1] and board[r][c] != 0:
                board[r][c] *= 2
                score_add += board[r][c]
                board[r][c+1] = 0
    return board, score_add

def move_left(board):
    board = compress(board)
    board, score_add = merge(board)
    board = compress(board)
    return board, score_add

def move_right(board):
    board = reverse(board)
    board, score_add = move_left(board)
    board = reverse(board)
    return board, score_add

def move_up(board):
    board = transpose(board)
    board, score_add = move_left(board)
    board = transpose(board)
    return board, score_add

def move_down(board):
    board = transpose(board)
    board, score_add = move_right(board)
    board = transpose(board)
    return board, score_add

def update_db_from_board(matrix, board):
    Cell.objects.filter(matrix=matrix).delete()
    for r in range(4):
        for c in range(4):
            if board[r][c] != 0:
                Cell.objects.create(matrix=matrix, row=r, col=c, val=board[r][c])
