from helpers.get_location import get_cell_location
from logic.technique_step import TechniqueStep


def apply_one_naked_pair(board):
    """
    Apply one naked pair technique on the board.
    Returns:
      changed (bool): True if any candidates were eliminated.
      step (TechniqueStep): Step description/details (or None if nothing changed)
    """
    # Ensure candidates are up to date
    # TODO: might remove as the technique should already eleimante candidates
    board.update_candidates()

    # Snapshot candidates before elimination
    prev_candidates = board.get_candidates_grid()
    changed = False
    focus_cells = []
    elimination_map = {}  # str(candidate) -> list of (r,c)

    def process_unit(cells, positions):
        nonlocal changed, focus_cells, elimination_map
        # Find all cells with exactly 2 candidates
        pairs = {}
        for idx, cell in enumerate(cells):
            if not cell.is_solved():
                cands = cell.get_candidates()
                if len(cands) == 2:
                    key = tuple(sorted(cands))
                    pairs.setdefault(key, []).append(idx)
        # For each candidate pair that appears in exactly two cells
        for key, idxs in pairs.items():
            if len(idxs) == 2:
                to_remove = set(key)
                # Eliminate from other cells in unit
                for idx, cell in enumerate(cells):
                    if idx not in idxs and not cell.is_solved():
                        old = cell.get_candidates()
                        new = old - to_remove
                        if new != old:
                            cell.set_candidates(new)
                            changed = True
                            pos = positions[idx]
                            for v in old - new:
                                elimination_map.setdefault(str(v), []).append(pos)
                # Mark the pair cells for focus/highlight
                for idx in idxs:
                    focus_cells.append(positions[idx])

    # Process all rows
    for r in range(9):
        row_cells = board.get_row(r)
        row_positions = [(r, c) for c in range(9)]
        process_unit(row_cells, row_positions)
    # Process all columns
    for c in range(9):
        col_cells = board.get_col(c)
        col_positions = [(r, c) for r in range(9)]
        process_unit(col_cells, col_positions)
    # Process all 3x3 boxes
    for br in range(3):
        for bc in range(3):
            box_cells = []
            box_positions = []
            for dr in range(3):
                for dc in range(3):
                    r = br * 3 + dr
                    c = bc * 3 + dc
                    box_cells.append(board.grid[r][c])
                    box_positions.append((r, c))
            process_unit(box_cells, box_positions)

    if not changed:
        return False, None

    # Build human-readable description
    lines = []
    for cand, poses in elimination_map.items():
        locs = [get_cell_location(r, c) for (r, c) in poses]
        lines.append(f"Eliminated {cand} from {locs}")
    description = "Naked Pair elimination:\n" + "\n".join(lines)
    eliminations = [{k: v} for k, v in elimination_map.items()]

    step = TechniqueStep(
        technique="Naked Pair",
        description=description,
        focus_cells=focus_cells,
        value=None,
        eliminations=eliminations,
    )
    return True, step


def apply_all_naked_pairs(board):
    """
    Apply naked pairs repeatedly until no more changes.
    Returns:
      changed (bool): True if any candidates were eliminated during the process.
      steps (list): List of TechniqueStep objects for each application
    """
    changed = False
    steps = []
    while True:
        step_changed, step = apply_one_naked_pair(board)
        if not step_changed:
            break
        changed = True
        steps.append(step)
    return changed, steps
