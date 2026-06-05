from board.board import SudokuBoard
from helpers.get_location import get_cell_location
from logic.naked_triples import apply_one_naked_triple


def make_board_with_naked_triple_puzzle():
    # Your puzzle, row by row; zeros are blanks:
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 5, 6, 0, 0, 0, 0, 0, 0],
        [7, 8, 9, 0, 0, 0, 0, 0, 0],
        [3, 1, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    board = SudokuBoard(grid)
    board.update_candidates()
    return board


def test_naked_triple_on_given_puzzle():
    board = make_board_with_naked_triple_puzzle()

    # Assert before state: A1, B1, and C1 form the naked triple {1, 2, 3}.
    naked_triple_cells = [(0, 0), (0, 1), (0, 2)]
    eliminated_cells = [(0, c) for c in range(3, 9)]
    assert board.grid[0][0].get_candidates() == {1, 2}
    assert board.grid[0][1].get_candidates() == {2, 3}
    assert board.grid[0][2].get_candidates() == {1, 3}
    for r, c in eliminated_cells:
        assert board.grid[r][c].get_candidates() == set(range(1, 10))

    changed, step = apply_one_naked_triple(board)

    assert changed, "Expected apply_one_naked_triple to find a naked triple"
    assert step is not None

    # Assert after state: {1, 2, 3} is removed from other row-1 cells.
    for r, c in eliminated_cells:
        assert board.grid[r][c].get_candidates() == {4, 5, 6, 7, 8, 9}

    # The naked-triple cells themselves remain unchanged.
    assert board.grid[0][0].get_candidates() == {1, 2}
    assert board.grid[0][1].get_candidates() == {2, 3}
    assert board.grid[0][2].get_candidates() == {1, 3}

    # Assert TechniqueStep details.
    assert step.technique == "Naked Triple"
    assert set(step.focus_cells) == set(naked_triple_cells)
    assert step.value is None

    elim_map = {k: set(v) for d in step.eliminations for k, v in d.items()}
    assert elim_map["1"] == set(eliminated_cells)
    assert elim_map["2"] == set(eliminated_cells)
    assert elim_map["3"] == set(eliminated_cells)

    locs = [get_cell_location(r, c) for r, c in eliminated_cells]
    assert "Naked Triple" in step.description
    for loc in locs:
        assert loc in step.description


def test_no_naked_triples():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    board = SudokuBoard(grid)
    board.update_candidates()

    changed, step = apply_one_naked_triple(board)

    assert not changed, "Expected no changes when no naked triples exist"
    assert step is None, "Expected no step when no naked triples found"