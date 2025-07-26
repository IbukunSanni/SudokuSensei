"""
Step-by-step Sudoku solver that applies one technique at a time and generates proper steps.
Uses the updated technique functions that return TechniqueStep objects.
"""

from typing import Dict, Any, List, Tuple
import copy
from board.board import SudokuBoard
from logic.naked_single import apply_one_naked_single
from logic.hidden_single import apply_one_hidden_single
from logic.hidden_pairs import apply_one_hidden_pair
from logic.naked_pairs import apply_one_naked_pair
from helpers.get_location import get_cell_location
from config.settings import settings


class StepByStepSolver:
    """
    Solver that applies one technique at a time and generates detailed steps.
    """

    def __init__(self, max_iterations=None):
        """Initialize the solver with available techniques and max_iterations."""
        self.MAX_ITERATIONS = (
            max_iterations
            if max_iterations is not None
            else settings.SUDOKU_MAX_ITERATIONS
        )
        # Order techniques by complexity - simpler techniques first
        self.techniques = [
            ("Naked Single", apply_one_naked_single),
            ("Hidden Single", apply_one_hidden_single),
            ("Naked Pair", apply_one_naked_pair),
            ("Hidden Pair", apply_one_hidden_pair),
        ]

    def solve(self, puzzle: List[List[int]]) -> Dict[str, Any]:
        """
        Solve a Sudoku puzzle applying one technique at a time.

        Returns:
            Dictionary with solved grid, steps, and metadata
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
                self._create_constraint_step(
                    constraint_changes,
                    board,
                    f"Applied basic Sudoku constraints to starting puzzle with {initial_empty_count} empty cells",
                )
            )

        # Main solving loop
        changed = True
        iteration = 0
        step_number = 1

        while changed and iteration < self.MAX_ITERATIONS and not board.is_solved():
            changed = False
            iteration += 1

            # Try each technique once per iteration
            for technique_name, technique_func in self.techniques:
                if board.is_solved():
                    break

                # Save state before technique
                before_grid = [[cell.get_value() for cell in row] for row in board.grid]
                before_candidates = board.get_candidates_grid()

                # Apply single technique
                technique_applied, technique_step = technique_func(board)

                if technique_applied and technique_step:
                    changed = True
                    step_number += 1

                    if technique_name not in techniques_applied:
                        techniques_applied.append(technique_name)

                    # Get state after technique
                    after_grid = [
                        [cell.get_value() for cell in row] for row in board.grid
                    ]
                    after_candidates = board.get_candidates_grid()

                    # Count cells solved
                    cells_solved = sum(
                        1
                        for r in range(9)
                        for c in range(9)
                        if before_grid[r][c] == 0 and after_grid[r][c] != 0
                    )

                    # Find solved positions
                    solved_positions = []
                    for r in range(9):
                        for c in range(9):
                            if before_grid[r][c] == 0 and after_grid[r][c] != 0:
                                solved_positions.append(
                                    f"{get_cell_location(r, c)}={after_grid[r][c]}"
                                )

                    # Count candidate eliminations
                    eliminations_count = 0
                    for elimination in technique_step.eliminations:
                        for positions in elimination.values():
                            eliminations_count += len(positions)

                    # Create solving step from TechniqueStep
                    solving_step = {
                        "step_type": "technique",
                        "step_number": step_number,
                        "grid": copy.deepcopy(after_grid),
                        "candidates": copy.deepcopy(after_candidates),
                        "technique": technique_step.technique,
                        "description": f"Step {step_number}: {technique_step.description}",
                        "cells_solved": cells_solved,
                        "candidates_eliminated": eliminations_count,
                        "candidate_changes": self._format_eliminations(
                            technique_step.eliminations
                        ),
                        "solved_positions": solved_positions,
                        "focus_cells": technique_step.focus_cells,
                        "value": technique_step.value,
                        "explanation": self._get_technique_explanation(technique_name),
                    }

                    solving_steps.append(solving_step)

                    # Apply constraint propagation if cells were solved
                    if cells_solved > 0:
                        constraint_changes = board.update_candidates()

                        if constraint_changes:
                            constraint_step = self._create_constraint_step(
                                constraint_changes,
                                board,
                                f"Eliminated {len(constraint_changes)} candidates due to newly filled cells",
                                solved_positions,
                            )
                            solving_steps.append(constraint_step)

                    # Break after applying one technique successfully
                    break

        # Final state
        solved_grid = [[cell.get_value() for cell in row] for row in board.grid]

        # Result message
        if board.is_solved():
            message = f"Puzzle solved successfully in {len(solving_steps)} steps using {len(techniques_applied)} technique(s)!"
        else:
            empty_cells = sum(1 for row in solved_grid for cell in row if cell == 0)
            message = f"Partial solution: {empty_cells} cells remaining after {len(solving_steps)} steps using {len(techniques_applied)} technique(s)"

        return {
            "solved_grid": solved_grid,
            "is_solved": board.is_solved(),
            "message": message,
            "techniques_applied": techniques_applied,
            "iterations": iteration,
            "solving_steps": solving_steps,
            "total_steps": len(solving_steps),
        }

    def _create_constraint_step(
        self,
        constraint_changes: List[Dict],
        board: SudokuBoard,
        description: str,
        solved_positions: List[str] = None,
    ) -> Dict:
        """Create a constraint propagation step."""
        return {
            "step_type": "constraint_elimination",
            "grid": copy.deepcopy(
                [[cell.get_value() for cell in row] for row in board.grid]
            ),
            "candidates": copy.deepcopy(board.get_candidates_grid()),
            "technique": "Constraint Propagation",
            "description": description,
            "cells_solved": 0,
            "candidates_eliminated": len(constraint_changes),
            "candidate_changes": self._format_constraint_changes(constraint_changes),
            "solved_positions": solved_positions or [],
            "explanation": "Removed candidates that conflict with filled cells in their rows, columns, and boxes",
        }

    def _format_eliminations(self, eliminations: List[Dict]) -> List[Dict]:
        """Format eliminations from TechniqueStep into API format."""
        formatted = []
        for elimination in eliminations:
            for candidate, positions in elimination.items():
                for pos in positions:
                    formatted.append(
                        {
                            "position": pos,
                            "location": get_cell_location(pos[0], pos[1]),
                            "eliminated": [int(candidate)],
                            "old_candidates": [],  # Would need to track this separately
                            "new_candidates": [],  # Would need to track this separately
                        }
                    )
        return formatted

    def _format_constraint_changes(self, constraint_changes: List[Dict]) -> List[Dict]:
        """Format constraint propagation changes."""
        formatted = []
        for change in constraint_changes:
            formatted.append(
                {
                    "position": change["position"],
                    "location": change["location"],
                    "eliminated": list(change["eliminated"]),
                    "old_candidates": list(change["old_candidates"]),
                    "new_candidates": list(change["new_candidates"]),
                }
            )
        return formatted

    def _get_technique_explanation(self, technique_name: str) -> str:
        """Get educational explanation for each technique."""
        explanations = {
            "Naked Single": "When a cell has only one possible candidate remaining, that candidate must be the solution",
            "Hidden Single": "When a candidate appears only once within a row, column, or box, it must go in that cell",
            "Hidden Pair": "When two candidates appear only in the same two cells within a unit, other candidates can be eliminated from those cells",
            "Naked Pair": "When two cells in a unit contain the same two candidates, those candidates can be eliminated from other cells in that unit",
        }
        return explanations.get(
            technique_name, f"Applied {technique_name} solving technique"
        )

    def get_available_techniques(self) -> List[str]:
        """Get list of available solving techniques."""
        return [name for name, _ in self.techniques]


# Global solver instance
step_by_step_solver = StepByStepSolver()
