"""
Test the Pointing Pairs / Triples technique implementation.

Puzzle sourced from the provided reference image.
Pointing pair: candidate 4 in the top-left box (rows 0-2, cols 0-2) is
confined to column 0 — cells (0,0) and (2,0) — so 4 is eliminated from
the rest of column 0 outside the box. Only (7,0) has 4, which gets removed.
"""

from board.board import SudokuBoard
from logic.pointing_pairs import apply_one_pointing_pair, apply_all_pointing_pairs


# Puzzle from the reference image
PUZZLE = [
    [0, 0, 9, 0, 7, 0, 0, 0, 0],
    [0, 8, 0, 4, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 2, 8],
    [1, 0, 0, 0, 0, 0, 6, 7, 0],
    [0, 2, 0, 0, 1, 3, 0, 4, 0],
    [0, 4, 0, 0, 0, 7, 8, 0, 0],
    [6, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 8, 4],
]


def make_puzzle_board():
    board = SudokuBoard([row[:] for row in PUZZLE])
    board.update_candidates()
    return board


def test_pointing_pair_column_elimination():
    """
    Candidate 4 in the top-left box is confined to column 0 (cells (0,0)
    and (2,0)). Eliminates 4 from (7,0) — the only other cell in col 0
    that carries candidate 4.
    """
    board = make_puzzle_board()

    # Pre-conditions: 4 is in the pointing pair cells and in the target cell
    assert 4 in board.grid[0][0].get_candidates()
    assert 4 in board.grid[2][0].get_candidates()
    assert 4 in board.grid[7][0].get_candidates()

    # 4 must NOT be present elsewhere in col 0 outside the box
    assert 4 not in board.grid[4][0].get_candidates()
    assert 4 not in board.grid[5][0].get_candidates()
    assert 4 not in board.grid[8][0].get_candidates()

    changed, step = apply_one_pointing_pair(board)

    assert changed, "Expected pointing pair to make a change"
    assert step is not None
    assert step.technique == "Pointing Pairs"

    # 4 should be eliminated from (7,0)
    assert 4 not in board.grid[7][0].get_candidates()

    # Pointing cells themselves still have 4
    assert 4 in board.grid[0][0].get_candidates()
    assert 4 in board.grid[2][0].get_candidates()

    # Focus cells are the two pointing cells
    assert set(step.focus_cells) == {(0, 0), (2, 0)}

    # Elimination recorded correctly
    elim_map = {k: set(tuple(p) for p in v)
                for d in step.eliminations for k, v in d.items()}
    assert elim_map["4"] == {(7, 0)}

    assert step.value is None
    assert "Pointing Pairs/Triples elimination" in step.description


def test_no_pointing_pairs_on_empty_board():
    """No pointing pair exists on a fully empty board — every candidate
    spans all rows and columns within every box."""
    grid = [[0] * 9 for _ in range(9)]
    board = SudokuBoard(grid)
    board.update_candidates()

    changed, step = apply_one_pointing_pair(board)

    assert not changed
    assert step is None


def test_apply_all_pointing_pairs():
    """apply_all_pointing_pairs finds at least one pointing pair and
    returns changed=True with a non-empty step list."""
    board = make_puzzle_board()
    changed, steps = apply_all_pointing_pairs(board)

    assert changed
    assert len(steps) >= 1
    assert all(s.technique == "Pointing Pairs" for s in steps)
