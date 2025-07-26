def process_all_units(board, process_unit_func):
    """
    Process all units (rows, columns, boxes) on the board with a given function.

    Args:
        board: The sudoku board
        process_unit_func: Function that takes (cells, positions) and processes a unit
    """
    # Process all rows
    for r in range(9):
        row_cells = board.get_row(r)
        row_positions = [(r, c) for c in range(9)]
        process_unit_func(row_cells, row_positions)

    # Process all columns
    for c in range(9):
        col_cells = board.get_col(c)
        col_positions = [(r, c) for r in range(9)]
        process_unit_func(col_cells, col_positions)

    # Process all 3x3 boxes
    for br in range(3):
        for bc in range(3):
            box_cells = []
            box_positions = []
            for dr in range(3):
                for dc in range(3):
                    r = br * 3 + dr
                    c = bc * 3 + dc
                    box_cells.append(board.grid[r][c])
                    box_positions.append((r, c))
            process_unit_func(box_cells, box_positions)
