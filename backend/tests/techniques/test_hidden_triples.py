"""
Test the hidden triples technique implementation.

Puzzle sourced from the provided reference image.
Hidden triple {1, 3, 9} is confined to column 6 (col index 5),
cells (2,5), (4,5), (5,5) — eliminating candidates {2, 4, 8}.
"""

from board.board import SudokuBoard
from logic.hidden_triples import apply_one_hidden_triple


# Puzzle from the reference image
PUZZLE = [
    [0, 0, 8, 0, 0, 7, 0, 0, 0],
    [0, 4, 2, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 6, 8, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 0, 0, 1, 3, 0, 4, 7, 0],
    [0, 8, 0, 0, 9, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
]


def make_puzzle_board():
    board = SudokuBoard([row[:] for row in PUZZLE])
    board.update_candidates()
    return board


def test_hidden_triples_elimination():
    """
    Hidden triple {1,3,9} in column 6 (col index 5) confined to cells
    (2,5), (4,5), (5,5). Eliminates candidates {2,4,8} from those cells.
    """
    board = make_puzzle_board()

    # Verify pre-condition candidates
    assert board.grid[2][5].get_candidates() == {1, 2, 3, 4, 8, 9}
    assert board.grid[4][5].get_candidates() == {1, 2, 3, 4, 8, 9}
    assert board.grid[5][5].get_candidates() == {1, 2, 3, 4, 8}

    changed, step = apply_one_hidden_triple(board)

    assert changed, "Expected hidden triple technique to make changes"
    assert step is not None
    assert step.technique == "Hidden Triple"

    # Triple cells retain only {1, 3, 9} (or subset if 9 wasn't present)
    assert board.grid[2][5].get_candidates() == {1, 3, 9}
    assert board.grid[4][5].get_candidates() == {1, 3, 9}
    assert board.grid[5][5].get_candidates() == {1, 3}   # 9 was not a candidate here

    # Focus cells are the three triple cells
    assert set(step.focus_cells) == {(2, 5), (4, 5), (5, 5)}

    # Candidates {2, 4, 8} eliminated from all three cells
    elim_map = {k: set(tuple(pos) for pos in v)
                for d in step.eliminations for k, v in d.items()}
    assert elim_map["2"] == {(2, 5), (4, 5), (5, 5)}
    assert elim_map["4"] == {(2, 5), (4, 5), (5, 5)}
    assert elim_map["8"] == {(2, 5), (4, 5), (5, 5)}

    assert step.value is None
    assert "Hidden Triple elimination" in step.description


def test_hidden_triples_no_change_when_absent():
    """Returns (False, None) when no hidden triple exists on the board."""
    # Fully empty board — every cell has candidates {1..9}, no triple is confined
    grid = [[0] * 9 for _ in range(9)]
    board = SudokuBoard(grid)
    board.update_candidates()

    changed, step = apply_one_hidden_triple(board)

    assert not changed
    assert step is None


def test_apply_all_hidden_triples():
    """apply_all_hidden_triples exhausts all triples and returns changed=True."""
    from logic.hidden_triples import apply_all_hidden_triples

    board = make_puzzle_board()
    changed, steps = apply_all_hidden_triples(board)

    assert changed
    assert len(steps) >= 1
    assert all(s.technique == "Hidden Triple" for s in steps)
