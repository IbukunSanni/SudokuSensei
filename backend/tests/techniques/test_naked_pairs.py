import pytest
from board.board import SudokuBoard
from logic.naked_pairs import apply_one_naked_pair


def make_board_with_candidates():
    # Start with an empty board (all cells unsolved)
    grid = [[0] * 9 for _ in range(9)]
    board = SudokuBoard(grid)

    # Manually set up row 0:
    # - Cells 0 and 1 form the naked pair {1,2}
    # - Cell 2 has candidates {1,2,3}
    # - Cell 3 has candidates {2,4}
    # - Cells 4–8 have no candidates (treated as solved for this test)
    row = board.get_row(0)
    row[0].set_candidates({1, 2})
    row[1].set_candidates({1, 2})
    row[2].set_candidates({1, 2, 3})
    row[3].set_candidates({2, 4})
    for i in range(4, 9):
        row[i].set_candidates(set())
    return board


def test_naked_pairs_row_elimination():
    board = make_board_with_candidates()
    row = board.get_row(0)

    # Sanity: initial candidate sets
    assert row[0].get_candidates() == {1, 2}
    assert row[1].get_candidates() == {1, 2}
    assert row[2].get_candidates() == {1, 2, 3}
    assert row[3].get_candidates() == {2, 4}

    # Apply the naked-pair technique
    changed, step = apply_one_naked_pair(board)
    assert changed, "Expected apply_one_naked_pair to return True"

    # After elimination:
    # - Cell 2 should have lost 1 and 2 → only {3}
    # - Cell 3 should have lost 2 → only {4}
    assert row[2].get_candidates() == {
        3
    }, f"Expected {{3}}, got {row[2].get_candidates()}"
    assert row[3].get_candidates() == {
        4
    }, f"Expected {{4}}, got {row[3].get_candidates()}"

    # The naked‐pair cells themselves remain unchanged
    assert row[0].get_candidates() == {1, 2}
    assert row[1].get_candidates() == {1, 2}

    # Other cells in the row (4–8) still have empty candidate sets
    for i in range(4, 9):
        assert row[i].get_candidates() == set()

    # Optionally, verify the step records the correct focus cells and eliminations
    assert set(step.focus_cells) == {(0, 0), (0, 1)}
    elim_map = {k: set(v) for d in step.eliminations for k, v in d.items()}
    assert elim_map["1"] == {(0, 2)}
    assert elim_map["2"] == {(0, 2), (0, 3)}
