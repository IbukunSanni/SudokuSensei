from board.board import SudokuBoard
from logic.hidden_single import apply_one_hidden_single
from helpers.get_location import get_cell_location


def make_board_with_hidden_single_puzzle():
    # Your puzzle, row by row; zeros are blanks:
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

    # Assert before state: D4 is unsolved and contains the hidden value 4.
    r, c = 3, 3
    assert not board.grid[r][c].is_solved()
    assert board.grid[r][c].get_candidates() == {2, 4, 7, 9}

    changed, step = apply_one_hidden_single(board)

    assert changed, "Expected apply_one_hidden_single to find a hidden single"
    assert step is not None

    # Assert after state: D4 is solved with the hidden single value.
    assert board.grid[r][c].get_value() == 4
    assert board.grid[r][c].is_solved()
    assert board.grid[r][c].get_candidates() == set()

    # Assert TechniqueStep details.
    assert step.technique == "Hidden Single"
    assert step.value == 4
    assert step.focus_cells == [(r, c)]

    loc = get_cell_location(r, c)
    assert "Hidden Single" in step.description
    assert f"cell {loc}" in step.description
