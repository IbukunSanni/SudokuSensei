"""
API routes for SudokuSensei
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

    Args:
        data: Puzzle input containing 9x9 grid

    Returns:
        Solved puzzle with metadata

    Raises:
        HTTPException: If puzzle is invalid or unsolvable
    """
    # Validate puzzle format
    if not is_valid_format(data.puzzle):
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid puzzle format",
                "error_type": "INVALID_FORMAT",
                "message": "Puzzle must be a 9x9 grid with numbers 0-9",
                "suggestions": [
                    "Ensure your puzzle is exactly 9 rows and 9 columns",
                    "Use 0 for empty cells and numbers 1-9 for filled cells",
                    "Check that all values are integers between 0 and 9",
                ],
            },
        )

    # Check if puzzle is solvable
    if not is_solvable(data.puzzle):
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Unsolvable puzzle",
                "error_type": "NO_SOLUTION",
                "message": "This puzzle is not solvable - it violates Sudoku rules",
                "suggestions": [
                    "Check for duplicate numbers in rows, columns, or 3x3 boxes",
                    "Verify that the puzzle follows standard Sudoku rules",
                    "Try loading the example puzzle to test the solver",
                ],
            },
        )

    # Check if puzzle has a unique solution
    if not has_unique_solution(data.puzzle):
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Multiple solutions found",
                "error_type": "MULTIPLE_SOLUTIONS",
                "message": "This puzzle has multiple possible solutions",
                "suggestions": [
                    "A valid Sudoku puzzle should have exactly one unique solution",
                    "Add more clues to constrain the puzzle to a single solution",
                    "Verify that all given numbers are correct",
                    "Try loading the example puzzle which has a unique solution",
                ],
            },
        )

    # Use the solver service
    result = solver.solve(data.puzzle)

    return SolveResponse(
        solved_grid=result["solved_grid"],
        is_solved=result["is_solved"],
        message=result["message"],
        techniques_applied=result.get("techniques_applied"),
    )
