from itertools import combinations

from helpers.get_location import get_cell_location
from models.technique_step import TechniqueStep


def apply_one_swordfish(board):
    """Find one row- or column-based Swordfish and apply its eliminations."""
    board.update_candidates()

    for candidate in range(1, 10):
        row_step = _find_row_swordfish(board, candidate)
        if row_step:
            return True, row_step

        column_step = _find_column_swordfish(board, candidate)
        if column_step:
            return True, column_step

    return False, None


def _find_row_swordfish(board, candidate):
    positions = {}
    for row in range(9):
        columns = {
            col
            for col in range(9)
            if not board.grid[row][col].is_solved()
            and candidate in board.grid[row][col].get_candidates()
        }
        if 2 <= len(columns) <= 3:
            positions[row] = columns

    for base_rows in combinations(positions, 3):
        cover_columns = set().union(*(positions[row] for row in base_rows))
        if len(cover_columns) != 3:
            continue
        if any(
            sum(col in positions[row] for row in base_rows) < 2
            for col in cover_columns
        ):
            continue

        eliminated = []
        for row in range(9):
            if row in base_rows:
                continue
            for col in cover_columns:
                cell = board.grid[row][col]
                if not cell.is_solved() and candidate in cell.get_candidates():
                    cell.set_candidates(cell.get_candidates() - {candidate})
                    eliminated.append((row, col))

        if eliminated:
            focus = [
                (row, col)
                for row in base_rows
                for col in sorted(positions[row])
            ]
            return _swordfish_step(
                candidate,
                focus,
                eliminated,
                "rows",
                base_rows,
                tuple(sorted(cover_columns)),
            )
    return None


def _find_column_swordfish(board, candidate):
    positions = {}
    for col in range(9):
        rows = {
            row
            for row in range(9)
            if not board.grid[row][col].is_solved()
            and candidate in board.grid[row][col].get_candidates()
        }
        if 2 <= len(rows) <= 3:
            positions[col] = rows

    for base_columns in combinations(positions, 3):
        cover_rows = set().union(*(positions[col] for col in base_columns))
        if len(cover_rows) != 3:
            continue
        if any(
            sum(row in positions[col] for col in base_columns) < 2
            for row in cover_rows
        ):
            continue

        eliminated = []
        for col in range(9):
            if col in base_columns:
                continue
            for row in cover_rows:
                cell = board.grid[row][col]
                if not cell.is_solved() and candidate in cell.get_candidates():
                    cell.set_candidates(cell.get_candidates() - {candidate})
                    eliminated.append((row, col))

        if eliminated:
            focus = [
                (row, col)
                for col in base_columns
                for row in sorted(positions[col])
            ]
            return _swordfish_step(
                candidate,
                focus,
                eliminated,
                "columns",
                base_columns,
                tuple(sorted(cover_rows)),
            )
    return None


def _swordfish_step(candidate, focus, eliminated, orientation, bases, covers):
    locations = ", ".join(get_cell_location(row, col) for row, col in eliminated)
    base_numbers = ", ".join(str(index + 1) for index in bases)
    cover_numbers = ", ".join(str(index + 1) for index in covers)
    description = (
        f"Swordfish on candidate {candidate} using {orientation} {base_numbers} "
        f"and cover units {cover_numbers}; eliminated {candidate} from {locations}"
    )
    return TechniqueStep(
        technique="Swordfish",
        description=description,
        focus_cells=focus,
        eliminations=[{str(candidate): eliminated}],
        extra={
            "orientation": orientation,
            "bases": tuple(bases),
            "covers": tuple(covers),
            "candidate": candidate,
        },
    )
