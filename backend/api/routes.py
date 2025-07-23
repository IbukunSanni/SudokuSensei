"""
API routes for SudokuSensei backend application.
Provides endpoints for solving Sudoku puzzles and health checks.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# Import services
from services.solver_service import SudokuSolver
from services.validation_service import (
    is_valid_format,
    is_solvable,
    has_unique_solution,
)

# Initialize router
router = APIRouter()

# Initialize services
solver = SudokuSolver()


# Data models
class PuzzleInput(BaseModel):
    """Input model for Sudoku puzzle"""

    puzzle: List[List[int]] = Field(
        ...,
        description="9x9 Sudoku grid with 0 for empty cells and 1-9 for filled cells",
    )


class SolveResponse(BaseModel):
    """Response model for solved puzzle"""

    solved_grid: List[List[int]] = Field(..., description="The solved 9x9 grid")
    is_solved: bool = Field(..., description="Whether the puzzle was completely solved")
    message: str = Field(..., description="Status message about the solving process")
    techniques_applied: Optional[List[str]] = Field(
        default=None, description="List of techniques applied"
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

    # Use the solver service
    result = solver.solve(data.puzzle)

    return SolveResponse(
        solved_grid=result["solved_grid"],
        is_solved=result["is_solved"],
        message=result["message"],
        techniques_applied=result.get("techniques_applied"),
    )
