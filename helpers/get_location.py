def get_column_letter(col_idx):
    """
    Convert zero-based column index to letter (A-I).

    Args:
        col_idx (int): column index (0-8)

    Returns:
        str: column letter like 'A', 'B', ..., 'I'
    """
    if not (0 <= col_idx <= 8):
        raise ValueError("Column index must be between 0 and 8 inclusive.")
    return chr(ord("A") + col_idx)


def get_row_number(row_idx):
    """
    Convert zero-based row index to 1-based string number.

    Args:
        row_idx (int): row index (0-8)

    Returns:
        str: row number string like '1', '2', ..., '9'
    """
    if not (0 <= row_idx <= 8):
        raise ValueError("Row index must be between 0 and 8 inclusive.")
    return str(row_idx + 1)


def get_cell_location(row_idx, col_idx):
    """
    Convert zero-based row and column indices to cell location string,
    e.g. column 0 and row 0 => 'A1'.

    Args:
        row_idx (int): row index (0-8)
        col_idx (int): column index (0-8)

    Returns:
        str: location string like 'B1', 'A9', etc.
    """
    col_letter = get_column_letter(col_idx)
    row_number = get_row_number(row_idx)
    return f"{col_letter}{row_number}"
