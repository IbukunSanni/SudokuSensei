import assert from "node:assert/strict";
import test from "node:test";
import { mapRecognizedSymbols } from "../src/utils/imagePuzzleOcr.mjs";

test("maps normalized sheet symbols only into expected nonblank cells", () => {
  const result = mapRecognizedSymbols(
    [
      { digit: 5, confidence: 92, bbox: { x0: 8, y0: 8, x1: 56, y1: 56 } },
      { digit: 9, confidence: 88, bbox: { x0: 520, y0: 520, x1: 568, y1: 568 } },
      { digit: 3, confidence: 99, bbox: { x0: 72, y0: 8, x1: 120, y1: 56 } },
    ],
    [{ row: 0, col: 0 }, { row: 8, col: 8 }]
  );

  assert.equal(result.grid[0][0], 5);
  assert.equal(result.grid[8][8], 9);
  assert.equal(result.grid[0][1], 0);
});

test("marks expected cells missing from OCR as uncertain", () => {
  const result = mapRecognizedSymbols([], [{ row: 2, col: 4 }]);
  assert.equal(result.grid[2][4], 0);
  assert.equal(result.confidence[2][4], 0);
});
