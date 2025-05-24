def find_empty_cell_with_fewest_candidates(board):
    min_candidates = 10  # max is 9, so start with something higher
    min_cell = None
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                candidates = get_candidates(board, r, c)
                if len(candidates) < min_candidates:
                    min_candidates = len(candidates)
                    min_cell = (r, c)
                if min_candidates == 1:
                    return min_cell  # best case early exit
    return min_cell


def get_candidates(board, row, col):
    used = set()
    # row
    used.update(board[row])
    # column
    used.update(board[r][col] for r in range(9))
    # box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            used.add(board[r][c])
    return [n for n in range(1, 10) if n not in used]


def solve(board):
    cell = find_empty_cell_with_fewest_candidates(board)
    if not cell:
        return True  # solved
    row, col = cell
    for num in get_candidates(board, row, col):
        board[row][col] = num
        if solve(board):
            return True
        board[row][col] = 0  # backtrack
    return False


def check_solvable(board):
    board_copy = [row[:] for row in board]
    return solve(board_copy)
