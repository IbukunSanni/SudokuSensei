from board.board import SudokuBoard
from logic.swordfish import apply_one_swordfish
from services.step_by_step_solver import StepByStepSolver


def candidate_board():
    board = SudokuBoard([[0] * 9 for _ in range(9)])
    for row in board.grid:
        for cell in row:
            cell.set_candidates(set())
    return board


def add_candidate(board, candidate, positions):
    for row, col in positions:
        board.grid[row][col].set_candidates({candidate, 9})


def test_row_swordfish_eliminates_from_three_cover_columns():
    board = candidate_board()
    focus = [(1, 2), (1, 5), (4, 5), (4, 7), (8, 2), (8, 7)]
    targets = [(0, 2), (3, 5), (6, 7)]
    add_candidate(board, 4, focus + targets)

    changed, step = apply_one_swordfish(board)

    assert changed
    assert step.technique == "Swordfish"
    assert step.extra == {
        "orientation": "rows",
        "bases": (1, 4, 8),
        "covers": (2, 5, 7),
        "candidate": 4,
    }
    assert set(step.focus_cells) == set(focus)
    assert all(4 not in board.grid[row][col].get_candidates() for row, col in targets)
    assert all(4 in board.grid[row][col].get_candidates() for row, col in focus)


def test_column_swordfish_eliminates_from_three_cover_rows():
    board = candidate_board()
    focus = [(1, 0), (6, 0), (1, 3), (8, 3), (6, 7), (8, 7)]
    targets = [(1, 2), (6, 5), (8, 8)]
    add_candidate(board, 5, focus + targets)

    changed, step = apply_one_swordfish(board)

    assert changed
    assert step.extra["orientation"] == "columns"
    assert step.extra["bases"] == (0, 3, 7)
    assert all(5 not in board.grid[row][col].get_candidates() for row, col in targets)


def test_near_miss_with_four_cover_columns_is_not_swordfish():
    board = candidate_board()
    pattern = [(1, 1), (1, 4), (3, 4), (3, 7), (6, 1), (6, 8)]
    add_candidate(board, 3, pattern + [(0, 1)])

    changed, step = apply_one_swordfish(board)

    assert not changed
    assert step is None
    assert 3 in board.grid[0][1].get_candidates()


def test_pattern_without_an_elimination_is_not_reported_as_a_step():
    board = candidate_board()
    pattern = [(0, 1), (0, 4), (3, 4), (3, 7), (6, 1), (6, 7)]
    add_candidate(board, 2, pattern)

    changed, step = apply_one_swordfish(board)

    assert not changed
    assert step is None


def test_swordfish_candidate_changes_replay_from_snapshots():
    board = candidate_board()
    focus = [(1, 2), (1, 5), (4, 5), (4, 7), (8, 2), (8, 7)]
    targets = [(0, 2), (3, 5), (6, 7)]
    add_candidate(board, 4, focus + targets)
    before = board.get_candidates_grid()
    grid = [[0] * 9 for _ in range(9)]

    changed, _ = apply_one_swordfish(board)
    changes = StepByStepSolver.derive_candidate_changes(
        grid, grid, before, board.get_candidates_grid()
    )

    assert changed
    assert {change.position for change in changes} == set(targets)
    assert all(change.eliminated == [4] for change in changes)
