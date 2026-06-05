from helpers.get_location import get_cell_location
from models.technique_step import TechniqueStep


def apply_one_pointing_pair(board):
    """
    Apply one Pointing Pairs / Triples step on the board.

    When a candidate within a 3x3 box is restricted to a single row or
    column inside that box, it can be eliminated from all other cells in
    that row or column outside the box.

    Handles both pointing pairs (2 cells) and pointing triples (3 cells).

    Returns:
      changed (bool): True if any candidates were eliminated.
      step (TechniqueStep): Step description/details (or None if nothing changed)
    """
    board.update_candidates()

    for br in range(3):        # box row index (0-2)
        for bc in range(3):    # box col index (0-2)

            # Collect cells and positions for this box
            box_cells = []
            box_positions = []
            for dr in range(3):
                for dc in range(3):
                    r = br * 3 + dr
                    c = bc * 3 + dc
                    box_cells.append(board.grid[r][c])
                    box_positions.append((r, c))

            for num in range(1, 10):
                # Positions inside this box where num is a candidate
                pointing_positions = [
                    box_positions[i]
                    for i, cell in enumerate(box_cells)
                    if not cell.is_solved() and num in cell.get_candidates()
                ]

                if len(pointing_positions) < 2:
                    continue

                changed = False
                focus_cells = list(pointing_positions)
                elimination_map = {}

                # --- Pointing via row ---
                rows = {r for r, c in pointing_positions}
                if len(rows) == 1:
                    target_row = next(iter(rows))
                    for col in range(9):
                        if col // 3 == bc:   # skip cells inside the same box
                            continue
                        cell = board.grid[target_row][col]
                        if not cell.is_solved() and num in cell.get_candidates():
                            cands = cell.get_candidates()
                            cell.set_candidates(cands - {num})
                            elimination_map.setdefault(str(num), []).append(
                                (target_row, col)
                            )
                            changed = True

                # --- Pointing via column ---
                cols = {c for r, c in pointing_positions}
                if len(cols) == 1:
                    target_col = next(iter(cols))
                    for row in range(9):
                        if row // 3 == br:   # skip cells inside the same box
                            continue
                        cell = board.grid[row][target_col]
                        if not cell.is_solved() and num in cell.get_candidates():
                            cands = cell.get_candidates()
                            cell.set_candidates(cands - {num})
                            elimination_map.setdefault(str(num), []).append(
                                (row, target_col)
                            )
                            changed = True

                if changed:
                    lines = []
                    for cand, poses in elimination_map.items():
                        locs = [get_cell_location(r, c) for (r, c) in poses]
                        lines.append(f"Eliminated {cand} from {locs}")
                    description = "Pointing Pairs/Triples elimination:\n" + "\n".join(lines)
                    eliminations = [{k: v} for k, v in elimination_map.items()]

                    step = TechniqueStep(
                        technique="Pointing Pairs",
                        description=description,
                        focus_cells=focus_cells,
                        value=None,
                        eliminations=eliminations,
                    )
                    return True, step

    return False, None


def apply_all_pointing_pairs(board):
    """
    Apply Pointing Pairs / Triples repeatedly until no more changes.
    Returns:
      changed (bool): True if any candidates were eliminated.
      steps (list): List of TechniqueStep objects for each application
    """
    changed = False
    steps = []
    while True:
        step_changed, step = apply_one_pointing_pair(board)
        if not step_changed:
            break
        changed = True
        steps.append(step)
    return changed, steps
