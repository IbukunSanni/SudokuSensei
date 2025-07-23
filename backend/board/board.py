from .cell import Cell
from helpers.get_location import get_cell_location


class SudokuBoard:
    def __init__(self, grid):  # grid is a 9x9 list of lists of integers
        self.grid = [[Cell(val, is_initial=(val != 0)) for val in row] for row in grid]

    def get_row(self, r):
        return self.grid[r]

    def get_col(self, c):
        return [self.grid[r][c] for r in range(9)]

    def get_box(self, r, c):
        start_row, start_col = 3 * (r // 3), 3 * (c // 3)
        return [
            self.grid[i][j]
            for i in range(start_row, start_row + 3)
            for j in range(start_col, start_col + 3)
        ]

    def update_candidates(self):
        """
        Update candidates for all cells based on current board state.
        Returns a list of changes made to candidates for tracking purposes.
        """
        changes = []
        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]
                if cell.is_solved():
                    continue

                used_values = (
                    {c2.get_value() for c2 in self.get_row(r) if c2.is_solved()}
                    | {c2.get_value() for c2 in self.get_col(c) if c2.is_solved()}
                    | {c2.get_value() for c2 in self.get_box(r, c) if c2.is_solved()}
                )

                old_candidates = cell.get_candidates().copy()
                cell.set_candidates(cell.get_candidates() - used_values)

                if old_candidates != cell.get_candidates():
                    eliminated = old_candidates - cell.get_candidates()
                    changes.append(
                        {
                            "position": (r, c),
                            "location": get_cell_location(r, c),
                            "old_candidates": old_candidates,
                            "new_candidates": cell.get_candidates().copy(),
                            "eliminated": eliminated,
                        }
                    )
                    # Debug output showing candidate updates (using standard A1-I9 notation)
                    print(
                        f"Updated candidates at {get_cell_location(r, c)}: {old_candidates} → {cell.get_candidates()}"
                    )
        return changes

    def display_simple(self):
        for i, row in enumerate(self.grid):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            print(
                " ".join(
                    str(cell) if (j + 1) % 3 else f"{cell} |"
                    for j, cell in enumerate(row)
                )
            )

    def display_with_candidates(self):
        def format_candidates(candidates):
            """
            Returns a list of 3 strings representing the candidate mini-grid:
            1 2 3
            4 5 6
            7 8 9
            Shows '.' where a candidate is missing.
            """
            return [
                "".join(str(i) if i in candidates else "." for i in range(1, 4)),
                "".join(str(i) if i in candidates else "." for i in range(4, 7)),
                "".join(str(i) if i in candidates else "." for i in range(7, 10)),
            ]

        def format_value(value):
            """Center a solved value in the middle of a 3x3 space"""
            return ["...", f".{value}.", "..."]

        num_rows = len(self.grid)
        num_cols = len(self.grid[0]) if num_rows > 0 else 0
        sub_rows = []

        for r in range(num_rows):
            # Each full row of cells will produce 3 display lines
            row_lines = ["", "", ""]

            for c in range(num_cols):
                cell = self.grid[r][c]

                # Choose how to render this cell: either its value or its candidates
                cell_grid = (
                    format_value(cell.get_value())
                    if cell.is_solved()
                    else format_candidates(cell.get_candidates())
                )

                # Add the mini-grid lines to the current row_lines
                for i in range(3):
                    row_lines[i] += cell_grid[i]
                    row_lines[i] += " || " if c in [2, 5] else " | "

            # Add the 3 constructed lines to the output
            sub_rows.extend(row_lines)

            # After every 3 rows, add a thick or thin horizontal border
            if r in [2, 5, 8]:
                sub_rows.append("=" * (num_cols * 6 + 1))
            else:
                sub_rows.append("-" * (num_cols * 6 + 1))

        # Print the full board display
        for sub_row in sub_rows:
            print(sub_row)

    def get_candidates_grid(self):
        """
        Returns a 9x9 grid of candidate sets for each cell.
        This is useful for tracking the state of candidates at each step.
        """
        return [[cell.get_candidates().copy() for cell in row] for row in self.grid]

    def is_solved(self):
        """
        Check if the board is completely solved and valid.
        """
        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]
                if not cell.is_solved():
                    return False

                val = cell.get_value()
                # Check row uniqueness
                row_vals = [self.grid[r][j].get_value() for j in range(9) if j != c]
                if val in row_vals:
                    return False
                # Check column uniqueness
                col_vals = [self.grid[i][c].get_value() for i in range(9) if i != r]
                if val in col_vals:
                    return False
                # Check box uniqueness
                start_r = (r // 3) * 3
                start_c = (c // 3) * 3
                box_vals = [
                    self.grid[i][j].get_value()
                    for i in range(start_r, start_r + 3)
                    for j in range(start_c, start_c + 3)
                    if (i, j) != (r, c)
                ]
                if val in box_vals:
                    return False

        return True
