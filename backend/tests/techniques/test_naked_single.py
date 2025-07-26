from board.board import SudokuBoard
from logic.naked_single import apply_one_naked_single


def make_board_with_naked_single():
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


def test_naked_single_fill():
    board = make_board_with_naked_single()
    changed, step = apply_one_naked_single(board)
    [print(f"{k}:{v}") for k, v in step.to_dict().items()]

    assert changed, "A naked single should be found and filled"
    assert step is not None
    # After application, cell [0][0] should be 1 (the only candidate)
    assert board.grid[0][0].get_value() == 1
    # Cell should have no candidates left
    assert board.grid[0][0].get_candidates() == set()
    # Step description should mention 'Naked Single'
    assert "Naked Single" in step.description
