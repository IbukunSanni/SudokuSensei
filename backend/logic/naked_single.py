# logic/naked_single.py
from helpers.get_location import get_cell_location
from logic.technique_step import TechniqueStep


def apply_one_naked_single(board):
    """
    Apply naked single technique once on the board.
    Returns:
      changed (bool): True if a cell was filled
      step (TechniqueStep): Detailed information for this step (or None if no fill)
    """
    board.update_candidates()  # update candidates for all cells

    for r in range(9):
        for c in range(9):
            cell = board.grid[r][c]
            if not cell.is_solved():
                candidates = cell.get_candidates()
                if len(candidates) == 1:
                    value = next(iter(candidates))
                    prev_candidates = {
                        (pr, pc): set(board.grid[pr][pc].get_candidates())
                        for pr in range(9)
                        for pc in range(9)
                    }
                    cell.set_value(value)
                    cell.set_candidates(set())
                    board.update_peers_candidates(r, c, value)
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
                    location_str = get_cell_location(r, c)
                    description = (
                        f"Naked Single in cell {location_str}\n"
                        f"Only candidate is {value}\n"
                        f"Filled {location_str}={value}; "
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
                    step = TechniqueStep(
                        technique="Naked Single",
                        description=description,
                        focus_cells=[(r, c)],
                        value=value,
                        eliminations=eliminations,
                    )
                    return True, step
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
