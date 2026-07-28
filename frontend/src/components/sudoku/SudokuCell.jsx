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
  wasSolved = false,
  isElimination = false,
  isActiveCell = false,
  isInActiveUnit = false
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

  // Cell highlighting priority system (highest to lowest):
  
  // 1. DUPLICATE CELLS - Red highlighting (highest priority)
  // Shows rule violations that need immediate attention
  if (isDuplicate) {
    baseStyle.backgroundColor = isInput ? "#ffebee" : "#ffcdd2";
    baseStyle.color = "#d32f2f";
    baseStyle.borderTop = "2px solid #f44336";
    baseStyle.borderRight = "2px solid #f44336";
    baseStyle.borderBottom = "2px solid #f44336";
    baseStyle.borderLeft = "2px solid #f44336";
  }
  // 2. TECHNIQUE FOCUS CELLS - Green highlighting (second highest priority)
  // Shows where the current technique is being applied for educational purposes
  else if (isTechniqueFocus) {
    baseStyle.backgroundColor = isInput ? "#e8f5e8" : "#c8e6c8";
    baseStyle.color = "#2e7d32";
    baseStyle.borderTop = "3px solid #4caf50";
    baseStyle.borderRight = "3px solid #4caf50";
    baseStyle.borderBottom = "3px solid #4caf50";
    baseStyle.borderLeft = "3px solid #4caf50";
    baseStyle.boxShadow = "0 0 8px rgba(76, 175, 80, 0.4)";
  }
  // 3. SOLVED CELLS - Blue highlighting (third priority)
  // Distinguishes cells solved by techniques from original puzzle clues
  else if (isElimination) {
    baseStyle.backgroundColor = "#fff3e0";
    baseStyle.color = "#ef6c00";
    baseStyle.boxShadow = "inset 0 0 0 2px #ff9800";
  }
  // 4. ACTIVE CELL - Strong selection highlight
  else if (isActiveCell) {
    baseStyle.backgroundColor = "#dbeafe";
    baseStyle.color = "#0f4c81";
    baseStyle.boxShadow = "inset 0 0 0 3px #2563eb";
  }
  // 5. ACTIVE ROW, COLUMN, OR BOX - Context highlight
  else if (isInActiveUnit) {
    baseStyle.backgroundColor = "#eff6ff";
    baseStyle.color = "#1e3a5f";
  }
  // 6. SOLVED CELLS - Blue highlighting
  else if (wasSolved) {
    baseStyle.backgroundColor = isInput ? "#e3f2fd" : "#bbdefb";
    baseStyle.color = "#1565c0";
    baseStyle.fontWeight = "bold";
  }
  // 7. AFFECTED UNITS - Yellow highlighting
  // Shows rows/columns/boxes that contain duplicate values
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
  wasSolved = false,
  isElimination = false,
  isActiveCell = false,
  isInActiveUnit = false,
  onHoverChange = () => {},
  onFocusChange = () => {},
  candidates = [],
  showCandidates = false,
  removedCandidates = []
}) {
  const cellStyle = getSudokuCellStyle(
    rowIdx,
    colIdx,
    true,
    isDuplicate,
    isInAffectedUnit,
    isTechniqueFocus,
    wasSolved,
    isElimination,
    isActiveCell,
    isInActiveUnit
  );

  const displayCandidates =
    (showCandidates || removedCandidates.length > 0) && value === 0;

  if (!displayCandidates) {
    return (
      <input
        type="text"
        aria-label={`Row ${rowIdx + 1}, column ${colIdx + 1}`}
        maxLength={1}
        value={value === 0 ? "" : value}
        onChange={(e) => onChange(rowIdx, colIdx, e.target.value)}
        onMouseEnter={() => onHoverChange(true)}
        onMouseLeave={() => onHoverChange(false)}
        onFocus={() => onFocusChange(true)}
        onBlur={() => onFocusChange(false)}
        style={cellStyle}
      />
    );
  }

  const inputStyle = {
    position: "absolute",
    inset: 0,
    width: "100%",
    height: "100%",
    border: 0,
    outline: "none",
    background: "transparent",
    color: "transparent",
    caretColor: "#1565c0",
    textAlign: "center",
    zIndex: 2,
  };

  const candidateStyle = {
    position: "absolute",
    inset: "2px",
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gridTemplateRows: "repeat(3, 1fr)",
    alignItems: "center",
    justifyItems: "center",
    color: "#546e7a",
    fontSize: "0.55rem",
    fontWeight: 600,
    lineHeight: 1,
    pointerEvents: "none",
    zIndex: 1,
  };

  return (
    <div
      style={{...cellStyle, position: "relative", padding: 0}}
      onMouseEnter={() => onHoverChange(true)}
      onMouseLeave={() => onHoverChange(false)}
    >
      <div style={candidateStyle} aria-hidden="true">
        {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((candidate) => (
          <span
            key={candidate}
            title={
              removedCandidates.includes(candidate)
                ? `Candidate ${candidate} removed by this step`
                : undefined
            }
            style={
              removedCandidates.includes(candidate)
                ? {
                    color: "#d32f2f",
                    backgroundColor: "#ffcdd2",
                    borderRadius: "50%",
                    fontWeight: 800,
                    textDecoration: "line-through",
                    textDecorationThickness: "2px",
                    width: "0.85rem",
                    height: "0.85rem",
                    display: "grid",
                    placeItems: "center"
                  }
                : undefined
            }
          >
            {candidates.includes(candidate) ||
            removedCandidates.includes(candidate)
              ? candidate
              : ""}
          </span>
        ))}
      </div>
      <input
        type="text"
        aria-label={`Row ${rowIdx + 1}, column ${colIdx + 1}`}
        maxLength={1}
        value=""
        onChange={(e) => onChange(rowIdx, colIdx, e.target.value)}
        onFocus={() => onFocusChange(true)}
        onBlur={() => onFocusChange(false)}
        style={inputStyle}
      />
    </div>
  );
}
