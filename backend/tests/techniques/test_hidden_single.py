from board.board import SudokuBoard
from logic.hidden_single import apply_one_hidden_single
from helpers.get_location import get_cell_location


def make_board_with_hidden_single_puzzle():
    # Your puzzle, row by row—zeros are blanks:
    grid = [
        [0, 0, 2, 1, 9, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [7, 0, 0, 0, 4, 0, 0, 1, 9],
        [8, 0, 3, 0, 0, 0, 6, 0, 0],
        [0, 4, 5, 0, 0, 0, 2, 3, 0],
        [0, 0, 7, 0, 0, 0, 5, 0, 4],
        [3, 7, 0, 0, 8, 0, 0, 0, 6],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 3, 4, 1, 0, 0],
    ]
    board = SudokuBoard(grid)
    board.update_candidates()
    return board


def test_hidden_single_on_given_puzzle():
    board = make_board_with_hidden_single_puzzle()
    changed, step = apply_one_hidden_single(board)

    # It should find exactly one hidden single
    assert changed, "Expected apply_one_hidden_single to find a hidden single"
    assert step is not None

    # The unique hidden single is at row 3, col 3 (0-indexed),
    # and must be the digit 4
    r, c = 3, 3
    assert board.grid[r][c].get_value() == 4
    assert board.grid[r][c].is_solved()
    assert board.grid[r][c].get_candidates() == set()

    # The TechniqueStep should reference that cell and value
    assert step.value == 4
    assert step.focus_cells == [(r, c)]

    # And the description should mention Hidden Single and the cell location
    loc = get_cell_location(r, c)  # e.g. "D4"
    assert "Hidden Single" in step.description
    assert f"cell {loc}" in step.description
