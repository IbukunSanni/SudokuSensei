"""
Validation service for Sudoku puzzles.
Handles format validation, solvability checks, and uniqueness validation.
"""

from typing import List


def is_valid_format(puzzle: List[List[int]]) -> bool:
    """
    Validate puzzle format: 9x9 grid with digits 0-9.

    Args:
        puzzle: 9x9 grid of integers

    Returns:
        bool: True if format is valid
    """
    if len(puzzle) != 9:
        return False
    for row in puzzle:
        if len(row) != 9:
            return False
        for val in row:
            if not (0 <= val <= 9):
                return False
    return True


def get_candidates(board: List[List[int]], row: int, col: int) -> List[int]:
    """
    Get valid candidate numbers for a cell.

    Args:
        board: 9x9 Sudoku grid
        row: Row index (0-8)
        col: Column index (0-8)

    Returns:
        List of valid numbers (1-9) for the cell
    """
    used = set()

    # Check row
    used.update(board[row])

    # Check column
    used.update(board[r][col] for r in range(9))

    # Check 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            used.add(board[r][c])

    return [n for n in range(1, 10) if n not in used]


def find_empty_cell(board: List[List[int]]) -> tuple:
    """
    Find the first empty cell in the board.

    Args:
        board: 9x9 Sudoku grid

    Returns:
        Tuple (row, col) of empty cell, or None if board is complete
    """
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None


def count_solutions(board: List[List[int]], max_solutions: int = 2) -> int:
    """
    Count the number of solutions for a puzzle (up to max_solutions).

    Args:
        board: 9x9 Sudoku grid (will be modified during search)
        max_solutions: Maximum solutions to count (for efficiency)

    Returns:
        Number of solutions found (capped at max_solutions)
    """
    cell = find_empty_cell(board)
    if not cell:
        return 1  # Found a complete solution

    row, col = cell
    solution_count = 0

    for num in get_candidates(board, row, col):
        board[row][col] = num
        solution_count += count_solutions(board, max_solutions)
        board[row][col] = 0  # backtrack

        # Early exit if we find more than one solution
        if solution_count >= max_solutions:
            return solution_count

    return solution_count


def has_unique_solution(puzzle: List[List[int]]) -> bool:
    """
    Check if the puzzle has exactly one unique solution.

    Args:
        puzzle: 9x9 Sudoku grid

    Returns:
        bool: True if puzzle has exactly one solution
    """
    # Create a copy to avoid modifying the original
    board_copy = [row[:] for row in puzzle]
    solution_count = count_solutions(board_copy, max_solutions=2)

    return solution_count == 1


def is_solvable(puzzle: List[List[int]]) -> bool:
    """
    Check if the puzzle is solvable (has at least one solution).

    Args:
        puzzle: 9x9 Sudoku grid

    Returns:
        bool: True if puzzle is solvable
    """
    from helpers.check_solvable import check_solvable

    return check_solvable(puzzle)
