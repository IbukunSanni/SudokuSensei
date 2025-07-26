"""
API routes for SudokuSensei backend application.
Provides endpoints for solving Sudoku puzzles and health checks.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Tuple

# Import services
from services.solver_service import SudokuSolver
from services.frontend_solver import frontend_solver
from services.step_by_step_solver import step_by_step_solver
from services.validation_service import (
    is_valid_format,
    is_solvable,
    has_unique_solution,
)

# Initialize router
router = APIRouter()

# Initialize services
solver = SudokuSolver()  # Keep for backward compatibility if needed


# Data models
class PuzzleInput(BaseModel):
    """Input model for Sudoku puzzle"""

    puzzle: List[List[int]] = Field(
        ...,
        description="9x9 Sudoku grid with 0 for empty cells and 1-9 for filled cells",
    )


class CandidateChange(BaseModel):
    """Model for a change in candidates for a cell"""

    position: Tuple[int, int] = Field(
        ..., description="Row and column indices of the cell"
    )
    location: str = Field(..., description="Human-readable location (e.g., 'R1C2')")
    eliminated: List[int] = Field(..., description="Candidates that were eliminated")
    old_candidates: List[int] = Field(..., description="Candidates before the change")
    new_candidates: List[int] = Field(..., description="Candidates after the change")


class SolvingStep(BaseModel):
    """Model for a single step in the solving process"""

    grid: List[List[int]] = Field(
        ..., description="The state of the grid after this step"
    )
    candidates: Optional[List[List[List[int]]]] = Field(
        None, description="The state of candidates for each cell after this step"
    )
    technique: str = Field(..., description="The technique applied in this step")
    description: str = Field(
        ..., description="Detailed description of what happened in this step"
    )
    cells_solved: int = Field(..., description="Number of cells solved in this step")
    candidates_eliminated: Optional[int] = Field(
        0, description="Number of candidates eliminated in this step"
    )
    candidate_changes: Optional[List[CandidateChange]] = Field(
        None, description="Details of candidate changes in this step"
    )
    solved_positions: Optional[List[str]] = Field(
        None, description="Positions of cells that were solved in this step"
    )


class SolveResponse(BaseModel):
    """Response model for solved puzzle"""

    solved_grid: List[List[int]] = Field(..., description="The solved 9x9 grid")
    is_solved: bool = Field(..., description="Whether the puzzle was completely solved")
    message: str = Field(..., description="Status message about the solving process")
    techniques_applied: Optional[List[str]] = Field(
        default=None, description="List of techniques that were successfully applied"
    )
    solving_steps: Optional[List[SolvingStep]] = Field(
        default=None,
        description="Complete step-by-step solving process with grid states and detailed descriptions",
    )


class ErrorResponse(BaseModel):
    """Error response model"""

    error: str
    error_type: str
    message: str
    suggestions: List[str] = []


def format_error(error_type: str, message: str, suggestions: List[str]) -> dict:
    """
    Create a properly formatted error response using the ErrorResponse model.

    Args:
        error_type: Type identifier for the error (e.g., "INVALID_FORMAT")
        message: Detailed error message explaining the issue
        suggestions: List of suggestions to help the user fix the error

    Returns:
        Dictionary representation of the ErrorResponse model ready for HTTP response
    """
    return ErrorResponse(
        error=error_type.replace("_", " ").title(),
        error_type=error_type,
        message=message,
        suggestions=suggestions,
    ).dict()


# API endpoints
@router.get("/")
def health_check():
    """Basic health check endpoint"""
    return {"status": "SudokuSensei backend is running!", "version": "1.0"}


@router.get("/health")
def detailed_health():
    """Detailed health check with service information"""
    return {
        "status": "healthy",
        "service": "SudokuSensei API",
        "endpoints": ["/", "/health", "/solve"],
        "cors_enabled": True,
        "frontend_url": "http://localhost:3000",
    }


@router.post("/solve", response_model=SolveResponse)
def solve_sudoku(data: PuzzleInput):
    """
    Solve a Sudoku puzzle using advanced logical techniques.

    This endpoint validates the input puzzle format, checks if it's solvable and has a unique solution,
    then attempts to solve it using various Sudoku solving techniques.

    Args:
        data: Puzzle input containing 9x9 grid where 0 represents empty cells

    Returns:
        Solved puzzle with metadata including techniques used

    Raises:
        HTTPException(400): If puzzle format is invalid
        HTTPException(422): If puzzle is unsolvable or has multiple solutions
    """
    # Validate puzzle format
    if not is_valid_format(data.puzzle):
        raise HTTPException(
            status_code=400,
            detail=format_error(
                "INVALID_FORMAT",
                "Puzzle must be a 9x9 grid with numbers 0-9",
                [
                    "Ensure your puzzle is exactly 9 rows and 9 columns",
                    "Use 0 for empty cells and numbers 1-9 for filled cells",
                    "Check that all values are integers between 0 and 9",
                ],
            ),
        )

    # Check if puzzle is solvable
    if not is_solvable(data.puzzle):
        raise HTTPException(
            status_code=422,
            detail=format_error(
                "NO_SOLUTION",
                "This puzzle is not solvable - it violates Sudoku rules",
                [
                    "Check for duplicate numbers in rows, columns, or 3x3 boxes",
                    "Verify that the puzzle follows standard Sudoku rules",
                    "Try loading the example puzzle to test the solver",
                ],
            ),
        )

    # Check if puzzle has a unique solution
    if not has_unique_solution(data.puzzle):
        raise HTTPException(
            status_code=422,
            detail=format_error(
                "MULTIPLE_SOLUTIONS",
                "This puzzle has multiple possible solutions",
                [
                    "A valid Sudoku puzzle should have exactly one unique solution",
                    "Add more clues to constrain the puzzle to a single solution",
                    "Verify that all given numbers are correct",
                    "Try loading the example puzzle which has a unique solution",
                ],
            ),
        )

    # Use the step-by-step solver for single technique application
    result = step_by_step_solver.solve(data.puzzle)

    return SolveResponse(
        solved_grid=result["solved_grid"],
        is_solved=result["is_solved"],
        message=result["message"],
        techniques_applied=result.get("techniques_applied", []),
        solving_steps=result.get("solving_steps", []),
    )


@router.post("/solve-step", response_model=SolveResponse)
def solve_single_step(data: PuzzleInput):
    """
    Apply a single solving technique to the puzzle.

    This endpoint applies only one technique and returns the result,
    allowing for more granular control over the solving process.

    Args:
        data: Puzzle input containing 9x9 grid where 0 represents empty cells

    Returns:
        Result after applying one technique step

    Raises:
        HTTPException(400): If puzzle format is invalid
        HTTPException(422): If puzzle is unsolvable
    """
    # Validate puzzle format
    if not is_valid_format(data.puzzle):
        raise HTTPException(
            status_code=400,
            detail=format_error(
                "INVALID_FORMAT",
                "Puzzle must be a 9x9 grid with numbers 0-9",
                [
                    "Ensure your puzzle is exactly 9 rows and 9 columns",
                    "Use 0 for empty cells and numbers 1-9 for filled cells",
                    "Check that all values are integers between 0 and 9",
                ],
            ),
        )

    # Check if puzzle is solvable
    if not is_solvable(data.puzzle):
        raise HTTPException(
            status_code=422,
            detail=format_error(
                "NO_SOLUTION",
                "This puzzle is not solvable - it violates Sudoku rules",
                [
                    "Check for duplicate numbers in rows, columns, or 3x3 boxes",
                    "Verify that the puzzle follows standard Sudoku rules",
                ],
            ),
        )

    # Apply single step using step-by-step solver
    from board.board import SudokuBoard
    from logic.naked_single import apply_one_naked_single
    from logic.hidden_single import apply_one_hidden_single
    from logic.naked_pairs import apply_one_naked_pair
    from logic.hidden_pairs import apply_one_hidden_pair
    from logic.naked_triples import apply_one_naked_triple

    board = SudokuBoard(data.puzzle)
    board.update_candidates()  # Initial constraint propagation

    # Try techniques in order until one succeeds
    techniques = [
        ("Naked Single", apply_one_naked_single),
        ("Hidden Single", apply_one_hidden_single),
        ("Naked Pair", apply_one_naked_pair),
        ("Hidden Pair", apply_one_hidden_pair),
        ("Naked Triple", apply_one_naked_triple),
    ]

    for technique_name, technique_func in techniques:
        changed, step = technique_func(board)
        if changed and step:
            # Apply constraint propagation after technique
            constraint_changes = board.update_candidates()

            # Build response
            solved_grid = [[cell.get_value() for cell in row] for row in board.grid]

            # Create single solving step
            solving_step = {
                "grid": solved_grid,
                "candidates": board.get_candidates_grid(),
                "technique": step.technique,
                "description": step.description,
                "cells_solved": 1 if step.value else 0,
                "candidates_eliminated": len(
                    [pos for elim in step.eliminations for pos in elim.values()]
                ),
                "candidate_changes": [],  # Could be enhanced to show detailed changes
                "solved_positions": (
                    [f"{get_cell_location(fc[0], fc[1])}={step.value}"]
                    if step.value
                    else []
                ),
            }

            return SolveResponse(
                solved_grid=solved_grid,
                is_solved=board.is_solved(),
                message=f"Applied {technique_name}: {step.description}",
                techniques_applied=[technique_name],
                solving_steps=[solving_step],
            )

    # No technique could be applied
    solved_grid = [[cell.get_value() for cell in row] for row in board.grid]
    return SolveResponse(
        solved_grid=solved_grid,
        is_solved=board.is_solved(),
        message="No technique could be applied to this puzzle state",
        techniques_applied=[],
        solving_steps=[],
    )
