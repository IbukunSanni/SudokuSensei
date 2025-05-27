from helpers.get_location import get_cell_location


def apply_one_naked_pair(board):
    """
    Apply one naked pair technique on the board.
    Returns:
      changed (bool): True if any candidates were eliminated.
    """
    board.update_candidates()
    changed = False

    def process_unit(cells, unit_name):
        nonlocal changed

        # Find cells with exactly two candidates
        pairs = {}
        for idx, cell in enumerate(cells):
            if not cell.is_solved() and len(cell.get_candidates()) == 2:
                candidates_tuple = tuple(sorted(cell.get_candidates()))
                pairs.setdefault(candidates_tuple, []).append(idx)

        # Check for naked pairs: candidate sets that appear exactly in two cells
        for candidates_tuple, positions in pairs.items():
            if len(positions) == 2:
                # Naked pair found
                to_eliminate = set(candidates_tuple)
                for idx, cell in enumerate(cells):
                    if idx not in positions and not cell.is_solved():
                        current_candidates = cell.get_candidates()
                        new_candidates = current_candidates - to_eliminate
                        if new_candidates != current_candidates:
                            cell.set_candidates(new_candidates)
                            changed = True
                            # Print details about elimination
                            pair_cells = [
                                get_cell_location(
                                    *get_cell_position_in_unit(unit_name, pos)
                                )
                                for pos in positions
                            ]
                            elim_cell = get_cell_location(
                                *get_cell_position_in_unit(unit_name, idx)
                            )
                            print(
                                f"Naked Pair {candidates_tuple} in {unit_name} at cells {pair_cells}. "
                                f"Eliminated {to_eliminate} from {elim_cell}."
                            )

    def get_cell_position_in_unit(unit_name, pos):
        # Returns (row, col) of pos-th cell in the given unit for printing location
        if unit_name.startswith("row"):
            r = int(unit_name.split()[1])
            c = pos
            return (r, c)
        elif unit_name.startswith("col"):
            c = int(unit_name.split()[1])
            r = pos
            return (r, c)
        elif unit_name.startswith("box"):
            parts = unit_name.split()
            br, bc = map(int, parts[1].split(","))
            r = br * 3 + pos // 3
            c = bc * 3 + pos % 3
            return (r, c)

    # Process all rows
    for r in range(9):
        process_unit(board.get_row(r), f"row {r}")
    # Process all columns
    for c in range(9):
        process_unit(board.get_col(c), f"col {c}")
    # Process all boxes
    for br in range(3):
        for bc in range(3):
            box_cells = []
            for r in range(br * 3, br * 3 + 3):
                for c in range(bc * 3, bc * 3 + 3):
                    box_cells.append(board.grid[r][c])
            process_unit(box_cells, f"box {br},{bc}")

    return changed


def apply_all_naked_pairs(board):
    """
    Apply naked pairs repeatedly until no more changes.
    Returns:
      changed (bool): True if any candidates were eliminated during the process.
    """
    changed = False
    while True:
        step_changed = apply_one_naked_pair(board)
        if not step_changed:
            break
        changed = True
    return changed
