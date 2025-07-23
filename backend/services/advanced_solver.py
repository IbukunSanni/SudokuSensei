"""
Advanced Sudoku solver that distinguishes between:
1. Basic constraint propagation (row/column/box eliminations from filled cells)
2. Advanced technique eliminations (pointing pairs, box/line reduction, etc.)
"""

from typing import Dict, Any, List, Tuple, Set
import copy
from board.board import SudokuBoard
from logic.naked_single import apply_all_naked_singles
from logic.hidden_single import apply_all_hidden_singles
from logic.hidden_pairs import apply_all_hidden_pairs
from logic.naked_pairs import apply_all_naked_pairs
from helpers.get_location import get_cell_location


class AdvancedSudokuSolver:
    """
    Advanced solver that tracks both basic constraint propagation and technique-based eliminations.
    """

    MAX_ITERATIONS = 100

    def __init__(self):
        """Initialize the solver with available techniques."""
        self.techniques = [
            ("Naked Singles", apply_all_naked_singles),
            ("Hidden Singles", apply_all_hidden_singles),
            ("Hidden Pairs", apply_all_hidden_pairs),
            ("Naked Pairs", apply_all_naked_pairs),
        ]

    def apply_basic_constraints(self, board: SudokuBoard) -> List[Dict]:
        """
        Apply basic constraint propagation (Type 1).
        Eliminates candidates based on filled cells in rows, columns, and boxes.

        Returns:
            List of candidate changes made by constraint propagation
        """
        return board.update_candidates()

    def apply_technique_eliminations(
        self, board: SudokuBoard, technique_name: str, technique_func
    ) -> Tuple[bool, List[Dict]]:
        """
        Apply advanced technique eliminations (Type 2).

        Args:
            board: The Sudoku board
            technique_name: Name of the technique being applied
            technique_func: Function that applies the technique

        Returns:
            Tuple of (technique_made_progress, list_of_candidate_changes)
        """
        # Save state before technique
        before_candidates = board.get_candidates_grid()

        # Apply the technique
        technique_applied = technique_func(board)

        # Find what the technique eliminated (before constraint propagation)
        after_candidates = board.get_candidates_grid()
        technique_changes = []

        for row in range(9):
            for col in range(9):
                if before_candidates[row][col] != after_candidates[row][col]:
                    eliminated = (
                        before_candidates[row][col] - after_candidates[row][col]
                    )
                    if eliminated:
                        technique_changes.append(
                            {
                                "position": (row, col),
                                "location": get_cell_location(row, col),
                                "eliminated": eliminated,
                                "old_candidates": before_candidates[row][col],
                                "new_candidates": after_candidates[row][col],
                                "elimination_type": "technique",
                            }
                        )

        return technique_applied, technique_changes

    def solve(self, puzzle: List[List[int]]) -> Dict[str, Any]:
        """
        Solve a Sudoku puzzle with detailed tracking of both constraint propagation and technique eliminations.
        """
        board = SudokuBoard(puzzle)
        techniques_applied = []
        solving_steps = []

        # Initial state
        initial_grid = [[cell.get_value() for cell in row] for row in board.grid]
        initial_empty_count = sum(
            1 for row in initial_grid for cell in row if cell == 0
        )

        # Step 1: Initial constraint propagation
        constraint_changes = self.apply_basic_constraints(board)

        if constraint_changes:
            solving_steps.append(
                {
                    "grid": copy.deepcopy(
                        [[cell.get_value() for cell in row] for row in board.grid]
                    ),
                    "candidates": copy.deepcopy(board.get_candidates_grid()),
                    "technique": "Initial Constraint Propagation",
                    "technique_type": "constraint_propagation",
                    "description": f"Applied basic row/column/box constraints to starting puzzle with {initial_empty_count} empty cells",
                    "cells_solved": 0,
                    "candidates_eliminated": len(constraint_changes),
                    "candidate_changes": self._format_constraint_changes(
                        constraint_changes
                    ),
                    "elimination_reason": "Basic constraints from given numbers",
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

                # Apply the technique (Type 2: Advanced eliminations)
                technique_applied, technique_changes = (
                    self.apply_technique_eliminations(
                        board, technique_name, technique_func
                    )
                )

                if technique_applied:
                    changed = True
                    if technique_name not in techniques_applied:
                        techniques_applied.append(technique_name)

                    # After technique, apply constraint propagation (Type 1: Basic eliminations)
                    constraint_changes = self.apply_basic_constraints(board)

                    # Get final state
                    after_grid = [
                        [cell.get_value() for cell in row] for row in board.grid
                    ]
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

                    # Combine all candidate changes
                    all_changes = technique_changes + self._format_constraint_changes(
                        constraint_changes
                    )

                    remaining_empty = sum(
                        1 for row in after_grid for cell in row if cell == 0
                    )

                    # Create description
                    description = self._create_step_description(
                        step_number,
                        technique_name,
                        cells_solved,
                        len(technique_changes),
                        len(constraint_changes),
                        remaining_empty,
                    )

                    solving_steps.append(
                        {
                            "grid": copy.deepcopy(after_grid),
                            "candidates": copy.deepcopy(board.get_candidates_grid()),
                            "technique": technique_name,
                            "technique_type": "solving_technique",
                            "description": description,
                            "cells_solved": cells_solved,
                            "candidates_eliminated": len(all_changes),
                            "candidate_changes": all_changes,
                            "solved_positions": solved_positions,
                            "technique_eliminations": len(technique_changes),
                            "constraint_eliminations": len(constraint_changes),
                        }
                    )
                    step_number += 1

        # Final state
        solved_grid = [[cell.get_value() for cell in row] for row in board.grid]

        if solving_steps and not board.is_solved():
            final_empty = sum(1 for row in solved_grid for cell in row if cell == 0)
            if final_empty > 0:
                solving_steps.append(
                    {
                        "grid": copy.deepcopy(solved_grid),
                        "candidates": copy.deepcopy(board.get_candidates_grid()),
                        "technique": "Final State",
                        "technique_type": "final",
                        "description": f"Solving completed. {final_empty} cells could not be solved with available techniques.",
                        "cells_solved": 0,
                        "candidates_eliminated": 0,
                        "candidate_changes": [],
                    }
                )

        # Result message
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

    def _format_constraint_changes(self, constraint_changes: List[Dict]) -> List[Dict]:
        """Format constraint propagation changes to match technique changes format."""
        formatted = []
        for change in constraint_changes:
            formatted.append(
                {
                    "position": change["position"],
                    "location": change["location"],
                    "eliminated": change["eliminated"],
                    "old_candidates": change["old_candidates"],
                    "new_candidates": change["new_candidates"],
                    "elimination_type": "constraint_propagation",
                }
            )
        return formatted

    def _create_step_description(
        self,
        step_num: int,
        technique: str,
        cells_solved: int,
        technique_eliminations: int,
        constraint_eliminations: int,
        remaining: int,
    ) -> str:
        """Create a detailed description of what happened in this step."""
        desc = f"Step {step_num}: {technique}"

        if technique_eliminations > 0:
            desc += f" eliminated {technique_eliminations} candidate(s) using logical deduction"

        if cells_solved > 0:
            desc += f", then solved {cells_solved} cell(s)"

        if constraint_eliminations > 0:
            desc += f", followed by {constraint_eliminations} constraint propagation elimination(s)"

        desc += f". {remaining} cells remaining."
        return desc

    def get_available_techniques(self) -> List[str]:
        """Get list of available solving techniques."""
        return [name for name, _ in self.techniques]


# Global solver instance
advanced_solver = AdvancedSudokuSolver()
