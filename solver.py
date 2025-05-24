from utilities.check_solvable import check_solvable
from utilities.naked_single import apply_naked_singles
from utilities.read_puzzle import read_puzzle


if __name__ == "__main__":
    puzzle = read_puzzle("test_puzzles/puzzle.txt")
    print("Initial Puzzle:")
    print_board(puzzle)

    if check_solvable(puzzle):
        print("Puzzle is solvable! Starting solving steps...")
        # You can add your human-like solving logic here
    else:
        print("Puzzle is NOT solvable. Please check the input.")
        exit()
    print("Applying Naked Singles Technique...")
    changed = True
    while changed:
        puzzle, changed = apply_naked_singles(puzzle)
        print_board(puzzle)
        print("*" * 30)

    print("Solved Puzzle:")
