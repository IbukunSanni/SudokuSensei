from helpers.get_location import get_cell_location
from models.technique_step import TechniqueStep


def apply_one_naked_single(board):
    """
    Apply naked single technique once on the board.
    Returns:
      changed (bool): True if a cell was filled
      step (TechniqueStep): Detailed information for this step (or None if no fill)
    """
    # Refresh all candidates before scanning
    board.update_candidates()

    for r in range(9):
        for c in range(9):
            cell = board.grid[r][c]
            if not cell.is_solved():
                candidates = cell.get_candidates()
                # Naked single found
                if len(candidates) == 1:
                    value = next(iter(candidates))
                    # Snapshot full-board candidates before elimination
                    prev_candidates = {
                        (pr, pc): board.get_candidates_grid()[pr][pc].copy()
                        for pr in range(9)
                        for pc in range(9)
                    }
                    # Place the value and clear candidates
                    cell.set_value(value)
                    cell.set_candidates(set())
                    # Eliminate from peers
                    board.update_peers_candidates(r, c, value)

                    # Compute exactly which candidates were removed
                    elimination_map = {}
                    for pr in range(9):
                        for pc in range(9):
                            if (pr, pc) == (r, c):
                                continue
                            before = prev_candidates[(pr, pc)]
                            after = board.grid[pr][pc].get_candidates()
                            removed = before - after
                            for v in removed:
                                elimination_map.setdefault(str(v), []).append((pr, pc))
                    eliminations = [{k: v} for k, v in elimination_map.items()]

                    # Build human-readable description
                    loc_str = get_cell_location(r, c)
                    description = (
                        f"Naked Single in cell {loc_str}\n"
                        f"Only candidate is {value}\n"
                        f"Filled {loc_str}={value}; "
                        + (
                            "Eliminated: "
                            + "; ".join(
                                f"{cand} from "
                                + ", ".join(
                                    get_cell_location(pr, pc) for pr, pc in cells
                                )
                                for e in eliminations
                                for cand, cells in e.items()
                            )
                            if eliminations
                            else "No eliminations needed."
                        )
                    )

                    # Create step object
                    step = TechniqueStep(
                        technique="Naked Single",
                        description=description,
                        focus_cells=[(r, c)],
                        value=value,
                        eliminations=eliminations,
                    )
                    return True, step
    # No naked single found
    return False, None


def apply_all_naked_singles(board):
    """
    Repeatedly apply naked single until no more changes.
    Returns:
      changed (bool): True if any cell was filled during the process
      steps (list): List of TechniqueStep objects for each fill
    """
    changed = False
    steps = []
    while True:
        step_changed, step = apply_one_naked_single(board)
        if not step_changed:
            break
        changed = True
        steps.append(step)
    return changed, steps
