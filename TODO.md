# SudokuSensei — TODO

## Solving Techniques

### Singles
- [x] Naked Single — `logic/naked_single.py`
- [x] Hidden Single — `logic/hidden_single.py`

### Pairs
- [x] Naked Pair — `logic/naked_pairs.py`
- [x] Hidden Pair — `logic/hidden_pairs.py`

### Triples
- [x] Naked Triple — `logic/naked_triples.py`
- [ ] Hidden Triple

### Quads
- [ ] Naked Quad
- [ ] Hidden Quad

### Intersection Techniques
- [ ] Pointing Pairs (Box-Line Reduction)
- [ ] Box-Line Reduction (Claiming)

### Fish Techniques
- [ ] X-Wing
- [ ] Swordfish
- [ ] Jellyfish

### Wing Techniques
- [ ] Y-Wing (XY-Wing)
- [ ] XYZ-Wing
- [ ] W-Wing

### Uniqueness Techniques
- [ ] Unique Rectangle Type 1
- [ ] Unique Rectangle Type 2
- [ ] Unique Rectangle Type 3
- [ ] Unique Rectangle Type 4

### Chain & Colouring Techniques
- [ ] Simple Colouring (Single Chains)
- [ ] Multi-Colouring
- [ ] X-Cycles
- [ ] XY-Chains
- [ ] Alternating Inference Chains (AIC)

### Backtracking / Brute Force
- [ ] Backtracking with constraint propagation (fallback when logic is exhausted)

---

## Infrastructure & Quality

- [ ] Plug Naked Triples into all solver services (`advanced_solver.py`, `enhanced_solver.py`, `frontend_solver.py`, `frontend_optimized_solver.py`, `step_by_step_solver.py`) — currently only `logic/naked_triples.py` exists but is not wired into any solver class
- [ ] Add technique difficulty ratings (Beginner / Intermediate / Advanced / Expert) to `TechniqueStep`
- [ ] Expand test coverage for Naked Triples (`tests/techniques/test_naked_triples.py`)
- [ ] Add tests for each new technique as implemented

---

## Future Enhancements (from README)

- [ ] Performance Monitoring — metrics collection and performance dashboards
- [ ] Puzzle Generation — algorithm to create puzzles with a guaranteed unique solution
- [ ] Multi-threading — parallel processing for solving multiple puzzles simultaneously
- [ ] Machine Learning — neural network approach for pattern recognition
- [ ] 3D Visualization — advanced UI with solving animation
