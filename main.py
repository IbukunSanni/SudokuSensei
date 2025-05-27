from helpers.print_board import print_input_puzzle
from helpers.read_puzzle import read_puzzle
from helpers.check_solvable import check_solvable

from logic.naked_single import apply_all_naked_singles
from logic.hidden_single import apply_all_hidden_singles
from logic.hidden_pairs import apply_all_hidden_pairs
from logic.naked_pairs import apply_all_naked_pairs  # <-- Import naked pairs here

from board.board import SudokuBoard


def main():
    puzzle = read_puzzle("test_puzzles/puzzle_hidden_pairs.txt")
    print("Initial Puzzle:")
    print_input_puzzle(puzzle)

    if not check_solvable(puzzle):
        print("Puzzle is NOT solvable. Please check the input.")
        return

    print("Puzzle is solvable! Starting solving steps...\n")

    board = SudokuBoard(puzzle)
    board.display_simple()
    print("*" * 30)
    print("Displaying with candidates:")
    board.display_with_candidates()

    # Add is_solved method if not present
    if not hasattr(board, "is_solved"):

        def is_solved(self):
            for r in range(9):
                for c in range(9):
                    if not self.grid[r][c].is_solved():
                        return False
            return True

        setattr(SudokuBoard, "is_solved", is_solved)

    while True:
        any_changed = False

        changed = apply_all_naked_singles(board)
        if changed:
            print("\nBoard after applying all naked singles:")
            board.display_simple()
            any_changed = True
        else:
            print("No naked singles found on this board.")

        changed = apply_all_hidden_singles(board)
        if changed:
            print("\nBoard after applying hidden singles:")
            board.display_simple()
            any_changed = True
        else:
            print("No hidden singles found.")

        changed = apply_all_hidden_pairs(board)
        if changed:
            print("\nBoard after applying hidden pairs:")
            board.display_simple()
            any_changed = True
        else:
            print("No hidden pairs found.")

        changed = apply_all_naked_pairs(board)  # <-- Apply naked pairs here
        if changed:
            print("\nBoard after applying naked pairs:")
            board.display_simple()
            any_changed = True
        else:
            print("No naked pairs found.")

        if board.is_solved():
            print("\nPuzzle solved successfully!")
            break

        if not any_changed:
            print("\nNo more techniques can be applied. Stopping.")
            break

    print("\nFinal board state:")
    board.display_simple()


if __name__ == "__main__":
    main()
