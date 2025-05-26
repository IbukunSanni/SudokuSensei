# logic/naked_single.py


def apply_one_naked_single(board):
    """
    Apply naked single technique once on the board.
    Returns:
      changed (bool): True if a cell was filled
      position (tuple): (row, col) of the filled cell or None
    """
    board.update_candidates()  # update candidates for all cells

    for r in range(9):
        for c in range(9):
            cell = board.grid[r][c]
            if not cell.is_solved():
                candidates = cell.get_candidates()
                if len(candidates) == 1:
                    value = candidates.pop()
                    cell.set_value(value)
                    cell.set_candidates(set())
                    print(f"Naked Single: Filled cell at ({r}, {c}) with {value}")
                    return True, (r, c)
    return False, None


def apply_all_naked_singles(board):
    """
    Repeatedly apply naked single until no more changes.
    Returns:
      changed (bool): True if any cell was filled during the process
    """
    changed = False
    while True:
        step_changed, pos = apply_one_naked_single(board)
        if not step_changed:
            break
        changed = True
    return changed
