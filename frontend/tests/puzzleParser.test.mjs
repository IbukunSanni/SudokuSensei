import test from "node:test";
import assert from "node:assert/strict";

import {
  parsePuzzleText,
  PuzzleParseError,
} from "../src/utils/puzzleParser.mjs";

const COMPACT =
  "530070000600195000098000060800060003400803001700020006060000280000419005000080079";

test("parses an 81-character puzzle", () => {
  const puzzle = parsePuzzleText(COMPACT);
  assert.equal(puzzle.length, 9);
  assert.deepEqual(puzzle[0], [5, 3, 0, 0, 7, 0, 0, 0, 0]);
  assert.deepEqual(puzzle[8], [0, 0, 0, 0, 8, 0, 0, 7, 9]);
});

test("parses dots, rows, and ASCII-grid separators", () => {
  const formatted = COMPACT.replaceAll("0", ".")
    .match(/.{9}/g)
    .map((row) => `${row.slice(0, 3)}|${row.slice(3, 6)}|${row.slice(6)}`)
    .join("\n");

  assert.deepEqual(parsePuzzleText(formatted), parsePuzzleText(COMPACT));
});

test("rejects invalid characters", () => {
  assert.throws(
    () => parsePuzzleText(`${COMPACT.slice(0, 80)}x`),
    PuzzleParseError
  );
});

test("reports the parsed cell count", () => {
  assert.throws(
    () => parsePuzzleText("1234"),
    /Expected 81 cells, but found 4/
  );
});
