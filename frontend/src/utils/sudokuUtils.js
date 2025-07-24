/**
 * Utility functions for Sudoku operations
 */

// Default example puzzle (medium difficulty)
export const defaultPuzzle = [
  [0, 0, 0, 0, 3, 0, 0, 0, 8],
  [0, 4, 2, 0, 0, 0, 6, 0, 0],
  [6, 0, 9, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 5, 7, 0, 0, 4],
  [3, 0, 0, 0, 0, 0, 0, 0, 7],
  [2, 0, 0, 9, 4, 0, 0, 6, 0],
  [0, 0, 5, 0, 0, 3, 2, 0, 1],
  [0, 0, 1, 0, 0, 0, 0, 7, 0],
  [0, 0, 0, 0, 2, 0, 0, 0, 0],
];

// Empty 9x9 grid filled with zeros
export const emptyGrid = Array(9)
  .fill(null)
  .map(() => Array(9).fill(0));

/**
 * Detects duplicates and affected units in the Sudoku grid
 *
 * @param {number[][]} grid - 9x9 Sudoku grid
 * @returns {Object} Sets of duplicates and affected units
 */
export function getHighlightInfo(grid) {
  const duplicates = new Set();
  const affectedRows = new Set();
  const affectedCols = new Set();
  const affectedBoxes = new Set();

  // Check rows for duplicates
  for (let row = 0; row < 9; row++) {
    const seen = new Map();
    let hasRowDuplicate = false;
    for (let col = 0; col < 9; col++) {
      const value = grid[row][col];
      if (value !== 0) {
        if (seen.has(value)) {
          duplicates.add(`${row}-${col}`);
          duplicates.add(`${row}-${seen.get(value)}`);
          hasRowDuplicate = true;
        } else {
          seen.set(value, col);
        }
      }
    }
    if (hasRowDuplicate) {
      affectedRows.add(row);
    }
  }

  // Check columns for duplicates
  for (let col = 0; col < 9; col++) {
    const seen = new Map();
    let hasColDuplicate = false;
    for (let row = 0; row < 9; row++) {
      const value = grid[row][col];
      if (value !== 0) {
        if (seen.has(value)) {
          duplicates.add(`${row}-${col}`);
          duplicates.add(`${seen.get(value)}-${col}`);
          hasColDuplicate = true;
        } else {
          seen.set(value, row);
        }
      }
    }
    if (hasColDuplicate) {
      affectedCols.add(col);
    }
  }

  // Check 3x3 boxes for duplicates
  for (let boxRow = 0; boxRow < 3; boxRow++) {
    for (let boxCol = 0; boxCol < 3; boxCol++) {
      const seen = new Map();
      let hasBoxDuplicate = false;
      for (let row = boxRow * 3; row < boxRow * 3 + 3; row++) {
        for (let col = boxCol * 3; col < boxCol * 3 + 3; col++) {
          const value = grid[row][col];
          if (value !== 0) {
            if (seen.has(value)) {
              duplicates.add(`${row}-${col}`);
              duplicates.add(seen.get(value));
              hasBoxDuplicate = true;
            } else {
              seen.set(value, `${row}-${col}`);
            }
          }
        }
      }
      if (hasBoxDuplicate) {
        affectedBoxes.add(`${boxRow}-${boxCol}`);
      }
    }
  }

  return { duplicates, affectedRows, affectedCols, affectedBoxes };
}
