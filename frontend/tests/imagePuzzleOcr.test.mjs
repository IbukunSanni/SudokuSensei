import assert from "node:assert/strict";
import test from "node:test";
import { mapOcrSymbolsToGrid } from "../src/utils/imagePuzzleOcr.mjs";

test("maps recognized digit centers into Sudoku cells", () => {
  const result = mapOcrSymbolsToGrid(
    [
      { digit: 5, confidence: 92, bbox: { x0: 1, y0: 1, x1: 9, y1: 9 } },
      { digit: 9, confidence: 81, bbox: { x0: 81, y0: 81, x1: 89, y1: 89 } },
    ],
    90,
    90
  );

  assert.equal(result.grid[0][0], 5);
  assert.equal(result.confidence[0][0], 92);
  assert.equal(result.grid[8][8], 9);
});

test("keeps the highest-confidence digit when OCR overlaps a cell", () => {
  const result = mapOcrSymbolsToGrid(
    [
      { digit: 2, confidence: 40, bbox: { x0: 1, y0: 1, x1: 5, y1: 5 } },
      { digit: 7, confidence: 90, bbox: { x0: 2, y0: 2, x1: 6, y1: 6 } },
    ],
    90,
    90
  );

  assert.equal(result.grid[0][0], 7);
  assert.equal(result.confidence[0][0], 90);
});

test("rejects missing image dimensions", () => {
  assert.throws(
    () => mapOcrSymbolsToGrid([], 0, 90),
    /dimensions could not be read/
  );
});
