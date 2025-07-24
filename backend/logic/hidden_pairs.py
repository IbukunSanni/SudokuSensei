from helpers.get_location import get_cell_location
from logic.technique_step import TechniqueStep
from logic.unit_processor import process_all_units


def apply_one_hidden_pair(board):
    """
    Apply one hidden pair technique on the board.
    Returns:
      changed (bool): True if any candidates were eliminated.
      step (TechniqueStep): Step description/details (or None if nothing changed)
    """
    # Ensure candidates are up to date
    board.update_candidates()

    changed = False
    focus_cells = []
    elimination_map = {}  # str(candidate) -> list of (r,c)

    def process_unit(cells, positions):
        nonlocal changed, focus_cells, elimination_map

        # Map candidate -> set of indices where candidate appears
        candidate_positions = {n: set() for n in range(1, 10)}

        for idx, cell in enumerate(cells):
            if not cell.is_solved():
                for c in cell.get_candidates():
                    candidate_positions[c].add(idx)

        nums = list(candidate_positions.keys())

        # Find pairs of candidates that appear exactly in the same two positions
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                c1, c2 = nums[i], nums[j]
                pos1, pos2 = candidate_positions[c1], candidate_positions[c2]

                if len(pos1) == 2 and pos1 == pos2:
                    # Hidden pair found
                    for pos in pos1:
                        cell = cells[pos]
                        current_candidates = cell.get_candidates()
                        allowed = {c1, c2}
                        if not current_candidates.issubset(allowed):
                            # Eliminate other candidates
                            eliminated = current_candidates - allowed
                            new_candidates = current_candidates.intersection(allowed)
                            cell.set_candidates(new_candidates)
                            changed = True

                            # Track eliminations
                            cell_pos = positions[pos]
                            for v in eliminated:
                                elimination_map.setdefault(str(v), []).append(cell_pos)

                    # Mark the pair cells for focus/highlight
                    for pos in pos1:
                        focus_cells.append(positions[pos])

    # Process all units using shared utility
    process_all_units(board, process_unit)

    if not changed:
        return False, None

    # Build human-readable description
    lines = []
    for cand, poses in elimination_map.items():
        locs = [get_cell_location(r, c) for (r, c) in poses]
        lines.append(f"Eliminated {cand} from {locs}")
    description = "Hidden Pair elimination:\n" + "\n".join(lines)
    eliminations = [{k: v} for k, v in elimination_map.items()]

    step = TechniqueStep(
        technique="Hidden Pair",
        description=description,
        focus_cells=focus_cells,
        value=None,
        eliminations=eliminations,
    )
    return True, step


def apply_all_hidden_pairs(board):
    """
    Apply hidden pair technique repeatedly until no more changes.
    Returns:
      changed (bool): True if any candidates were eliminated during the process.
      steps (list): List of TechniqueStep objects for each application
    """
    changed = False
    steps = []
    while True:
        step_changed, step = apply_one_hidden_pair(board)
        if not step_changed:
            break
        changed = True
        steps.append(step)
    return changed, steps
