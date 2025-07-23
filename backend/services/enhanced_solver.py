"""
Enhanced Sudoku solver service that tracks both cell placements and candidate eliminations.
This provides a more detailed step-by-step solving process.
"""

from typing import Dict, Any, List, Tuple, Set
import copy
from board.board import SudokuBoard
from logic.naked_single import apply_all_naked_singles
from logic.hidden_single import apply_all_hidden_singles
from logic.hidden_pairs import apply_all_hidden_pairs
from logic.naked_pairs import apply_all_naked_pairs
from helpers.get_location import get_cell_location


class EnhancedSudokuSolver:
    """
    Enhanced solver class that tracks both cell placements and candidate eliminations.
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
        Tracks and records each step of the solving process with detailed information
        about both cell placements and candidate eliminations.

        Args:
            puzzle: 9x9 grid of integers (0 for empty cells)

        Returns:
            Dictionary containing:
            - solved_grid: The solved/partially solved grid
            - is_solved: Whether the puzzle was completely solved
            - message: Description of the result
            - techniques_applied: List of techniques that made progress
            - solving_steps: List of steps with grid states and candidate changes
        """
        board = SudokuBoard(puzzle)
        techniques_applied = []
        solving_steps = []

        # Add initial state with more details
        initial_grid = [[cell.get_value() for cell in row] for row in board.grid]
        initial_candidates = board.get_candidates_grid()
        initial_empty_count = sum(
            1 for row in initial_grid for cell in row if cell == 0
        )

        # Update candidates for initial state
        candidate_changes = board.update_candidates()

        solving_steps.append(
            {
                "grid": copy.deepcopy(initial_grid),
                "candidates": copy.deepcopy(initial_candidates),
                "technique": "Initial State",
                "description": f"Starting puzzle with {initial_empty_count} empty cells",
                "cells_solved": 0,
                "candidates_eliminated": len(candidate_changes),
                "candidate_changes": candidate_changes,
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
                before_candidates = board.get_candidates_grid()
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
                    after_candidates = board.get_candidates_grid()
                    after_solved_count = sum(
                        1 for row in after_grid for cell in row if cell != 0
                    )
                    cells_solved = after_solved_count - before_solved_count

                    # Find which cells were solved
                    solved_positions = []
                    for row in range(9):
                        for col in range(9):
                            if before_grid[row][col] == 0 and after_grid[row][col] != 0:
                                solved_positions.append(
                                    f"{get_cell_location(row, col)}={after_grid[row][col]}"
                                )

                    # Find candidate changes
                    candidate_changes = []
                    for row in range(9):
                        for col in range(9):
                            if (
                                before_candidates[row][col]
                                != after_candidates[row][col]
                            ):
                                eliminated = (
                                    before_candidates[row][col]
                                    - after_candidates[row][col]
                                )
                                if eliminated:
                                    candidate_changes.append(
                                        {
                                            "position": (row, col),
                                            "location": get_cell_location(row, col),
                                            "eliminated": eliminated,
                                            "old_candidates": before_candidates[row][
                                                col
                                            ],
                                            "new_candidates": after_candidates[row][
                                                col
                                            ],
                                        }
                                    )

                    remaining_empty = sum(
                        1 for row in after_grid for cell in row if cell == 0
                    )

                    # Create description based on what happened
                    if cells_solved > 0:
                        description = f"Step {step_number}: {technique_name} solved {cells_solved} cell(s)"
                        if solved_positions:
                            description += f" - {', '.join(solved_positions)}"
                        description += f". {remaining_empty} cells remaining."
                    else:
                        description = f"Step {step_number}: {technique_name} eliminated {len(candidate_changes)} candidate(s)"
                        if candidate_changes:
                            eliminated_desc = []
                            for change in candidate_changes[
                                :3
                            ]:  # Limit to first 3 for brevity
                                eliminated_desc.append(
                                    f"{change['location']} removed {sorted(change['eliminated'])}"
                                )
                            if len(candidate_changes) > 3:
                                eliminated_desc.append(
                                    f"and {len(candidate_changes)-3} more..."
                                )
                            description += f" - {', '.join(eliminated_desc)}"

                    solving_steps.append(
                        {
                            "grid": copy.deepcopy(after_grid),
                            "candidates": copy.deepcopy(after_candidates),
                            "technique": technique_name,
                            "description": description,
                            "cells_solved": cells_solved,
                            "candidates_eliminated": len(candidate_changes),
                            "candidate_changes": candidate_changes,
                            "solved_positions": solved_positions,
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
                        "candidates": copy.deepcopy(board.get_candidates_grid()),
                        "technique": "Final State",
                        "description": f"Solving completed. {final_empty} cells could not be solved with available techniques.",
                        "cells_solved": 0,
                        "candidates_eliminated": 0,
                        "candidate_changes": [],
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
enhanced_solver = EnhancedSudokuSolver()
