from helpers.get_location import get_cell_location


def apply_one_hidden_pair(board):
    """
    Apply one hidden pair technique on the board.
    Returns:
      changed (bool): True if any candidates were eliminated.
      info (str): Description of what was done, or None if nothing done.
    """
    board.update_candidates()
    changed = False
    info = None

    def process_unit(cells, unit_name):
        nonlocal changed, info

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
                            new_candidates = current_candidates.intersection(allowed)
                            cell.set_candidates(new_candidates)
                            changed = True
                            location = get_cell_location(
                                # If unit is row or column, row and col are known; for box we calculate below
                                *get_cell_position_in_unit(unit_name, pos)
                            )
                            info = (
                                f"Hidden Pair {c1} and {c2} found in {unit_name} "
                                f"at cells {', '.join(get_cell_location(*get_cell_position_in_unit(unit_name, p)) for p in pos1)}. "
                                f"Candidates reduced to {allowed} at {location}."
                            )
                            print(info)

    def get_cell_position_in_unit(unit_name, pos):
        # Returns (row, col) of pos-th cell in the given unit for printing location
        # unit_name format: e.g. 'row 3', 'col 5', 'box 1,2'
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

    # Process rows
    for r in range(9):
        process_unit(board.get_row(r), f"row {r}")
    # Process columns
    for c in range(9):
        process_unit(board.get_col(c), f"col {c}")
    # Process boxes
    for br in range(3):
        for bc in range(3):
            box_cells = []
            for r in range(br * 3, br * 3 + 3):
                for c in range(bc * 3, bc * 3 + 3):
                    box_cells.append(board.grid[r][c])
            process_unit(box_cells, f"box {br},{bc}")

    return changed


def apply_all_hidden_pairs(board):
    """
    Apply hidden pair technique repeatedly until no more changes.
    Returns:
      changed (bool): True if any candidates were eliminated during the process.
    """
    changed = False
    while True:
        step_changed = apply_one_hidden_pair(board)
        if not step_changed:
            break
        changed = True
    return changed
