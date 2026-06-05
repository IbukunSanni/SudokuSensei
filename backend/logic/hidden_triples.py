from itertools import combinations
from helpers.get_location import get_cell_location
from models.technique_step import TechniqueStep
from utils.unit_processor import process_all_units


def apply_one_hidden_triple(board):
    """
    Apply one hidden triple technique on the board.

    A hidden triple exists when exactly 3 candidates are collectively confined
    to exactly 3 cells within a unit (row, column, or box). All other candidates
    in those 3 cells can be eliminated.

    Returns:
      changed (bool): True if any candidates were eliminated.
      step (TechniqueStep): Step description/details (or None if nothing changed)
    """
    board.update_candidates()

    changed = False
    focus_cells = []
    elimination_map = {}  # str(candidate) -> list of (r,c)

    def process_unit(cells, positions):
        nonlocal changed, focus_cells, elimination_map

        # Already found a hidden triple, skip remaining units
        if changed:
            return

        # Map candidate -> set of cell indices where it appears in this unit
        candidate_positions = {n: set() for n in range(1, 10)}
        for idx, cell in enumerate(cells):
            if not cell.is_solved():
                for c in cell.get_candidates():
                    candidate_positions[c].add(idx)

        # Only candidates appearing in 2 or 3 cells are eligible
        # (1 = naked/hidden single, 4+ = can't form a confined triple)
        eligible = [n for n in range(1, 10) if 2 <= len(candidate_positions[n]) <= 3]

        for c1, c2, c3 in combinations(eligible, 3):
            pos_union = (
                candidate_positions[c1]
                | candidate_positions[c2]
                | candidate_positions[c3]
            )

            # Hidden triple: 3 candidates confined to exactly 3 cells
            if len(pos_union) == 3:
                allowed = {c1, c2, c3}
                local_changed = False

                for pos in pos_union:
                    cell = cells[pos]
                    current = cell.get_candidates()
                    eliminated = current - allowed
                    if eliminated:
                        cell.set_candidates(current & allowed)
                        changed = True
                        local_changed = True
                        cell_pos = positions[pos]
                        for v in eliminated:
                            elimination_map.setdefault(str(v), []).append(cell_pos)

                if local_changed:
                    for pos in pos_union:
                        focus_cells.append(positions[pos])
                    return  # One triple per call

    process_all_units(board, process_unit)

    if not changed:
        return False, None

    lines = []
    for cand, poses in elimination_map.items():
        locs = [get_cell_location(r, c) for (r, c) in poses]
        lines.append(f"Eliminated {cand} from {locs}")
    description = "Hidden Triple elimination:\n" + "\n".join(lines)
    eliminations = [{k: v} for k, v in elimination_map.items()]

    step = TechniqueStep(
        technique="Hidden Triple",
        description=description,
        focus_cells=focus_cells,
        value=None,
        eliminations=eliminations,
    )
    return True, step


def apply_all_hidden_triples(board):
    """
    Apply hidden triple technique repeatedly until no more changes.
    Returns:
      changed (bool): True if any candidates were eliminated during the process.
      steps (list): List of TechniqueStep objects for each application
    """
    changed = False
    steps = []
    while True:
        step_changed, step = apply_one_hidden_triple(board)
        if not step_changed:
            break
        changed = True
        steps.append(step)
    return changed, steps
