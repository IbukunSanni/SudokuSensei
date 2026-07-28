export const VISUAL_PHASES = Object.freeze([
  "prepare",
  "focus",
  "explain",
  "remove",
  "place",
  "settle",
]);

const BASE_DURATIONS = Object.freeze({
  prepare: 150,
  focus: 500,
  explain: 850,
  remove: 650,
  place: 450,
  settle: 250,
});

function uniqueCells(cells) {
  const seen = new Set();
  return cells.filter(([row, col]) => {
    const key = `${row}-${col}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function speedMultiplier(speed) {
  if (typeof speed === "number" && speed > 0) return speed;
  return { fast: 0.55, slow: 1.5 }[speed] || 1;
}

export function compileStepTimeline(step, preferences = {}) {
  const candidateChanges = step.candidate_changes || [];
  const focusCells = step.focus_cells || [];
  const changedCells = candidateChanges.map((change) => change.position);
  const affectedCells = uniqueCells([...focusCells, ...changedCells]);
  const eliminatedCount = candidateChanges.reduce(
    (total, change) => total + (change.eliminated || []).length,
    0
  );
  const placementCount = Number(step.cells_solved || 0);
  const multiplier = speedMultiplier(preferences.speed);
  const duration = (phase) =>
    preferences.reducedMotion
      ? 0
      : Math.round(BASE_DURATIONS[phase] * multiplier);

  const narrations = {
    prepare: `Prepare to apply ${step.technique}.`,
    focus: focusCells.length
      ? `Focus on ${focusCells.length} pattern ${focusCells.length === 1 ? "cell" : "cells"}.`
      : `Focus on the cells affected by ${step.technique}.`,
    explain: step.explanation || step.description,
    remove: eliminatedCount
      ? `Remove ${eliminatedCount} candidate${eliminatedCount === 1 ? "" : "s"} from ${candidateChanges.length} cell${candidateChanges.length === 1 ? "" : "s"}.`
      : "This step does not remove candidates directly.",
    place: placementCount
      ? `Place ${placementCount} solved value${placementCount === 1 ? "" : "s"}.`
      : "This step does not place a value.",
    settle: `${step.technique} is complete. Review the resulting board.`,
  };

  return VISUAL_PHASES.map((phase) => ({
    phase,
    duration: duration(phase),
    affectedCells,
    focusCells,
    candidateChanges: phase === "remove" ? candidateChanges : [],
    hasPlacement: phase === "place" && placementCount > 0,
    narration: narrations[phase],
  }));
}
