from helpers.get_location import get_cell_location
from logic.technique_step import TechniqueStep
from logic.unit_processor import process_all_units


def apply_one_hidden_single(board):
    """
    Apply hidden single technique once on the board.
    Returns:
      changed (bool): True if a cell was filled
      step (TechniqueStep): Detailed information for this step (or None if no fill)
    """
    board.update_candidates()

    def find_hidden_single_in_unit(cells):
        # Count candidate occurrences in the unit
        candidate_positions = {n: [] for n in range(1, 10)}
        for idx, cell in enumerate(cells):
            if not cell.is_solved():
                for c in cell.get_candidates():
                    candidate_positions[c].append(idx)
        # Hidden single if a candidate appears exactly once
        for num, positions in candidate_positions.items():
            if len(positions) == 1:
                return positions[0], num
        return None, None

    def create_step(r, c, value):
        # Snapshot full-board candidates before elimination
        prev = {
            (pr, pc): board.get_candidates_grid()[pr][pc].copy()
            for pr in range(9)
            for pc in range(9)
        }
        # Place the hidden single
        board.grid[r][c].set_value(value)
        board.grid[r][c].set_candidates(set())
        board.update_peers_candidates(r, c, value)
        # Compute eliminations
        elim_map = {}
        for pr in range(9):
            for pc in range(9):
                if (pr, pc) == (r, c):
                    continue
                before = prev[(pr, pc)]
                after = board.grid[pr][pc].get_candidates()
                removed = before - after
                for v in removed:
                    elim_map.setdefault(str(v), []).append((pr, pc))
        eliminations = [{k: v} for k, v in elim_map.items()]
        # Build description
        loc = get_cell_location(r, c)
        elimination_text = (
            "Eliminated: "
            + "; ".join(
                f"{cand} from "
                + ", ".join(get_cell_location(pr, pc) for pr, pc in positions)
                for entry in eliminations
                for cand, positions in entry.items()
            )
            if eliminations
            else "No eliminations."
        )
        description = (
            f"Hidden Single in cell {loc}\n"
            f"Only possible value for this unit is {value}\n"
            f"Filled {loc}={value}; {elimination_text}"
        )
        return TechniqueStep(
            technique="Hidden Single",
            description=description,
            focus_cells=[(r, c)],
            value=value,
            eliminations=eliminations,
        )

    # Track if we found a hidden single
    found_result = [None]  # Use list to allow modification in nested function

    def process_unit(cells, positions):
        if found_result[0] is not None:  # Already found one, skip processing
            return
        pos, value = find_hidden_single_in_unit(cells)
        if pos is not None:
            r, c = positions[pos]
            found_result[0] = (True, create_step(r, c, value))

    # Process all units using shared utility
    process_all_units(board, process_unit)

    # Return result if found, otherwise no hidden single
    if found_result[0] is not None:
        return found_result[0]

    return False, None


def apply_all_hidden_singles(board):
    """
    Repeatedly apply hidden single until no more changes.
    Returns:
      changed (bool), steps (list of TechniqueStep)
    """
    changed = False
    steps = []
    while True:
        step_changed, step = apply_one_hidden_single(board)
        if not step_changed:
            break
        changed = True
        steps.append(step)
    return changed, steps
