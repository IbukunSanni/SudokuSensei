from board.board import SudokuBoard
from logic.x_wing import apply_one_x_wing


def candidate_board():
    board = SudokuBoard([[0] * 9 for _ in range(9)])
    for row in board.grid:
        for cell in row:
            cell.set_candidates(set())
    return board


def test_row_x_wing_eliminates_from_cover_columns():
    board = candidate_board()
    for row, col in [(1, 2), (1, 7), (5, 2), (5, 7), (0, 2), (8, 7)]:
        board.grid[row][col].set_candidates({4, 6})

    changed, step = apply_one_x_wing(board)

    assert changed
    assert step.technique == "X-Wing"
    assert set(step.focus_cells) == {(1, 2), (1, 7), (5, 2), (5, 7)}
    assert 4 not in board.grid[0][2].get_candidates()
    assert 4 not in board.grid[8][7].get_candidates()
    assert 4 in board.grid[1][2].get_candidates()


def test_column_x_wing_eliminates_from_cover_rows():
    board = candidate_board()
    for row, col in [(2, 1), (6, 1), (2, 4), (6, 4), (2, 0), (6, 8)]:
        board.grid[row][col].set_candidates({5, 9})

    changed, step = apply_one_x_wing(board)

    assert changed
    assert step.extra["orientation"] == "columns"
    assert 5 not in board.grid[2][0].get_candidates()
    assert 5 not in board.grid[6][8].get_candidates()
