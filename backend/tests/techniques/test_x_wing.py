"""
Test the X-Wing technique implementation.

Classic X-Wing example puzzle. Candidate 7 is confined to the same two
columns (3 and 7) in exactly two rows (1 and 5), forming the four corners
(1,3), (1,7), (5,3), (5,7). Therefore 7 can be eliminated from those two
columns in every other row.
"""

from board.board import SudokuBoard
from logic.x_wing import apply_one_x_wing, apply_all_x_wings


# Classic X-Wing example puzzle
PUZZLE = [
    [1, 0, 0, 0, 0, 0, 5, 6, 9],
    [4, 9, 2, 0, 5, 6, 1, 0, 8],
    [0, 5, 6, 1, 0, 9, 2, 4, 0],
    [0, 0, 9, 6, 4, 0, 8, 0, 1],
    [0, 6, 4, 0, 1, 0, 0, 0, 0],
    [2, 1, 8, 0, 3, 5, 6, 0, 4],
    [0, 4, 0, 5, 0, 0, 0, 1, 6],
    [9, 0, 5, 0, 6, 1, 4, 0, 2],
    [6, 2, 1, 0, 0, 0, 0, 5, 0],
]

# The four X-Wing corners for candidate 7
CORNERS = [(1, 3), (1, 7), (5, 3), (5, 7)]

# Cells where 7 is eliminated (other rows in columns 3 and 7)
ELIMINATED = {(0, 3), (4, 3), (7, 3), (8, 3), (3, 7), (4, 7), (7, 7)}


def make_board_with_x_wing_puzzle():
    board = SudokuBoard([row[:] for row in PUZZLE])
    board.update_candidates()
    return board


def test_x_wing_on_given_puzzle():
    """
    Candidate 7 forms an X-Wing on columns 3 and 7 across rows 1 and 5.
    7 is eliminated from the other cells in columns 3 and 7.
    """
    board = make_board_with_x_wing_puzzle()

    # Pre-conditions: 7 is a candidate in all four corners
    for r, c in CORNERS:
        assert 7 in board.grid[r][c].get_candidates()

    # Pre-conditions: 7 is a candidate in every cell that should be eliminated
    for r, c in ELIMINATED:
        assert 7 in board.grid[r][c].get_candidates()

    changed, step = apply_one_x_wing(board)

    assert changed, "Expected X-Wing to make a change"
    assert step is not None
    assert step.technique == "X-Wing"
    assert step.value is None

    # 7 removed from every eliminated cell
    for r, c in ELIMINATED:
        assert 7 not in board.grid[r][c].get_candidates()

    # The four corners still keep candidate 7
    for r, c in CORNERS:
        assert 7 in board.grid[r][c].get_candidates()

    # Focus cells are the four X-Wing corners
    assert set(step.focus_cells) == set(CORNERS)

    # Elimination recorded correctly
    elim_map = {k: set(tuple(p) for p in v)
                for d in step.eliminations for k, v in d.items()}
    assert elim_map["7"] == ELIMINATED

    assert "X-Wing elimination" in step.description


def test_no_x_wing_on_empty_board():
    """No X-Wing exists on a fully empty board — every candidate appears in
    far more than two cells per row and column."""
    grid = [[0] * 9 for _ in range(9)]
    board = SudokuBoard(grid)
    board.update_candidates()

    changed, step = apply_one_x_wing(board)

    assert not changed
    assert step is None


def test_apply_all_x_wings():
    """apply_all_x_wings finds at least one X-Wing and returns changed=True
    with a non-empty step list."""
    board = make_board_with_x_wing_puzzle()
    changed, steps = apply_all_x_wings(board)

    assert changed
    assert len(steps) >= 1
    assert all(s.technique == "X-Wing" for s in steps)
