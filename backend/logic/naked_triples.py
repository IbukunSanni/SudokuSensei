from helpers.get_location import get_cell_location
from models.technique_step import TechniqueStep
from utils.unit_processor import process_all_units


def apply_one_naked_triple(board):
    """
    Apply one naked triple technique on the board.
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

        # If we already found a triple, don't process more units
        if changed:
            return

        # Find all cells with 2 or 3 candidates (naked triples can have 2-3 candidates each)
        candidate_cells = {}  # frozenset(candidates) -> list of indices

        for idx, cell in enumerate(cells):
            if not cell.is_solved():
                cands = cell.get_candidates()
                if 1 <= len(cands) <= 3:  # Naked triples have 1-3 candidates per cell
                    key = frozenset(cands)
                    candidate_cells.setdefault(key, []).append(idx)

        # Find all possible combinations of 3 cells
        cell_indices = []
        for indices in candidate_cells.values():
            cell_indices.extend(indices)

        # Remove duplicates and ensure we have at least 3 cells
        unique_indices = list(set(cell_indices))
        if len(unique_indices) < 3:
            return

        # Check all combinations of 3 cells
        from itertools import combinations

        for triple_indices in combinations(unique_indices, 3):
            # Get the union of all candidates in these 3 cells
            all_candidates = set()
            for idx in triple_indices:
                all_candidates.update(cells[idx].get_candidates())

            # Naked triple: exactly 3 candidates across exactly 3 cells
            if len(all_candidates) == 3:
                # Verify each cell's candidates are a subset of the triple
                is_naked_triple = True
                for idx in triple_indices:
                    cell_candidates = cells[idx].get_candidates()
                    if not cell_candidates.issubset(all_candidates):
                        is_naked_triple = False
                        break

                if is_naked_triple:
                    # Found a naked triple! Eliminate these candidates from other cells
                    to_remove = all_candidates
                    local_changed = False

                    for idx, cell in enumerate(cells):
                        if idx not in triple_indices and not cell.is_solved():
                            old = cell.get_candidates()
                            new = old - to_remove
                            if new != old:
                                cell.set_candidates(new)
                                changed = True
                                local_changed = True
                                pos = positions[idx]
                                for v in old - new:
                                    elimination_map.setdefault(str(v), []).append(pos)

                    # Mark the triple cells for focus/highlight (only if we made changes)
                    if local_changed:
                        for idx in triple_indices:
                            focus_cells.append(positions[idx])
                        return  # Only process one triple per call

    # Process all units using shared utility
    process_all_units(board, process_unit)

    if not changed:
        return False, None

    # Build human-readable description
    lines = []
    for cand, poses in elimination_map.items():
        locs = [get_cell_location(r, c) for (r, c) in poses]
        lines.append(f"Eliminated {cand} from {locs}")
    description = "Naked Triple elimination:\n" + "\n".join(lines)
    eliminations = [{k: v} for k, v in elimination_map.items()]

    step = TechniqueStep(
        technique="Naked Triple",
        description=description,
        focus_cells=focus_cells,
        value=None,
        eliminations=eliminations,
    )
    return True, step


def apply_all_naked_triples(board):
    """
    Apply naked triples repeatedly until no more changes.
    Returns:
      changed (bool): True if any candidates were eliminated during the process.
      steps (list): List of TechniqueStep objects for each application
    """
    changed = False
    steps = []
    while True:
        step_changed, step = apply_one_naked_triple(board)
        if not step_changed:
            break
        changed = True
        steps.append(step)
    return changed, steps
