"""
Frontend-optimized Sudoku solver that separates solving into clear, distinct steps:
1. Technique Step: Shows which technique filled cells
2. Constraint Elimination Step: Shows candidates eliminated by basic constraints
3. Advanced Elimination Step: Shows candidates eliminated by advanced techniques
"""

from typing import Dict, Any, List, Tuple, Set
import copy
from board.board import SudokuBoard
from logic.naked_single import apply_all_naked_singles
from logic.hidden_single import apply_all_hidden_singles
from logic.hidden_pairs import apply_all_hidden_pairs
from logic.naked_pairs import apply_all_naked_pairs
from logic.naked_triples import apply_all_naked_triples
from helpers.get_location import get_cell_location
from config.settings import settings


class FrontendSudokuSolver:
    """
    Solver optimized for frontend display with clear step separation.
    """

    def __init__(self, max_iterations=None):
        """Initialize the solver with available techniques and max_iterations."""
        self.MAX_ITERATIONS = (
            max_iterations
            if max_iterations is not None
            else settings.SUDOKU_MAX_ITERATIONS
        )
        self.techniques = [
            ("Naked Singles", apply_all_naked_singles),
            ("Hidden Singles", apply_all_hidden_singles),
            ("Hidden Pairs", apply_all_hidden_pairs),
            ("Naked Pairs", apply_all_naked_pairs),
            ("Naked Triples", apply_all_naked_triples),
        ]

    def solve(self, puzzle: List[List[int]]) -> Dict[str, Any]:
        """
        Solve a Sudoku puzzle with clear step separation for frontend display.

        Returns steps in this order:
        1. Initial constraint propagation
        2. For each technique application:
           a. Technique step (shows cells filled)
           b. Constraint elimination step (shows basic eliminations)
           c. Advanced elimination step (if any advanced eliminations)
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
        constraint_changes = board.update_candidates()

        if constraint_changes:
            solving_steps.append(
                {
                    "step_type": "initial_constraints",
                    "grid": copy.deepcopy(
                        [[cell.get_value() for cell in row] for row in board.grid]
                    ),
                    "candidates": copy.deepcopy(board.get_candidates_grid()),
                    "technique": "Initial Setup",
                    "description": f"Applied basic Sudoku constraints to starting puzzle with {initial_empty_count} empty cells",
                    "cells_solved": 0,
                    "candidates_eliminated": len(constraint_changes),
                    "candidate_changes": self._format_constraint_changes(
                        constraint_changes
                    ),
                    "explanation": "Eliminated candidates that conflict with given numbers in rows, columns, and boxes",
                }
            )

        changed = True
        iteration = 0
        step_number = 1

        while changed and iteration < self.MAX_ITERATIONS:
            changed = False
            iteration += 1

            for technique_name, technique_func in self.techniques:
                # Save state before technique
                before_grid = [[cell.get_value() for cell in row] for row in board.grid]
                before_candidates = board.get_candidates_grid()
                before_solved_count = sum(
                    1 for row in before_grid for cell in row if cell != 0
                )

                # Apply technique (this may fill cells and eliminate candidates)
                technique_applied = technique_func(board)

                if technique_applied:
                    changed = True
                    if technique_name not in techniques_applied:
                        techniques_applied.append(technique_name)

                    # Get state after technique but before constraint propagation
                    after_technique_grid = [
                        [cell.get_value() for cell in row] for row in board.grid
                    ]
                    after_technique_candidates = board.get_candidates_grid()
                    after_solved_count = sum(
                        1 for row in after_technique_grid for cell in row if cell != 0
                    )
                    cells_solved = after_solved_count - before_solved_count

                    # Find which cells were solved by the technique
                    solved_positions = []
                    for row in range(9):
                        for col in range(9):
                            if (
                                before_grid[row][col] == 0
                                and after_technique_grid[row][col] != 0
                            ):
                                solved_positions.append(
                                    f"{get_cell_location(row, col)}={after_technique_grid[row][col]}"
                                )

                    # Find technique eliminations (candidates eliminated by the technique itself)
                    technique_eliminations = []
                    for row in range(9):
                        for col in range(9):
                            if (
                                before_candidates[row][col]
                                != after_technique_candidates[row][col]
                            ):
                                eliminated = (
                                    before_candidates[row][col]
                                    - after_technique_candidates[row][col]
                                )
                                if (
                                    eliminated and after_technique_grid[row][col] == 0
                                ):  # Only count if cell wasn't solved
                                    technique_eliminations.append(
                                        {
                                            "position": (row, col),
                                            "location": get_cell_location(row, col),
                                            "eliminated": eliminated,
                                            "old_candidates": before_candidates[row][
                                                col
                                            ],
                                            "new_candidates": after_technique_candidates[
                                                row
                                            ][
                                                col
                                            ],
                                        }
                                    )

                    # STEP A: Technique Step (shows what the technique accomplished)
                    if cells_solved > 0 or technique_eliminations:
                        technique_description = self._create_technique_description(
                            step_number,
                            technique_name,
                            cells_solved,
                            len(technique_eliminations),
                        )

                        solving_steps.append(
                            {
                                "step_type": "technique",
                                "grid": copy.deepcopy(after_technique_grid),
                                "candidates": copy.deepcopy(after_technique_candidates),
                                "technique": technique_name,
                                "description": technique_description,
                                "cells_solved": cells_solved,
                                "candidates_eliminated": len(technique_eliminations),
                                "candidate_changes": technique_eliminations,
                                "solved_positions": solved_positions,
                                "explanation": self._get_technique_explanation(
                                    technique_name
                                ),
                            }
                        )

                    # STEP B: Constraint Elimination Step (if cells were filled)
                    if cells_solved > 0:
                        # Apply constraint propagation
                        constraint_changes = board.update_candidates()

                        if constraint_changes:
                            final_grid = [
                                [cell.get_value() for cell in row] for row in board.grid
                            ]

                            solving_steps.append(
                                {
                                    "step_type": "constraint_elimination",
                                    "grid": copy.deepcopy(final_grid),
                                    "candidates": copy.deepcopy(
                                        board.get_candidates_grid()
                                    ),
                                    "technique": "Constraint Propagation",
                                    "description": f"Eliminated {len(constraint_changes)} candidates due to newly filled cells",
                                    "cells_solved": 0,
                                    "candidates_eliminated": len(constraint_changes),
                                    "candidate_changes": self._format_constraint_changes(
                                        constraint_changes
                                    ),
                                    "solved_positions": solved_positions,  # Reference to cells that caused this
                                    "explanation": f"Removed candidates that conflict with {', '.join(solved_positions)} in their rows, columns, and boxes",
                                }
                            )

                    step_number += 1

        # Final state
        solved_grid = [[cell.get_value() for cell in row] for row in board.grid]

        # Result message
        if board.is_solved():
            message = f"Puzzle solved successfully in {step_number-1} logical steps using {len(techniques_applied)} technique(s)!"
        else:
            empty_cells = sum(1 for row in solved_grid for cell in row if cell == 0)
            message = f"Partial solution: {empty_cells} cells remaining after {step_number-1} steps using {len(techniques_applied)} technique(s)"

        return {
            "solved_grid": solved_grid,
            "is_solved": board.is_solved(),
            "message": message,
            "techniques_applied": techniques_applied,
            "iterations": iteration,
            "solving_steps": solving_steps,
            "total_logical_steps": step_number - 1,
        }

    def _format_constraint_changes(self, constraint_changes: List[Dict]) -> List[Dict]:
        """Format constraint propagation changes."""
        formatted = []
        for change in constraint_changes:
            formatted.append(
                {
                    "position": change["position"],
                    "location": change["location"],
                    "eliminated": change["eliminated"],
                    "old_candidates": change["old_candidates"],
                    "new_candidates": change["new_candidates"],
                }
            )
        return formatted

    def _create_technique_description(
        self, step_num: int, technique: str, cells_solved: int, eliminations: int
    ) -> str:
        """Create description for technique step."""
        desc = f"Step {step_num}: {technique}"

        if cells_solved > 0 and eliminations > 0:
            desc += f" filled {cells_solved} cell(s) and eliminated {eliminations} candidate(s)"
        elif cells_solved > 0:
            desc += f" filled {cells_solved} cell(s)"
        elif eliminations > 0:
            desc += f" eliminated {eliminations} candidate(s)"

        return desc

    def _get_technique_explanation(self, technique_name: str) -> str:
        """Get educational explanation for each technique."""
        explanations = {
            "Naked Singles": "When a cell has only one possible candidate remaining, that candidate must be the solution",
            "Hidden Singles": "When a candidate appears only once within a row, column, or box, it must go in that cell",
            "Hidden Pairs": "When two candidates appear only in the same two cells within a unit, other candidates can be eliminated from those cells",
            "Naked Pairs": "When two cells in a unit contain the same two candidates, those candidates can be eliminated from other cells in that unit",
            "Naked Triples": "When three cells in a unit contain the same three candidates between them, those candidates can be eliminated from other cells in that unit",
            "Initial Setup": "Basic Sudoku constraints eliminate candidates that would violate row, column, or box rules",
        }
        return explanations.get(
            technique_name, f"Applied {technique_name} solving technique"
        )

    def get_available_techniques(self) -> List[str]:
        """Get list of available solving techniques."""
        return [name for name, _ in self.techniques]


# Global solver instance
frontend_solver = FrontendSudokuSolver()
