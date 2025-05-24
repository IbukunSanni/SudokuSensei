from .cell import Cell


class SudokuBoard:
    def __init__(self, grid):  # grid is a 9x9 list of lists
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
        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]
                if cell.is_solved():
                    continue

                used_values = (
                    {c2.value for c2 in self.get_row(r) if c2.is_solved()}
                    | {c2.value for c2 in self.get_col(c) if c2.is_solved()}
                    | {c2.value for c2 in self.get_box(r, c) if c2.is_solved()}
                )

                old_candidates = cell.get_candidates().copy()
                cell.set_candidates(cell.get_candidates() - used_values)

                if old_candidates != cell.candidates:
                    print(
                        f"Updated candidates at ({r},{c}): {old_candidates} → {cell.candidates}"
                    )

    def display(self):
        for i, row in enumerate(self.grid):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            print(
                " ".join(
                    str(cell) if (j + 1) % 3 else f"{cell} |"
                    for j, cell in enumerate(row)
                )
            )
