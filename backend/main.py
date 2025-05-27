from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from board.board import SudokuBoard
from logic.naked_single import apply_all_naked_singles
from logic.hidden_single import apply_all_hidden_singles
from logic.hidden_pairs import apply_all_hidden_pairs
from logic.naked_pairs import apply_all_naked_pairs  # <-- Import naked pairs here

app = FastAPI()


class PuzzleInput(BaseModel):
    puzzle: List[List[int]]  # 9x9 grid


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


@app.post("/solve")
def solve_sudoku(data: PuzzleInput):
    if not is_valid_puzzle(data.puzzle):
        raise HTTPException(status_code=400, detail="Invalid puzzle format")

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
        "incomplete_cells": incomplete_cells,
        "message": message,
    }
