from helpers.print_board import print_input_puzzle
from helpers.read_puzzle import read_puzzle
from helpers.check_solvable import check_solvable

from logic.naked_single import apply_all_naked_singles
from logic.hidden_single import apply_all_hidden_singles

from board.board import SudokuBoard

puzzle = read_puzzle("test_puzzles/puzzle_hidden_single.txt")
print("Initial Puzzle:")
print_input_puzzle(puzzle)

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
else:
    print("No naked singles found on this board.")

board.display_simple()

# Now try applying hidden singles
changed = apply_all_hidden_singles(board)
if changed:
    print("\nBoard after applying hidden singles:")
else:
    print("No hidden singles found.")

board.display_simple()
