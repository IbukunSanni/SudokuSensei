"""
API routes for SudokuSensei
"""

from fastapi import APIRouter, HTTPException
from api.models import (
    PuzzleInput,
    SolveResponse,
    ErrorDetail,
    HealthResponse,
    DetailedHealthResponse,
)
from services.solver_service import SudokuSolverService

# Create router
router = APIRouter()

# Initialize solver service
solver_service = SudokuSolverService()


@router.get("/", response_model=HealthResponse)
def health_check():
    """Basic health check endpoint"""
    return HealthResponse(status="SudokuSensei backend is running!", version="1.0")


@router.get("/health", response_model=DetailedHealthResponse)
def detailed_health():
    """Detailed health check with service information"""
    return DetailedHealthResponse(
        status="healthy",
        service="SudokuSensei API",
        endpoints=["/", "/health", "/solve"],
        cors_enabled=True,
        frontend_url="http://localhost:3000",
    )


@router.post("/solve", response_model=SolveResponse)
def solve_sudoku(data: PuzzleInput):
    """
    Solve a Sudoku puzzle using advanced logical techniques

    Args:
        data: Puzzle input containing 9x9 grid

    Returns:
        Solved puzzle with metadata

    Raises:
        HTTPException: If puzzle is invalid or unsolvable
    """
    result = solver_service.solve_puzzle(data.puzzle)

    # Handle errors
    if result.get("error", False):
        error_detail = ErrorDetail(
            error=result["error_type"].replace("_", " ").title(),
            error_type=result["error_type"],
            message=result["message"],
            suggestions=result["suggestions"],
        )

        status_code = 400 if result["error_type"] == "INVALID_FORMAT" else 422
        raise HTTPException(status_code=status_code, detail=error_detail.dict())

    # Return successful result
    return SolveResponse(
        solved_grid=result["solved_grid"],
        is_solved=result["is_solved"],
        message=result["message"],
        techniques_used=result["techniques_used"],
    )
