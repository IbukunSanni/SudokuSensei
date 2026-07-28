from helpers.get_location import get_cell_location
from models.technique_step import TechniqueStep


def apply_one_x_wing(board):
    """Find one row- or column-based X-Wing and apply its eliminations."""
    board.update_candidates()

    for candidate in range(1, 10):
        row_positions = {}
        for row in range(9):
            columns = tuple(
                col
                for col in range(9)
                if not board.grid[row][col].is_solved()
                and candidate in board.grid[row][col].get_candidates()
            )
            if len(columns) == 2:
                row_positions.setdefault(columns, []).append(row)

        for columns, rows in row_positions.items():
            if len(rows) < 2:
                continue
            for first_index in range(len(rows) - 1):
                for second_index in range(first_index + 1, len(rows)):
                    base_rows = (rows[first_index], rows[second_index])
                    eliminated = []
                    for row in range(9):
                        if row in base_rows:
                            continue
                        for col in columns:
                            cell = board.grid[row][col]
                            if not cell.is_solved() and candidate in cell.get_candidates():
                                cell.set_candidates(cell.get_candidates() - {candidate})
                                eliminated.append((row, col))
                    if eliminated:
                        focus = [(row, col) for row in base_rows for col in columns]
                        return _x_wing_step(
                            candidate, focus, eliminated, "rows", base_rows, columns
                        )

        column_positions = {}
        for col in range(9):
            rows = tuple(
                row
                for row in range(9)
                if not board.grid[row][col].is_solved()
                and candidate in board.grid[row][col].get_candidates()
            )
            if len(rows) == 2:
                column_positions.setdefault(rows, []).append(col)

        for rows, columns in column_positions.items():
            if len(columns) < 2:
                continue
            for first_index in range(len(columns) - 1):
                for second_index in range(first_index + 1, len(columns)):
                    base_columns = (columns[first_index], columns[second_index])
                    eliminated = []
                    for col in range(9):
                        if col in base_columns:
                            continue
                        for row in rows:
                            cell = board.grid[row][col]
                            if not cell.is_solved() and candidate in cell.get_candidates():
                                cell.set_candidates(cell.get_candidates() - {candidate})
                                eliminated.append((row, col))
                    if eliminated:
                        focus = [(row, col) for col in base_columns for row in rows]
                        return _x_wing_step(
                            candidate, focus, eliminated, "columns", base_columns, rows
                        )

    return False, None


def _x_wing_step(candidate, focus, eliminated, orientation, bases, covers):
    locations = ", ".join(get_cell_location(row, col) for row, col in eliminated)
    description = (
        f"X-Wing on candidate {candidate} using {orientation} "
        f"{bases[0] + 1} and {bases[1] + 1}; eliminated {candidate} from {locations}"
    )
    return True, TechniqueStep(
        technique="X-Wing",
        description=description,
        focus_cells=focus,
        eliminations=[{str(candidate): eliminated}],
        extra={"orientation": orientation, "bases": bases, "covers": covers},
    )
