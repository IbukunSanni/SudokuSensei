from copy import deepcopy

import pytest
from pydantic import ValidationError

from models.technique_step import CandidateChange
from services.step_by_step_solver import StepByStepSolver


PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def test_candidate_change_requires_an_exact_set_difference():
    with pytest.raises(
        ValidationError,
        match="Eliminated candidates must equal",
    ):
        CandidateChange(
            position=(0, 2),
            location="C1",
            old_candidates=[1, 2, 4],
            new_candidates=[1, 4],
            eliminated=[4],
        )


def test_single_step_candidate_changes_replay_to_returned_snapshot():
    solver = StepByStepSolver()
    before_candidates = solver.get_candidates(PUZZLE)

    result = solver.solve_one(PUZZLE)
    step = result["solving_steps"][0]
    replayed_candidates = deepcopy(before_candidates)

    for row in range(9):
        for col in range(9):
            if PUZZLE[row][col] == 0 and result["solved_grid"][row][col] != 0:
                replayed_candidates[row][col] = []

    for change in step["candidate_changes"]:
        row, col = change["position"]
        assert change["old_candidates"] == before_candidates[row][col]
        assert set(change["eliminated"]) == (
            set(change["old_candidates"]) - set(change["new_candidates"])
        )
        replayed_candidates[row][col] = change["new_candidates"]

    normalized_snapshot = [
        [sorted(candidates) for candidates in row]
        for row in step["candidates"]
    ]
    assert replayed_candidates == normalized_snapshot


def test_elimination_only_snapshot_derives_complete_before_and_after_sets():
    empty_grid = [[0] * 9 for _ in range(9)]
    before = [[set() for _ in range(9)] for _ in range(9)]
    after = [[set() for _ in range(9)] for _ in range(9)]
    before[0][2] = {1, 2, 3}
    after[0][2] = {3}

    changes = StepByStepSolver.derive_candidate_changes(
        empty_grid,
        empty_grid,
        before,
        after,
    )

    assert len(changes) == 1
    assert changes[0].model_dump() == {
        "position": (0, 2),
        "location": "C1",
        "eliminated": [1, 2],
        "old_candidates": [1, 2, 3],
        "new_candidates": [3],
    }
