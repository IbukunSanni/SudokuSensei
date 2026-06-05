from board.board import SudokuBoard
from logic.hidden_pairs import apply_one_hidden_pair
from helpers.get_location import get_cell_location


def make_board_with_hidden_pair_puzzle():
    # Your puzzle, row by row; zeros are blanks:
    grid = [
        [0, 0, 9, 0, 3, 2, 0, 0, 0],
        [0, 0, 0, 7, 4, 8, 0, 0, 0],
        [1, 6, 2, 0, 0, 0, 0, 4, 8],
        [0, 0, 1, 0, 2, 0, 5, 6, 0],
        [0, 0, 0, 9, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 1, 0, 7],
        [0, 0, 0, 0, 0, 0, 4, 0, 3],
        [0, 2, 6, 0, 0, 9, 0, 0, 0],
        [0, 0, 5, 8, 7, 0, 0, 0, 0],
    ]

    board = SudokuBoard(grid)
    board.update_candidates()
    return board


def test_hidden_pair_on_given_puzzle():
    board = make_board_with_hidden_pair_puzzle()

    # Assert before state: A1 and B1 contain the hidden pair plus extra candidates.
    hidden_pair_cells = [(0, 0), (0, 1)]
    assert board.grid[0][0].get_candidates() == {4, 5, 7, 8}
    assert board.grid[0][1].get_candidates() == {4, 7, 8}

    changed, step = apply_one_hidden_pair(board)

    assert changed, "Expected apply_one_hidden_pair to find a hidden pair"
    assert step is not None

    # Assert after state: both hidden-pair cells retain only {4, 8}.
    assert board.grid[0][0].get_candidates() == {4, 8}
    assert board.grid[0][1].get_candidates() == {4, 8}

    # Assert TechniqueStep details.
    assert step.technique == "Hidden Pair"
    assert set(step.focus_cells) == set(hidden_pair_cells)
    assert step.value is None

    elim_map = {k: set(v) for d in step.eliminations for k, v in d.items()}
    assert elim_map["5"] == {(0, 0)}
    assert elim_map["7"] == {(0, 0), (0, 1)}

    locs = [get_cell_location(r, c) for r, c in hidden_pair_cells]
    assert "Hidden Pair" in step.description
    for loc in locs:
        assert loc in step.description


def test_no_hidden_pairs():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    board = SudokuBoard(grid)
    board.update_candidates()

    changed, step = apply_one_hidden_pair(board)

    assert not changed, "Expected no changes when no hidden pairs exist"
    assert step is None, "Expected no step when no hidden pairs found"
