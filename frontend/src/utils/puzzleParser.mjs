export class PuzzleParseError extends Error {
  constructor(message) {
    super(message);
    this.name = "PuzzleParseError";
  }
}

/**
 * Parse common text representations of a Sudoku puzzle.
 *
 * Accepts digits, dots for empty cells, whitespace, commas, semicolons,
 * vertical bars, plus signs, and dashes used by ASCII grids.
 */
export function parsePuzzleText(input) {
  if (typeof input !== "string" || input.trim() === "") {
    throw new PuzzleParseError("Paste a puzzle before importing.");
  }

  const compact = input.replace(/[\s,;|+\-]/g, "");

  if (/[^0-9.]/.test(compact)) {
    throw new PuzzleParseError(
      "Use digits 1-9 and either 0 or . for empty cells."
    );
  }

  if (compact.length !== 81) {
    throw new PuzzleParseError(
      `Expected 81 cells, but found ${compact.length}.`
    );
  }

  const values = [...compact].map((character) =>
    character === "." ? 0 : Number(character)
  );

  return Array.from({ length: 9 }, (_, row) =>
    values.slice(row * 9, row * 9 + 9)
  );
}
