def get_candidates(board, row, col):
    if board[row][col] != 0:
        return []  # already filled

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


def apply_naked_singles(board):
    """
    Applies Naked Singles technique once over the board.
    Returns:
        updated_board (list of lists): board after filling naked singles.
        changed (bool): True if at least one cell was filled, else False.
    """
    changed = False
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                candidates = get_candidates(board, row, col)
                if len(candidates) == 1:
                    board[row][col] = candidates[0]
                    changed = True
    return board, changed
