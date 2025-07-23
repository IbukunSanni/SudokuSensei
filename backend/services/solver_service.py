"""
Solver service for applying Sudoku solving techniques.
Coordinates the application of various logical solving methods.
"""

from typing import Dict, Any, List
from board.board import SudokuBoard
from logic.naked_single import apply_all_naked_singles
from logic.hidden_single import apply_all_hidden_singles
from logic.hidden_pairs import apply_all_hidden_pairs
from logic.naked_pairs import apply_all_naked_pairs


class SudokuSolver:
    """
    Main solver class that applies various Sudoku solving techniques.
    """

    def __init__(self):
        """Initialize the solver with available techniques."""
        self.techniques = [
            ("Naked Singles", apply_all_naked_singles),
            ("Hidden Singles", apply_all_hidden_singles),
            ("Hidden Pairs", apply_all_hidden_pairs),
            ("Naked Pairs", apply_all_naked_pairs),
        ]

    def solve(self, puzzle: List[List[int]]) -> Dict[str, Any]:
        """
        Solve a Sudoku puzzle using logical techniques.

        Args:
            puzzle: 9x9 grid of integers (0 for empty cells)

        Returns:
            Dictionary containing:
            - solved_grid: The solved/partially solved grid
            - is_solved: Whether the puzzle was completely solved
            - message: Description of the result
            - techniques_applied: List of techniques that made progress
        """
        board = SudokuBoard(puzzle)
        techniques_applied = []

        changed = True
        iteration = 0
        max_iterations = 100  # Prevent infinite loops

        while changed and iteration < max_iterations:
            changed = False
            iteration += 1

            for technique_name, technique_func in self.techniques:
                if technique_func(board):
                    changed = True
                    if technique_name not in techniques_applied:
                        techniques_applied.append(technique_name)

        # Convert board back to grid format
        solved_grid = [[cell.get_value() for cell in row] for row in board.grid]

        # Determine result message
        if board.is_solved():
            message = f"Puzzle solved successfully using {len(techniques_applied)} technique(s)!"
        else:
            empty_cells = sum(1 for row in solved_grid for cell in row if cell == 0)
            message = f"Partial solution: {empty_cells} cells remaining after applying logical techniques"

        return {
            "solved_grid": solved_grid,
            "is_solved": board.is_solved(),
            "message": message,
            "techniques_applied": techniques_applied,
            "iterations": iteration,
        }

    def get_available_techniques(self) -> List[str]:
        """
        Get list of available solving techniques.

        Returns:
            List of technique names
        """
        return [name for name, _ in self.techniques]


# Global solver instance
solver = SudokuSolver()
