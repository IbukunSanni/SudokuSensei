from helpers.get_location import get_cell_location
from models.technique_step import TechniqueStep


def apply_one_box_line_reduction(board):
    """
    Apply one Box-Line Reduction (Claiming) step on the board.

    This is the inverse of Pointing Pairs: when a candidate within a row or
    column is restricted to a single 3x3 box, that candidate can be eliminated
    from all other cells in that box outside the row/column.

    Returns:
      changed (bool): True if any candidates were eliminated.
      step (TechniqueStep): Step description/details (or None if nothing changed)
    """
    board.update_candidates()

    # --- Check rows ---
    for row in range(9):
        for num in range(1, 10):
            # Find all positions in this row where num is a candidate
            positions = [
                col for col in range(9)
                if not board.grid[row][col].is_solved()
                and num in board.grid[row][col].get_candidates()
            ]

            if len(positions) < 2:
                continue

            # Are all positions confined to the same box?
            box_cols = {col // 3 for col in positions}
            if len(box_cols) != 1:
                continue

            # Claiming: eliminate num from the rest of this box (other rows)
            bc = next(iter(box_cols))   # box column index (0-2)
            br = row // 3               # box row index (0-2)

            changed = False
            focus_cells = [(row, col) for col in positions]
            elimination_map = {}

            for dr in range(3):
                r = br * 3 + dr
                if r == row:            # skip the claiming row itself
                    continue
                for dc in range(3):
                    c = bc * 3 + dc
                    cell = board.grid[r][c]
                    if not cell.is_solved() and num in cell.get_candidates():
                        cell.set_candidates(cell.get_candidates() - {num})
                        elimination_map.setdefault(str(num), []).append((r, c))
                        changed = True

            if changed:
                lines = []
                for cand, poses in elimination_map.items():
                    locs = [get_cell_location(r, c) for (r, c) in poses]
                    lines.append(f"Eliminated {cand} from {locs}")
                description = "Box-Line Reduction elimination:\n" + "\n".join(lines)
                eliminations = [{k: v} for k, v in elimination_map.items()]

                step = TechniqueStep(
                    technique="Box-Line Reduction",
                    description=description,
                    focus_cells=focus_cells,
                    value=None,
                    eliminations=eliminations,
                )
                return True, step

    # --- Check columns ---
    for col in range(9):
        for num in range(1, 10):
            positions = [
                row for row in range(9)
                if not board.grid[row][col].is_solved()
                and num in board.grid[row][col].get_candidates()
            ]

            if len(positions) < 2:
                continue

            box_rows = {row // 3 for row in positions}
            if len(box_rows) != 1:
                continue

            br = next(iter(box_rows))   # box row index (0-2)
            bc = col // 3               # box column index (0-2)

            changed = False
            focus_cells = [(row, col) for row in positions]
            elimination_map = {}

            for dr in range(3):
                r = br * 3 + dr
                for dc in range(3):
                    c = bc * 3 + dc
                    if c == col:        # skip the claiming column itself
                        continue
                    cell = board.grid[r][c]
                    if not cell.is_solved() and num in cell.get_candidates():
                        cell.set_candidates(cell.get_candidates() - {num})
                        elimination_map.setdefault(str(num), []).append((r, c))
                        changed = True

            if changed:
                lines = []
                for cand, poses in elimination_map.items():
                    locs = [get_cell_location(r, c) for (r, c) in poses]
                    lines.append(f"Eliminated {cand} from {locs}")
                description = "Box-Line Reduction elimination:\n" + "\n".join(lines)
                eliminations = [{k: v} for k, v in elimination_map.items()]

                step = TechniqueStep(
                    technique="Box-Line Reduction",
                    description=description,
                    focus_cells=focus_cells,
                    value=None,
                    eliminations=eliminations,
                )
                return True, step

    return False, None


def apply_all_box_line_reductions(board):
    """
    Apply Box-Line Reduction repeatedly until no more changes.
    Returns:
      changed (bool): True if any candidates were eliminated.
      steps (list): List of TechniqueStep objects for each application
    """
    changed = False
    steps = []
    while True:
        step_changed, step = apply_one_box_line_reduction(board)
        if not step_changed:
            break
        changed = True
        steps.append(step)
    return changed, steps
