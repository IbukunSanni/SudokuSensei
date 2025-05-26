def apply_one_hidden_single(board):
    board.update_candidates()

    # Check all units: rows, columns, boxes
    # Return True and cell position if a hidden single is found and applied

    # Helper to find hidden singles in a unit of cells
    def find_hidden_single_in_unit(cells):
        candidate_counts = {n: [] for n in range(1, 10)}
        for idx, cell in enumerate(cells):
            if not cell.is_solved():
                for c in cell.get_candidates():
                    candidate_counts[c].append(idx)
        for num, positions in candidate_counts.items():
            if len(positions) == 1:
                return positions[0], num
        return None, None

    # Check rows
    for r in range(9):
        cells = board.get_row(r)
        pos, num = find_hidden_single_in_unit(cells)
        if pos is not None:
            cell = cells[pos]
            cell.set_value(num)
            cell.set_candidates(set())
            print(f"Hidden Single in row {r} at col {pos}: placed {num}")
            return True, (r, pos)

    # Check columns
    for c in range(9):
        cells = board.get_col(c)
        pos, num = find_hidden_single_in_unit(cells)
        if pos is not None:
            cell = cells[pos]
            cell.set_value(num)
            cell.set_candidates(set())
            print(f"Hidden Single in col {c} at row {pos}: placed {num}")
            return True, (pos, c)

    # Check boxes
    for br in range(3):
        for bc in range(3):
            cells = []
            for r in range(br * 3, br * 3 + 3):
                for c in range(bc * 3, bc * 3 + 3):
                    cells.append(board.grid[r][c])
            pos, num = find_hidden_single_in_unit(cells)
            if pos is not None:
                cell = cells[pos]
                # Calculate real row, col
                row = br * 3 + pos // 3
                col = bc * 3 + pos % 3
                cell.set_value(num)
                cell.set_candidates(set())
                print(
                    f"Hidden Single in box ({br},{bc}) at ({row},{col}): placed {num}"
                )
                return True, (row, col)

    return False, None


def apply_all_hidden_singles(board):
    changed = False
    while True:
        step_changed, pos = apply_one_hidden_single(board)
        if not step_changed:
            break
        changed = True
    return changed
