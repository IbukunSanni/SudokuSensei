"""
Test the Box-Line Reduction (Claiming) technique implementation.

Puzzle sourced from the provided reference image.
Box-Line Reduction: candidate 7 in row 2 is confined to cols 6, 7, 8
(all inside the top-right box). Row 2 therefore "claims" candidate 7
for that box, eliminating 7 from (0,6), (0,7), and (0,8).
"""

from board.board import SudokuBoard
from helpers.get_location import get_cell_location
from logic.box_line_reduction import (
    apply_one_box_line_reduction,
    apply_all_box_line_reductions,
)


def make_board_with_box_line_reduction_puzzle():
    grid = [
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 7, 0, 0, 0, 0, 8],
        [4, 9, 8, 5, 0, 0, 0, 0, 0],
        [7, 3, 2, 6, 4, 8, 0, 0, 0],
        [8, 4, 5, 3, 1, 9, 0, 0, 2],
        [9, 1, 6, 2, 7, 5, 4, 8, 3],
        [0, 0, 9, 0, 0, 0, 0, 0, 4],
        [0, 6, 4, 0, 0, 7, 3, 5, 9],
        [0, 8, 7, 0, 0, 3, 0, 0, 0],
    ]
    board = SudokuBoard(grid)
    board.update_candidates()
    return board


def test_box_line_reduction_on_given_puzzle():
    """
    Candidate 7 in row 2 only appears in cols 6, 7, 8 — all inside the
    top-right box. Row 2 claims 7 for that box, so 7 is eliminated from
    (0,6), (0,7), (0,8) in the same box.
    """
    board = make_board_with_box_line_reduction_puzzle()

    # Assert before state: claiming cells in row 2 all have 7
    claiming_cells = [(2, 6), (2, 7), (2, 8)]
    assert 7 in board.grid[2][6].get_candidates()
    assert 7 in board.grid[2][7].get_candidates()
    assert 7 in board.grid[2][8].get_candidates()

    # 7 is absent from row 2 outside the top-right box (cols 0-5 are solved)
    assert 7 not in board.grid[2][4].get_candidates()
    assert 7 not in board.grid[2][5].get_candidates()

    # Target cells (same box, different rows) have 7 before elimination
    assert 7 in board.grid[0][6].get_candidates()
    assert 7 in board.grid[0][7].get_candidates()
    assert 7 in board.grid[0][8].get_candidates()

    changed, step = apply_one_box_line_reduction(board)

    assert changed, "Expected box-line reduction to make changes"
    assert step is not None

    # Assert after state: 7 removed from rows 0-1 inside the top-right box
    assert 7 not in board.grid[0][6].get_candidates()
    assert 7 not in board.grid[0][7].get_candidates()
    assert 7 not in board.grid[0][8].get_candidates()

    # Claiming cells in row 2 still have 7
    assert 7 in board.grid[2][6].get_candidates()
    assert 7 in board.grid[2][7].get_candidates()
    assert 7 in board.grid[2][8].get_candidates()

    # Assert TechniqueStep details
    assert step.technique == "Box-Line Reduction"
    assert set(step.focus_cells) == set(claiming_cells)
    assert step.value is None

    elim_map = {k: set(tuple(p) for p in v)
                for d in step.eliminations for k, v in d.items()}
    assert elim_map["7"] == {(0, 6), (0, 7), (0, 8)}

    locs = [get_cell_location(r, c) for r, c in [(0, 6), (0, 7), (0, 8)]]
    assert "Box-Line Reduction" in step.description
    for loc in locs:
        assert loc in step.description


def test_box_line_reduction_no_change_when_absent():
    """Returns (False, None) on a fully solved board — nothing to eliminate."""
    grid = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    board = SudokuBoard(grid)
    board.update_candidates()

    changed, step = apply_one_box_line_reduction(board)

    assert not changed
    assert step is None


def test_apply_all_box_line_reductions():
    """apply_all finds at least one reduction and returns changed=True."""
    board = make_board_with_box_line_reduction_puzzle()
    changed, steps = apply_all_box_line_reductions(board)

    assert changed
    assert len(steps) >= 1
    assert all(s.technique == "Box-Line Reduction" for s in steps)
