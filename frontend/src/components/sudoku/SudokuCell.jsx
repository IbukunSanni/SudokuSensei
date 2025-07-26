/**
 * SudokuCell component - Renders a single cell in the Sudoku grid
 */

/**
 * Generates style object for a Sudoku cell based on its position and state
 * 
 * @param {number} rowIdx - Row index (0-8)
 * @param {number} colIdx - Column index (0-8)
 * @param {boolean} isInput - Whether this is an input cell or display-only
 * @param {boolean} isDuplicate - Whether this cell contains a duplicate value
 * @param {boolean} isInAffectedUnit - Whether this cell is in a row/column/box with duplicates
 * @returns {Object} Style object for the cell
 */
export function getSudokuCellStyle(
  rowIdx,
  colIdx,
  isInput = true,
  isDuplicate = false,
  isInAffectedUnit = false,
  isTechniqueFocus = false,
  wasSolved = false
) {
  // Base styling for all cells
  const baseStyle = {
    width: "3rem",
    height: "3rem",
    textAlign: "center",
    fontSize: "1.2rem",
    fontWeight: "bold",
    borderTop: "1px solid #ccc",
    borderRight: "1px solid #ccc",
    borderBottom: "1px solid #ccc",
    borderLeft: "1px solid #ccc",
    backgroundColor: isInput ? "white" : "#f8f9fa",
    outline: "none",
    transition: "background-color 0.2s",
  };

  // Highlight duplicate cells in red (highest priority)
  if (isDuplicate) {
    baseStyle.backgroundColor = isInput ? "#ffebee" : "#ffcdd2";
    baseStyle.color = "#d32f2f";
    baseStyle.borderTop = "2px solid #f44336";
    baseStyle.borderRight = "2px solid #f44336";
    baseStyle.borderBottom = "2px solid #f44336";
    baseStyle.borderLeft = "2px solid #f44336";
  }
  // Highlight technique focus cells in green (second highest priority)
  else if (isTechniqueFocus) {
    baseStyle.backgroundColor = isInput ? "#e8f5e8" : "#c8e6c8";
    baseStyle.color = "#2e7d32";
    baseStyle.borderTop = "3px solid #4caf50";
    baseStyle.borderRight = "3px solid #4caf50";
    baseStyle.borderBottom = "3px solid #4caf50";
    baseStyle.borderLeft = "3px solid #4caf50";
    baseStyle.boxShadow = "0 0 8px rgba(76, 175, 80, 0.4)";
  }
  // Highlight solved cells in blue (third priority)
  else if (wasSolved) {
    baseStyle.backgroundColor = isInput ? "#e3f2fd" : "#bbdefb";
    baseStyle.color = "#1565c0";
    baseStyle.fontWeight = "bold";
  }
  // Highlight affected units in yellow (lower priority)
  else if (isInAffectedUnit) {
    baseStyle.backgroundColor = isInput ? "#fffde7" : "#fff9c4";
    baseStyle.borderTop = "1px solid #fbc02d";
    baseStyle.borderRight = "1px solid #fbc02d";
    baseStyle.borderBottom = "1px solid #fbc02d";
    baseStyle.borderLeft = "1px solid #fbc02d";
  }

  // Thick borders for 3x3 box separation (only if not technique focus)
  if (!isTechniqueFocus) {
    if (colIdx % 3 === 0 && colIdx !== 0) {
      baseStyle.borderLeft = "3px solid #333";
    }
    if (rowIdx % 3 === 0 && rowIdx !== 0) {
      baseStyle.borderTop = "3px solid #333";
    }

    // Outer borders (only if not technique focus)
    if (colIdx === 0) {
      baseStyle.borderLeft = "3px solid #333";
    }
    if (rowIdx === 0) {
      baseStyle.borderTop = "3px solid #333";
    }
    if (colIdx === 8) {
      baseStyle.borderRight = "3px solid #333";
    }
    if (rowIdx === 8) {
      baseStyle.borderBottom = "3px solid #333";
    }
  }

  return baseStyle;
}

/**
 * Input cell for the Sudoku grid
 */
export default function SudokuCell({ 
  rowIdx, 
  colIdx, 
  value, 
  onChange, 
  isDuplicate, 
  isInAffectedUnit,
  isTechniqueFocus = false,
  techniqueInfo = null,
  wasSolved = false
}) {
  const cellStyle = getSudokuCellStyle(
    rowIdx,
    colIdx,
    true,
    isDuplicate,
    isInAffectedUnit,
    isTechniqueFocus,
    wasSolved
  );

  return (
    <input
      type="text"
      maxLength={1}
      value={value === 0 ? "" : value}
      onChange={(e) => onChange(rowIdx, colIdx, e.target.value)}
      style={cellStyle}
      onFocus={(e) => {
        if (!isDuplicate && !isInAffectedUnit && !isTechniqueFocus && !wasSolved) {
          e.target.style.backgroundColor = "#e3f2fd";
        }
      }}
      onBlur={(e) => {
        if (!isDuplicate && !isInAffectedUnit && !isTechniqueFocus) {
          if (wasSolved) {
            e.target.style.backgroundColor = "#e3f2fd";
          } else {
            e.target.style.backgroundColor = "white";
          }
        }
      }}
    />
  );
}