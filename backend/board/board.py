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

    def get_peer_positions(self, r: int, c: int) -> set[tuple[int, int]]:
        """
        Return all (row,col) positions that share a row, column, or box with (r,c), excluding (r,c) itself.
        """
        peers = set()
        # same row & column
        peers.update((r, i) for i in range(9) if i != c)
        peers.update((i, c) for i in range(9) if i != r)
        # same 3×3 box
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for rr in range(br, br + 3):
            for cc in range(bc, bc + 3):
                if (rr, cc) != (r, c):
                    peers.add((rr, cc))
        return peers

    def update_candidates_for_cells(self, positions):
        """
        Update candidates for a list of (row, col) positions based on current board state.
        Returns a list of candidate-change dicts for tracking/explanation.
        """
        changes = []
        for r, c in positions:
            cell = self.grid[r][c]
            if cell.is_solved():
                continue
            used_values = (
                {peer.get_value() for peer in self.get_row(r) if peer.is_solved()}
                | {peer.get_value() for peer in self.get_col(c) if peer.is_solved()}
                | {peer.get_value() for peer in self.get_box(r, c) if peer.is_solved()}
            )
            old = cell.get_candidates()
            new = old - used_values
            if new != old:
                cell.set_candidates(new)
                eliminated = old - new
                changes.append(
                    {
                        "position": (r, c),
                        "location": get_cell_location(r, c),
                        "old_candidates": old,
                        "new_candidates": new,
                        "eliminated": eliminated,
                    }
                )
                print(
                    f"Updated candidates at {get_cell_location(r, c)}: {old} -> {new}"
                )
        return changes

    def update_candidates(self):
        """
        Update candidates for all cells on the board.
        Returns a list of all candidate changes.
        """
        all_positions = [(r, c) for r in range(9) for c in range(9)]
        return self.update_candidates_for_cells(all_positions)

    def update_peers_candidates(self, r, c, value):
        """
        After setting a value at (r, c), remove `value` from candidates
        of all peer cells in the same row, column, and 3×3 box.
        Returns the list of changes made.
        """
        peers = self.get_peer_positions(r, c)
        changes = []
        for pr, pc in peers:
            peer = self.grid[pr][pc]
            if not peer.is_solved():
                old = peer.get_candidates()
                new = old - {value}
                if new != old:
                    peer.set_candidates(new)
                    eliminated = old - new
                    changes.append(
                        {
                            "position": (pr, pc),
                            "location": get_cell_location(pr, pc),
                            "old_candidates": old,
                            "new_candidates": new,
                            "eliminated": eliminated,
                        }
                    )
                    print(
                        f"Updated candidates at {get_cell_location(pr, pc)}: {old} -> {new}"
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
            return [
                "".join(str(i) if i in candidates else "." for i in range(1, 4)),
                "".join(str(i) if i in candidates else "." for i in range(4, 7)),
                "".join(str(i) if i in candidates else "." for i in range(7, 10)),
            ]

        def format_value(value):
            return ["...", f".{value}.", "..."]

        num_rows = len(self.grid)
        num_cols = len(self.grid[0]) if num_rows > 0 else 0
        sub_rows = []

        for r in range(num_rows):
            row_lines = ["", "", ""]
            for c in range(num_cols):
                cell = self.grid[r][c]
                cell_grid = (
                    format_value(cell.get_value())
                    if cell.is_solved()
                    else format_candidates(cell.get_candidates())
                )
                for i in range(3):
                    row_lines[i] += cell_grid[i]
                    row_lines[i] += " || " if c in [2, 5] else " | "
            sub_rows.extend(row_lines)
            sub_rows.append(
                "=" * (num_cols * 6 + 1) if r in [2, 5, 8] else "-" * (num_cols * 6 + 1)
            )

        for sub_row in sub_rows:
            print(sub_row)

    def get_candidates_grid(self):
        """
        Returns a 9x9 grid of candidate sets for each cell.
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
