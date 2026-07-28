import assert from "node:assert/strict";
import test from "node:test";
import {
  compileStepTimeline,
  VISUAL_PHASES,
} from "../src/utils/stepTimeline.mjs";

test("compiles a placement into deterministic teaching phases", () => {
  const timeline = compileStepTimeline({
    technique: "Naked Single",
    description: "Place 5 in A1",
    explanation: "Only one candidate remains.",
    focus_cells: [[0, 0]],
    candidate_changes: [],
    cells_solved: 1,
  });

  assert.deepEqual(timeline.map(({ phase }) => phase), VISUAL_PHASES);
  assert.equal(timeline.find(({ phase }) => phase === "place").hasPlacement, true);
  assert.match(
    timeline.find(({ phase }) => phase === "explain").narration,
    /Only one candidate/
  );
});

test("compiles elimination changes without technique-specific branching", () => {
  const change = {
    position: [4, 6],
    eliminated: [3, 8],
    old_candidates: [1, 3, 8],
    new_candidates: [1],
  };
  const timeline = compileStepTimeline({
    technique: "Any Future Technique",
    description: "Generic elimination",
    focus_cells: [[1, 2], [4, 6]],
    candidate_changes: [change],
    cells_solved: 0,
  });
  const remove = timeline.find(({ phase }) => phase === "remove");

  assert.deepEqual(remove.candidateChanges, [change]);
  assert.deepEqual(remove.affectedCells, [[1, 2], [4, 6]]);
  assert.match(remove.narration, /Remove 2 candidates from 1 cell/);
});

test("reduced motion preserves constraint-step order with zero durations", () => {
  const timeline = compileStepTimeline(
    {
      technique: "Constraint Propagation",
      description: "Remove conflicts",
      focus_cells: [],
      candidate_changes: [
        { position: [0, 1], eliminated: [4], old_candidates: [4, 6], new_candidates: [6] },
      ],
      cells_solved: 0,
    },
    { reducedMotion: true }
  );

  assert.deepEqual(timeline.map(({ phase }) => phase), VISUAL_PHASES);
  assert.ok(timeline.every(({ duration }) => duration === 0));
});
