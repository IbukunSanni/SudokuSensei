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
- [x] Naked Triples *(logic done — needs wiring into solver services)*
- [ ] Hidden Triples
- [ ] X-Wing
- [ ] Swordfish

---

## Future Enhancements

- [ ] Puzzle Generation — create puzzles with a guaranteed unique solution
- [ ] Performance Monitoring — metrics and dashboards
- [ ] Multi-threading — parallel puzzle solving
- [ ] Machine Learning — neural network pattern recognition
- [ ] 3D Visualization — advanced solving animation
