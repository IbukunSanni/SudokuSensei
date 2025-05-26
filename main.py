from helpers.print_board import print_board
from helpers.read_puzzle import read_puzzle
from helpers.check_solvable import check_solvable

from logic.naked_single import apply_one_naked_single, apply_all_naked_singles

from board.board import SudokuBoard

puzzle = read_puzzle("test_puzzles/puzzle.txt")
print("Initial Puzzle:")
print_board(puzzle)

if check_solvable(puzzle):
    print("Puzzle is solvable! Starting solving steps...")
    # You can add your human-like solving logic here
else:
    print("Puzzle is NOT solvable. Please check the input.")
    exit()

board = SudokuBoard(puzzle)
board.display_simple()
print("*" * 30)
print("Diplaying with candidates:")
board.display_with_candidates()

changed = apply_all_naked_singles(board)
if changed:
    print("\nBoard after applying all naked singles:")
    print_board(board)
else:
    print("No naked singles found on this board.")
