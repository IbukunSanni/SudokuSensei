from board.board import SudokuBoard
from logic.naked_single import apply_one_naked_single
from helpers.get_location import get_cell_location


def make_board_with_naked_single_puzzle():
    # Row 0, Col 0 must be 1 (naked single). All other values chosen to force this.
    grid = [
        [0, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ]
    board = SudokuBoard(grid)
    board.update_candidates()
    return board


def test_naked_single_on_given_puzzle():
    board = make_board_with_naked_single_puzzle()

    # Assert before state: A1 is unsolved and has one candidate.
    r, c = 0, 0
    assert not board.grid[r][c].is_solved()
    assert board.grid[r][c].get_candidates() == {1}

    changed, step = apply_one_naked_single(board)

    assert changed, "Expected apply_one_naked_single to find a naked single"
    assert step is not None

    # Assert after state: A1 is solved with the only candidate.
    assert board.grid[r][c].get_value() == 1
    assert board.grid[r][c].is_solved()
    assert board.grid[r][c].get_candidates() == set()

    # Assert TechniqueStep details.
    assert step.technique == "Naked Single"
    assert step.value == 1
    assert step.focus_cells == [(r, c)]

    loc = get_cell_location(r, c)
    assert "Naked Single" in step.description
    assert f"cell {loc}" in step.description
