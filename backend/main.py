from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from board.board import SudokuBoard
from logic.naked_single import apply_all_naked_singles
from logic.hidden_single import apply_all_hidden_singles
from logic.hidden_pairs import apply_all_hidden_pairs
from logic.naked_pairs import apply_all_naked_pairs  # <-- Import naked pairs here
from helpers.check_solvable import check_solvable
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="SudokuSensei API",
    version="1.0",
    json_indent=2,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PuzzleInput(BaseModel):
    puzzle: List[List[int]]  # 9x9 grid


class ErrorResponse(BaseModel):
    error: str
    error_type: str
    message: str
    suggestions: List[str] = []


def is_valid_puzzle(puzzle: List[List[int]]) -> bool:
    # Basic validation: 9x9 grid with digits 0-9
    if len(puzzle) != 9:
        return False
    for row in puzzle:
        if len(row) != 9:
            return False
        for val in row:
            if not (0 <= val <= 9):
                return False
    return True


def has_unique_solution(puzzle: List[List[int]]) -> bool:
    """
    Check if the puzzle has exactly one unique solution.
    Returns True if unique, False if multiple solutions exist.
    """

    def get_candidates(board, row, col):
        used = set()
        # Check row
        used.update(board[row])
        # Check column
        used.update(board[r][col] for r in range(9))
        # Check 3x3 box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                used.add(board[r][c])
        return [n for n in range(1, 10) if n not in used]

    def find_empty_cell(board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return None

    def count_solutions(board, max_solutions=2):
        """Count solutions up to max_solutions (for efficiency)"""
        cell = find_empty_cell(board)
        if not cell:
            return 1  # Found a complete solution

        row, col = cell
        solution_count = 0

        for num in get_candidates(board, row, col):
            board[row][col] = num
            solution_count += count_solutions(board, max_solutions)
            board[row][col] = 0  # backtrack

            # Early exit if we find more than one solution
            if solution_count >= max_solutions:
                return solution_count

        return solution_count

    # Create a copy to avoid modifying the original
    board_copy = [row[:] for row in puzzle]
    solution_count = count_solutions(board_copy, max_solutions=2)

    return solution_count == 1


@app.get("/")
def health_check():
    return {"status": "SudokuSensei backend is running!", "version": "1.0"}


@app.get("/health")
def detailed_health():
    return {
        "status": "healthy",
        "service": "SudokuSensei API",
        "endpoints": ["/", "/health", "/solve"],
        "cors_enabled": True,
        "frontend_url": "http://localhost:3000",
    }


@app.post("/solve")
def solve_sudoku(data: PuzzleInput):
    if not is_valid_puzzle(data.puzzle):
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

    # Check if puzzle is solvable before attempting logical techniques
    if not check_solvable(data.puzzle):
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

    # Check if puzzle has a unique solution (important for educational purposes)
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

    board = SudokuBoard(data.puzzle)

    changed = True
    while changed:
        changed = False
        if apply_all_naked_singles(board):
            changed = True
        if apply_all_hidden_singles(board):
            changed = True
        if apply_all_hidden_pairs(board):
            changed = True
        if apply_all_naked_pairs(board):  # naked pairs applied here
            changed = True

    solved_grid = [[cell.get_value() for cell in row] for row in board.grid]

    message = (
        "Puzzle solved successfully!"
        if board.is_solved()
        else "Partial solution after applying techniques"
    )

    return {
        "solved_grid": solved_grid,
        "is_solved": board.is_solved(),
        "message": message,
    }
