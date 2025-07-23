"""
Puzzle validation utilities
"""

from typing import List


def is_valid_puzzle_format(puzzle: List[List[int]]) -> bool:
    """
    Basic format validation: 9x9 grid with digits 0-9

    Args:
        puzzle: 9x9 grid to validate

    Returns:
        bool: True if format is valid
    """
    if len(puzzle) != 9:
        return False

    for row in puzzle:
        if len(row) != 9:
            return False
        for val in row:
            if not isinstance(val, int) or not (0 <= val <= 9):
                return False

    return True


def has_unique_solution(puzzle: List[List[int]]) -> bool:
    """
    Check if the puzzle has exactly one unique solution.

    Args:
        puzzle: 9x9 Sudoku grid

    Returns:
        bool: True if puzzle has exactly one solution
    """

    def get_candidates(board, row, col):
        """Get valid candidates for a cell"""
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

    def find_empty_cell(board):
        """Find first empty cell"""
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return None

    def count_solutions(board, max_solutions=2):
        """Count solutions up to max_solutions (for efficiency)"""
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

    # Create a copy to avoid modifying the original
    board_copy = [row[:] for row in puzzle]
    solution_count = count_solutions(board_copy, max_solutions=2)

    return solution_count == 1
