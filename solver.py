from utilities.check_solvable import check_solvable
from utilities.naked_single import apply_naked_singles


def read_puzzle(filename):
    board = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if len(line) == 9 and line.isdigit():
                row = [int(c) for c in line]
                board.append(row)
    return board


def print_board(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        row_str = ""
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += " | "
            row_str += str(num) if num != 0 else "."
            row_str += " "
        print(row_str)


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
