# SudokuSensei — TODO

## Definition of Done
A feature is **done** when:
- Logic is implemented in `backend/logic/`
- Wired into all solver services (`step_by_step_solver.py`, `frontend_optimized_solver.py`, `advanced_solver.py`)
- At least one passing test in `backend/tests/techniques/`
- Works end-to-end: frontend displays the technique step with correct cell highlights

---

## Solving Techniques

- [x] Naked Singles
- [x] Hidden Singles
- [x] Naked Pairs
- [x] Hidden Pairs
- [ ] Pointing Pairs / Triples
- [ ] Box-Line Reduction
- [x] Naked Triples
- [x] Hidden Triples
- [ ] X-Wing
- [ ] Swordfish

---

## Future Enhancements

- [ ] Puzzle Generation — create puzzles with a guaranteed unique solution
- [ ] Performance Monitoring — metrics and dashboards
- [ ] Multi-threading — parallel puzzle solving
- [ ] Puzzle Image Ingestion — upload a photo of a Sudoku puzzle and have it parsed, solved, and explained step by step
  - Grid detection & perspective correction (OpenCV or similar)
  - Digit recognition via a tailored/custom-trained CNN (not a generic API call)
  - Output: extracted grid fed directly into the solver pipeline
- [ ] 3D Visualization — advanced solving animation
