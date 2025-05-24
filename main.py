from helpers.print_board import print_board
from helpers.read_puzzle import read_puzzle
from helpers.check_solvable import check_solvable

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
board.display()
