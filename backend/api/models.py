"""
API data models for SudokuSensei
"""

from pydantic import BaseModel, Field, validator
from typing import List


class PuzzleInput(BaseModel):
    """Input model for Sudoku puzzle"""

    puzzle: List[List[int]] = Field(
        ...,
        description="9x9 Sudoku grid with 0 for empty cells and 1-9 for filled cells",
    )

    @validator("puzzle")
    def validate_puzzle_format(cls, v):
        """Validate puzzle is 9x9 grid with valid values"""
        if len(v) != 9:
            raise ValueError("Puzzle must have exactly 9 rows")

        for i, row in enumerate(v):
            if len(row) != 9:
                raise ValueError(f"Row {i+1} must have exactly 9 columns")

            for j, val in enumerate(row):
                if not isinstance(val, int) or not (0 <= val <= 9):
                    raise ValueError(
                        f"Cell [{i+1},{j+1}] must be an integer between 0-9"
                    )

        return v


class SolveResponse(BaseModel):
    """Response model for solved puzzle"""

    solved_grid: List[List[int]] = Field(..., description="The solved 9x9 grid")
    is_solved: bool = Field(..., description="Whether the puzzle was completely solved")
    message: str = Field(..., description="Status message about the solving process")
    techniques_used: List[str] = Field(
        default=[], description="List of techniques applied"
    )


class ErrorDetail(BaseModel):
    """Detailed error information"""

    error: str = Field(..., description="Error title")
    error_type: str = Field(..., description="Error type identifier")
    message: str = Field(..., description="Detailed error message")
    suggestions: List[str] = Field(
        default=[], description="Helpful suggestions to fix the error"
    )


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")


class DetailedHealthResponse(BaseModel):
    """Detailed health check response"""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    endpoints: List[str] = Field(..., description="Available endpoints")
    cors_enabled: bool = Field(..., description="CORS configuration status")
    frontend_url: str = Field(..., description="Expected frontend URL")
