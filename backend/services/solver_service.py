"""
Solver service for applying Sudoku solving techniques.
Coordinates the application of various logical solving methods.
Tracks and records the step-by-step solving process.
"""

from typing import Dict, Any, List, Tuple
import copy
from board.board import SudokuBoard
from logic.naked_single import apply_all_naked_singles
from logic.hidden_single import apply_all_hidden_singles
from logic.hidden_pairs import apply_all_hidden_pairs
from logic.naked_pairs import apply_all_naked_pairs


class SudokuSolver:
    """
    Main solver class that applies various Sudoku solving techniques.
    """

    MAX_ITERATIONS = 100  # Prevent infinite loops

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
        Tracks and records each step of the solving process with detailed information.

        Args:
            puzzle: 9x9 grid of integers (0 for empty cells)

        Returns:
            Dictionary containing:
            - solved_grid: The solved/partially solved grid
            - is_solved: Whether the puzzle was completely solved
            - message: Description of the result
            - techniques_applied: List of techniques that made progress
            - solving_steps: List of steps with board state and technique applied
        """
        board = SudokuBoard(puzzle)
        techniques_applied = []
        solving_steps = []

        # Add initial state with more details
        initial_grid = [[cell.get_value() for cell in row] for row in board.grid]
        initial_empty_count = sum(
            1 for row in initial_grid for cell in row if cell == 0
        )
        solving_steps.append(
            {
                "grid": copy.deepcopy(initial_grid),
                "technique": "Initial State",
                "description": f"Starting puzzle with {initial_empty_count} empty cells",
                "cells_solved": 0,
            }
        )

        changed = True
        iteration = 0
        step_number = 1

        while changed and iteration < self.MAX_ITERATIONS:
            changed = False
            iteration += 1

            for technique_name, technique_func in self.techniques:
                # Save grid state before applying technique
                before_grid = [[cell.get_value() for cell in row] for row in board.grid]
                before_solved_count = sum(
                    1 for row in before_grid for cell in row if cell != 0
                )

                # Apply technique
                technique_applied = technique_func(board)

                if technique_applied:
                    changed = True
                    if technique_name not in techniques_applied:
                        techniques_applied.append(technique_name)

                    # Save grid state after applying technique
                    after_grid = [
                        [cell.get_value() for cell in row] for row in board.grid
                    ]
                    after_solved_count = sum(
                        1 for row in after_grid for cell in row if cell != 0
                    )
                    cells_solved = after_solved_count - before_solved_count

                    # Record this step if it made progress
                    if cells_solved > 0:
                        # Find which cells were solved
                        solved_positions = []
                        for row in range(9):
                            for col in range(9):
                                if (
                                    before_grid[row][col] == 0
                                    and after_grid[row][col] != 0
                                ):
                                    solved_positions.append(
                                        f"R{row+1}C{col+1}={after_grid[row][col]}"
                                    )

                        remaining_empty = sum(
                            1 for row in after_grid for cell in row if cell == 0
                        )

                        description = f"Step {step_number}: {technique_name} solved {cells_solved} cell(s)"
                        if solved_positions:
                            description += f" - {', '.join(solved_positions)}"
                        description += f". {remaining_empty} cells remaining."

                        solving_steps.append(
                            {
                                "grid": copy.deepcopy(after_grid),
                                "technique": technique_name,
                                "description": description,
                                "cells_solved": cells_solved,
                            }
                        )
                        step_number += 1

        # Convert board back to grid format for final state
        solved_grid = [[cell.get_value() for cell in row] for row in board.grid]

        # Add final state if different from last step
        if solving_steps and not board.is_solved():
            final_empty = sum(1 for row in solved_grid for cell in row if cell == 0)
            if final_empty > 0:
                solving_steps.append(
                    {
                        "grid": copy.deepcopy(solved_grid),
                        "technique": "Final State",
                        "description": f"Solving completed. {final_empty} cells could not be solved with available techniques.",
                        "cells_solved": 0,
                    }
                )

        # Determine result message
        if board.is_solved():
            message = f"Puzzle solved successfully in {step_number-1} steps using {len(techniques_applied)} technique(s)!"
        else:
            empty_cells = sum(1 for row in solved_grid for cell in row if cell == 0)
            message = f"Partial solution: {empty_cells} cells remaining after {step_number-1} steps and {len(techniques_applied)} technique(s)"

        return {
            "solved_grid": solved_grid,
            "is_solved": board.is_solved(),
            "message": message,
            "techniques_applied": techniques_applied,
            "iterations": iteration,
            "solving_steps": solving_steps,
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
