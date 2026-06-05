from itertools import combinations

from helpers.get_location import get_cell_location
from models.technique_step import TechniqueStep
from utils.unit_processor import process_rows, process_columns


def apply_one_x_wing(board):
    """
    Apply one X-Wing step on the board.

    An X-Wing exists when a candidate is confined to the same two columns in
    exactly two different rows (a row-based X-Wing), or to the same two rows in
    exactly two different columns (a column-based X-Wing). The candidate forms
    the four corners of a rectangle, and can be eliminated from the rest of
    those two columns (or rows).

    Returns:
      changed (bool): True if any candidates were eliminated.
      step (TechniqueStep): Step description/details (or None if nothing changed)
    """
    board.update_candidates()

    def positions_with_candidate(cells, positions, num):
        """Positions (from this unit) where num is an unsolved candidate."""
        return [
            pos
            for cell, pos in zip(cells, positions)
            if not cell.is_solved() and num in cell.get_candidates()
        ]

    def build_step(corners, elimination_map):
        lines = []
        for cand, poses in elimination_map.items():
            locs = [get_cell_location(r, c) for (r, c) in poses]
            lines.append(f"Eliminated {cand} from {locs}")
        description = "X-Wing elimination:\n" + "\n".join(lines)
        eliminations = [{k: v} for k, v in elimination_map.items()]
        return TechniqueStep(
            technique="X-Wing",
            description=description,
            focus_cells=corners,
            value=None,
            eliminations=eliminations,
        )

    # --- Row-based X-Wing ---
    for num in range(1, 10):
        # Rows where num is a candidate in exactly two columns
        rows_with_pair = {}

        def collect_row(cells, positions, num=num):
            cols = [c for (_, c) in positions_with_candidate(cells, positions, num)]
            if len(cols) == 2:
                rows_with_pair[positions[0][0]] = tuple(cols)

        process_rows(board, collect_row)

        # Two rows sharing the same column pair form an X-Wing
        for r1, r2 in combinations(sorted(rows_with_pair), 2):
            if rows_with_pair[r1] != rows_with_pair[r2]:
                continue

            c1, c2 = rows_with_pair[r1]
            corners = [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]

            elimination_map = {}
            for col in (c1, c2):
                for row in range(9):
                    if row in (r1, r2):  # skip the X-Wing rows themselves
                        continue
                    cell = board.grid[row][col]
                    if not cell.is_solved() and num in cell.get_candidates():
                        cell.set_candidates(cell.get_candidates() - {num})
                        elimination_map.setdefault(str(num), []).append((row, col))

            if elimination_map:
                return True, build_step(corners, elimination_map)

    # --- Column-based X-Wing ---
    for num in range(1, 10):
        # Columns where num is a candidate in exactly two rows
        cols_with_pair = {}

        def collect_col(cells, positions, num=num):
            rows = [r for (r, _) in positions_with_candidate(cells, positions, num)]
            if len(rows) == 2:
                cols_with_pair[positions[0][1]] = tuple(rows)

        process_columns(board, collect_col)

        # Two columns sharing the same row pair form an X-Wing
        for c1, c2 in combinations(sorted(cols_with_pair), 2):
            if cols_with_pair[c1] != cols_with_pair[c2]:
                continue

            r1, r2 = cols_with_pair[c1]
            corners = [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]

            elimination_map = {}
            for row in (r1, r2):
                for col in range(9):
                    if col in (c1, c2):  # skip the X-Wing columns themselves
                        continue
                    cell = board.grid[row][col]
                    if not cell.is_solved() and num in cell.get_candidates():
                        cell.set_candidates(cell.get_candidates() - {num})
                        elimination_map.setdefault(str(num), []).append((row, col))

            if elimination_map:
                return True, build_step(corners, elimination_map)

    return False, None


def apply_all_x_wings(board):
    """
    Apply X-Wing repeatedly until no more changes.
    Returns:
      changed (bool): True if any candidates were eliminated.
      steps (list): List of TechniqueStep objects for each application
    """
    changed = False
    steps = []
    while True:
        step_changed, step = apply_one_x_wing(board)
        if not step_changed:
            break
        changed = True
        steps.append(step)
    return changed, steps
