from fastapi.testclient import TestClient

from app import app


client = TestClient(app)

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


def test_solve_returns_solution_and_steps():
    response = client.post("/solve", json={"puzzle": PUZZLE})
    assert response.status_code == 200
    payload = response.json()
    assert payload["is_solved"]
    assert all(all(value for value in row) for row in payload["solved_grid"])
    assert payload["solving_steps"]
    assert payload["techniques_applied"]


def test_solve_step_returns_exactly_one_technique_step():
    response = client.post("/solve-step", json={"puzzle": PUZZLE})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["solving_steps"]) == 1
    assert len(payload["techniques_applied"]) == 1
    step = payload["solving_steps"][0]
    assert step["step_type"] == "technique"
    assert step["focus_cells"]
    assert step["explanation"]
    for change in step["candidate_changes"]:
        assert change["old_candidates"]
        assert set(change["eliminated"]) == (
            set(change["old_candidates"]) - set(change["new_candidates"])
        )


def test_candidates_returns_marks_without_changing_grid():
    response = client.post("/candidates", json={"puzzle": PUZZLE})
    assert response.status_code == 200
    candidates = response.json()["candidates"]
    assert candidates[0][0] == []
    assert candidates[0][2] == [1, 2, 4]


def test_solve_rejects_invalid_shape():
    response = client.post("/solve", json={"puzzle": [[0] * 9]})
    assert response.status_code == 400
    assert response.json()["detail"]["error_type"] == "INVALID_FORMAT"


def test_solve_step_rejects_conflicting_clues():
    invalid = [row[:] for row in PUZZLE]
    invalid[0][2] = 5
    response = client.post("/solve-step", json={"puzzle": invalid})
    assert response.status_code == 422
    assert response.json()["detail"]["error_type"] == "NO_SOLUTION"


def test_solver_advertises_swordfish_after_x_wing():
    from services.step_by_step_solver import step_by_step_solver

    techniques = step_by_step_solver.get_available_techniques()
    assert techniques[-2:] == ["X-Wing", "Swordfish"]
