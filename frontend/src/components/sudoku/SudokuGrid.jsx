import SudokuCell from './SudokuCell';
import { getSudokuCellStyle } from './SudokuCell';

/**
 * Column header component (A-I)
 */
function ColumnHeader({ letter }) {
  const style = {
    width: "3rem",
    height: "1.5rem",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "0.9rem",
    fontWeight: "bold",
    color: "#666",
  };
  
  return (
    <div style={style}>
      {letter}
    </div>
  );
}

/**
 * Row header component (1-9)
 */
function RowHeader({ number }) {
  const style = {
    width: "1.5rem",
    height: "3rem",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "0.9rem",
    fontWeight: "bold",
    color: "#666",
  };
  
  return (
    <div style={style}>
      {number}
    </div>
  );
}

/**
 * Display-only cell for the solution grid
 */
function SolutionCell({ rowIdx, colIdx, value, isSolved }) {
  const cellStyle = getSudokuCellStyle(rowIdx, colIdx, false);
  
  // Add solution-specific styles
  cellStyle.lineHeight = "3rem";
  cellStyle.userSelect = "none";
  cellStyle.backgroundColor = isSolved ? "#e8f5e8" : "#fff3e0";
  
  return (
    <div style={cellStyle}>
      {value === 0 ? "?" : value}
    </div>
  );
}

/**
 * Complete Sudoku grid with row/column headers
 */
export default function SudokuGrid({ 
  puzzle, 
  highlightInfo, 
  onCellChange, 
  isReadOnly = false,
  solvedGrid = null,
  isSolved = false
}) {
  const containerStyle = {
    display: "flex",
    justifyContent: "center",
    marginBottom: "2rem",
  };
  
  const innerContainerStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  };
  
  const headerGridStyle = {
    display: "grid",
    gridTemplateColumns: "3rem repeat(9, 3rem)",
    gap: "0",
    marginBottom: "0.25rem",
  };
  
  const rowContainerStyle = {
    display: "flex",
  };
  
  const rowHeadersStyle = {
    display: "flex",
    flexDirection: "column",
    marginRight: "0.25rem",
  };
  
  const gridStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(9, 3rem)",
    gap: "0",
    border: "3px solid #333",
    backgroundColor: "#333",
  };

  return (
    <div style={containerStyle}>
      <div style={innerContainerStyle}>
        {/* Column headers (A-I) */}
        <div style={headerGridStyle}>
          <div></div> {/* Empty corner */}
          {["A", "B", "C", "D", "E", "F", "G", "H", "I"].map((letter) => (
            <ColumnHeader key={letter} letter={letter} />
          ))}
        </div>

        {/* Grid with row numbers */}
        <div style={rowContainerStyle}>
          {/* Row numbers (1-9) */}
          <div style={rowHeadersStyle}>
            {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((number) => (
              <RowHeader key={number} number={number} />
            ))}
          </div>

          {/* Sudoku grid */}
          <div style={gridStyle}>
            {isReadOnly && solvedGrid ? (
              // Solution display grid
              solvedGrid.flat().map((num, idx) => {
                const r = Math.floor(idx / 9);
                const c = idx % 9;
                return (
                  <SolutionCell 
                    key={idx} 
                    rowIdx={r} 
                    colIdx={c} 
                    value={num} 
                    isSolved={isSolved} 
                  />
                );
              })
            ) : (
              // Editable input grid
              puzzle.map((row, rIdx) =>
                row.map((value, cIdx) => {
                  const cellKey = `${rIdx}-${cIdx}`;
                  const isDuplicate = highlightInfo?.duplicates.has(cellKey) || false;
                  const boxKey = `${Math.floor(rIdx / 3)}-${Math.floor(cIdx / 3)}`;
                  const isInAffectedUnit =
                    highlightInfo?.affectedRows.has(rIdx) ||
                    highlightInfo?.affectedCols.has(cIdx) ||
                    highlightInfo?.affectedBoxes.has(boxKey) || false;

                  return (
                    <SudokuCell
                      key={cellKey}
                      rowIdx={rIdx}
                      colIdx={cIdx}
                      value={value}
                      onChange={onCellChange}
                      isDuplicate={isDuplicate}
                      isInAffectedUnit={isInAffectedUnit}
                    />
                  );
                })
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}