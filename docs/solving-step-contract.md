# Solving-step contract

The backend emits solving steps as deterministic state transitions. The frontend
may explain, animate, pause, or replay a step, but it must not rerun a Sudoku
technique to reconstruct the result.

## Candidate-change invariant

Every candidate change describes one unsolved cell:

```text
eliminated = old_candidates - new_candidates
new_candidates is a subset of old_candidates
```

Candidate arrays are sorted for stable API responses. A newly solved cell is
represented by the step's grid and value fields; clearing that cell's candidate
set is not reported as a candidate elimination.

## Placement example

```json
{
  "technique": "Naked Single",
  "focus_cells": [[0, 2]],
  "value": 4,
  "grid": [[5, 3, 4, 0, 7, 0, 0, 0, 0]],
  "candidate_changes": [
    {
      "position": [1, 2],
      "location": "C2",
      "old_candidates": [2, 4],
      "new_candidates": [2],
      "eliminated": [4]
    }
  ]
}
```

The placement and its peer eliminations belong to the same logical step.

## Elimination-only example

```json
{
  "technique": "Naked Pair",
  "focus_cells": [[0, 0], [0, 1]],
  "value": null,
  "candidate_changes": [
    {
      "position": [0, 2],
      "location": "C1",
      "old_candidates": [1, 2, 3],
      "new_candidates": [3],
      "eliminated": [1, 2]
    }
  ]
}
```

## Replay procedure

To replay a step:

1. Start with the preceding grid and candidate snapshot.
2. Apply the solved value, if present.
3. Replace each affected cell's candidates with `new_candidates`.
4. The result must equal the step's `grid` and `candidates` snapshots.

Animation phases are a presentation concern layered over this transition. They
must never alter the recorded solver state.
