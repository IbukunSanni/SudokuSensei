from board.board import SudokuBoard
from logic.naked_pairs import apply_one_naked_pair
from helpers.get_location import get_cell_location


def make_board_with_naked_pair_puzzle():
    # Your puzzle, row by row; zeros are blanks:
    grid = [
        [4, 0, 0, 2, 7, 0, 6, 0, 0],
        [7, 9, 8, 1, 5, 6, 2, 3, 4],
        [0, 2, 0, 8, 4, 0, 0, 0, 7],
        [2, 3, 7, 4, 6, 8, 9, 5, 1],
        [8, 4, 9, 5, 3, 1, 7, 2, 6],
        [5, 6, 1, 7, 9, 2, 8, 4, 3],
        [0, 8, 2, 0, 1, 5, 4, 7, 9],
        [0, 7, 0, 0, 2, 4, 3, 0, 0],
        [0, 0, 4, 0, 8, 7, 0, 0, 2],
    ]
    board = SudokuBoard(grid)
    board.update_candidates()
    return board


def test_naked_pairs_on_given_puzzle():
    board = make_board_with_naked_pair_puzzle()

    # Assert before state: in row 9, B9 and G9 form the naked pair {1, 5}.
    naked_pair_cells = [(8, 1), (8, 6)]
    eliminated_cells = [(8, 0), (8, 7)]
    assert board.grid[8][1].get_candidates() == {1, 5}
    assert board.grid[8][6].get_candidates() == {1, 5}
    assert board.grid[8][0].get_candidates() == {1, 3, 6, 9}
    assert board.grid[8][7].get_candidates() == {1, 6}

    changed, step = apply_one_naked_pair(board)
    assert changed, "Expected apply_one_naked_pair to find a naked pair"
    assert step is not None

    # Assert after state: the pair eliminates 1 from the other row-9 cells.
    assert board.grid[8][0].get_candidates() == {3, 6, 9}
    assert board.grid[8][7].get_candidates() == {6}

    # The naked-pair cells themselves remain unchanged.
    assert board.grid[8][1].get_candidates() == {1, 5}
    assert board.grid[8][6].get_candidates() == {1, 5}

    # Assert TechniqueStep details.
    assert step.technique == "Naked Pair"
    assert set(naked_pair_cells).issubset(set(step.focus_cells))

    elim_map = {k: set(v) for d in step.eliminations for k, v in d.items()}
    assert elim_map["1"] == set(eliminated_cells)

    locs = [get_cell_location(r, c) for r, c in eliminated_cells]
    assert "Naked Pair" in step.description
    for loc in locs:
        assert loc in step.description
