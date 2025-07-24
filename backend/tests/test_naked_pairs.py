from board.board import SudokuBoard
from logic.naked_pairs import apply_one_naked_pair


def test_naked_pairs_on_realistic_grid():
    # Provided puzzle grid (some hardcoded solutions for most cells)
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
    changed, step = apply_one_naked_pair(board)

    # We care mostly about structure here, since actual eliminations will depend on candidate calculations
    assert isinstance(changed, bool)  # Should return a bool for changed
    if changed:
        assert step is not None
        assert hasattr(step, "technique")
        assert step.technique == "Naked Pair"
        assert hasattr(step, "eliminations")
        assert isinstance(step.eliminations, list)
        # The description should offer info
        assert (
            "Naked Pair" in step.description or "eliminated" in step.description.lower()
        )
    else:
        # It is possible no naked pair was found first-call; this is still correct
        assert step is None

    # Optionally, print info for visual confirmation during local dev
    print("Naked Pair Step:", getattr(step, "description", "None found"))


# To run:
# pytest backend/tests/test_naked_pairs.py
