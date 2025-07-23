"use client";

import { useState } from "react";
import axios from "axios";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL_IP ||
  process.env.NEXT_PUBLIC_BACKEND_URL_LOCALHOST;

// Default puzzle example
const defaultPuzzle = [
  [5, 3, 0, 0, 7, 0, 0, 0, 0],
  [6, 0, 0, 1, 9, 5, 0, 0, 0],
  [0, 9, 8, 0, 0, 0, 0, 6, 0],
  [8, 0, 0, 0, 6, 0, 0, 0, 3],
  [4, 0, 0, 8, 0, 3, 0, 0, 1],
  [7, 0, 0, 0, 2, 0, 0, 0, 6],
  [0, 6, 0, 0, 0, 0, 2, 8, 0],
  [0, 0, 0, 4, 1, 9, 0, 0, 5],
  [0, 0, 0, 0, 8, 0, 0, 7, 9],
];



// Helper to generate proper Sudoku board styling
function getSudokuCellStyle(rowIdx, colIdx, isInput = true, isDuplicate = false, isInAffectedUnit = false) {
  const baseStyle = {
    width: "3rem",
    height: "3rem",
    textAlign: "center",
    fontSize: "1.2rem",
    fontWeight: "bold",
    border: "1px solid #ccc",
    backgroundColor: isInput ? "white" : "#f8f9fa",
  };

  // Highlight duplicate cells in red (highest priority)
  if (isDuplicate) {
    baseStyle.backgroundColor = isInput ? "#ffebee" : "#ffcdd2";
    baseStyle.color = "#d32f2f";
    baseStyle.border = "2px solid #f44336";
  }
  // Highlight affected units in yellow (lower priority)
  else if (isInAffectedUnit) {
    baseStyle.backgroundColor = isInput ? "#fffde7" : "#fff9c4";
    baseStyle.border = "1px solid #fbc02d";
  }

  // Thick borders for 3x3 box separation
  if (colIdx % 3 === 0 && colIdx !== 0) baseStyle.borderLeft = "3px solid #333";
  if (rowIdx % 3 === 0 && rowIdx !== 0) baseStyle.borderTop = "3px solid #333";

  // Outer borders
  if (colIdx === 0) baseStyle.borderLeft = "3px solid #333";
  if (rowIdx === 0) baseStyle.borderTop = "3px solid #333";
  if (colIdx === 8) baseStyle.borderRight = "3px solid #333";
  if (rowIdx === 8) baseStyle.borderBottom = "3px solid #333";

  return baseStyle;
}

export default function Page() {
  // Empty grid initialization
  const emptyGrid = Array(9)
    .fill(null)
    .map(() => Array(9).fill(0));

  const [puzzle, setPuzzle] = useState(emptyGrid);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Function to detect duplicates and affected units
  const getHighlightInfo = (grid) => {
    const duplicates = new Set();
    const affectedRows = new Set();
    const affectedCols = new Set();
    const affectedBoxes = new Set();

    // Check rows
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

    // Check columns
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

    // Check 3x3 boxes
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
  };

  const highlightInfo = getHighlightInfo(puzzle);

  const handleChange = (row, col, value) => {
    if (value === "" || /^[1-9]$/.test(value)) {
      const newGrid = puzzle.map((r) => [...r]);
      newGrid[row][col] = value === "" ? 0 : parseInt(value);
      setPuzzle(newGrid);
    }
  };

  const solvePuzzle = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${BACKEND_URL}/solve`, { puzzle });
      setResult(response.data);
    } catch (error) {
      const errorData = error.response?.data?.detail;
      if (errorData && typeof errorData === 'object') {
        // Structured error from backend
        setResult({
          error: true,
          error_type: errorData.error_type,
          message: errorData.message,
          suggestions: errorData.suggestions || []
        });
      } else {
        // Fallback for other errors
        setResult({
          error: true,
          error_type: "UNKNOWN_ERROR",
          message: error.response?.data?.detail || error.message,
          suggestions: ["Please try again or check your network connection"]
        });
      }
    }
    setLoading(false);
  };

  const loadDefaultPuzzle = () => {
    setPuzzle(defaultPuzzle);
    setResult(null);
  };

  const clearPuzzle = () => {
    setPuzzle(emptyGrid);
    setResult(null);
  };

  return (
    <div
      style={{
        padding: "2rem",
        fontFamily: "Arial, sans-serif",
        backgroundColor: "#f5f5f5",
        minHeight: "100vh",
      }}
    >
      <div
        style={{
          maxWidth: "600px",
          margin: "0 auto",
          backgroundColor: "white",
          padding: "2rem",
          borderRadius: "10px",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
        }}
      >
        <h1
          style={{
            textAlign: "center",
            color: "#333",
            marginBottom: "2rem",
            fontSize: "2.5rem",
          }}
        >
          SudokuSensei
        </h1>

        {/* Editable Sudoku input grid */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginBottom: "2rem",
          }}
        >
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(9, 3rem)",
              gap: "0",
              border: "3px solid #333",
              backgroundColor: "#333",
            }}
          >
            {puzzle.map((row, rIdx) =>
              row.map((value, cIdx) => {
                const cellKey = `${rIdx}-${cIdx}`;
                const isDuplicate = highlightInfo.duplicates.has(cellKey);
                const boxKey = `${Math.floor(rIdx / 3)}-${Math.floor(cIdx / 3)}`;
                const isInAffectedUnit = 
                  highlightInfo.affectedRows.has(rIdx) ||
                  highlightInfo.affectedCols.has(cIdx) ||
                  highlightInfo.affectedBoxes.has(boxKey);
                
                return (
                  <input
                    key={cellKey}
                    type="text"
                    maxLength={1}
                    value={value === 0 ? "" : value}
                    onChange={(e) => handleChange(rIdx, cIdx, e.target.value)}
                    style={{
                      ...getSudokuCellStyle(rIdx, cIdx, true, isDuplicate, isInAffectedUnit),
                      outline: "none",
                      transition: "background-color 0.2s",
                    }}
                    onFocus={(e) => {
                      if (!isDuplicate && !isInAffectedUnit) {
                        e.target.style.backgroundColor = "#e3f2fd";
                      }
                    }}
                    onBlur={(e) => {
                      if (!isDuplicate && !isInAffectedUnit) {
                        e.target.style.backgroundColor = "white";
                      }
                    }}
                  />
                );
              })
            )}
          </div>
        </div>

        {/* Duplicate warning */}
        {highlightInfo.duplicates.size > 0 && (
          <div
            style={{
              backgroundColor: "#ffebee",
              border: "1px solid #f44336",
              borderRadius: "5px",
              padding: "0.75rem",
              margin: "1rem 0",
              textAlign: "center",
            }}
          >
            <span style={{ color: "#d32f2f", fontWeight: "bold" }}>
              ⚠️ Duplicate numbers detected! 
            </span>
            <span style={{ color: "#666", marginLeft: "0.5rem" }}>
              Red cells have duplicates, yellow areas show affected rows/columns/boxes.
            </span>
          </div>
        )}

        {/* Buttons */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "1rem",
            marginBottom: "2rem",
          }}
        >
          <button
            onClick={loadDefaultPuzzle}
            style={{
              padding: "0.75rem 1.5rem",
              fontSize: "1rem",
              backgroundColor: "#4CAF50",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              transition: "background-color 0.2s",
            }}
            onMouseOver={(e) => (e.target.style.backgroundColor = "#45a049")}
            onMouseOut={(e) => (e.target.style.backgroundColor = "#4CAF50")}
          >
            Load Example
          </button>

          <button
            onClick={clearPuzzle}
            style={{
              padding: "0.75rem 1.5rem",
              fontSize: "1rem",
              backgroundColor: "#f44336",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              transition: "background-color 0.2s",
            }}
            onMouseOver={(e) => (e.target.style.backgroundColor = "#da190b")}
            onMouseOut={(e) => (e.target.style.backgroundColor = "#f44336")}
          >
            Clear
          </button>

          <button
            onClick={solvePuzzle}
            disabled={loading}
            style={{
              padding: "0.75rem 1.5rem",
              fontSize: "1rem",
              backgroundColor: loading ? "#ccc" : "#2196F3",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: loading ? "not-allowed" : "pointer",
              transition: "background-color 0.2s",
            }}
            onMouseOver={(e) =>
              !loading && (e.target.style.backgroundColor = "#1976D2")
            }
            onMouseOut={(e) =>
              !loading && (e.target.style.backgroundColor = "#2196F3")
            }
          >
            {loading ? "Solving..." : "Solve Puzzle"}
          </button>
        </div>

        {/* Results display */}
        {result && (
          <div style={{ textAlign: "center" }}>
            {result.error ? (
              // Error display
              <div>
                <h2
                  style={{
                    color: "#f44336",
                    marginBottom: "1rem",
                  }}
                >
                  ❌ {result.error_type === "NO_SOLUTION" ? "Not Solvable" : "Invalid Puzzle"}
                </h2>
                <p
                  style={{
                    color: "#666",
                    marginBottom: "1rem",
                    fontSize: "1.1rem",
                  }}
                >
                  {result.message}
                </p>
                {result.suggestions && result.suggestions.length > 0 && (
                  <div
                    style={{
                      backgroundColor: "#fff3cd",
                      border: "1px solid #ffeaa7",
                      borderRadius: "5px",
                      padding: "1rem",
                      margin: "1rem 0",
                      textAlign: "left",
                    }}
                  >
                    <h4 style={{ color: "#856404", marginBottom: "0.5rem" }}>
                      💡 Suggestions:
                    </h4>
                    <ul
                      style={{
                        color: "#856404",
                        margin: 0,
                        paddingLeft: "1.5rem",
                      }}
                    >
                      {result.suggestions.map((suggestion, idx) => (
                        <li key={idx} style={{ marginBottom: "0.25rem" }}>
                          {suggestion}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              // Success display
              <div>
                <h2
                  style={{
                    color: result.is_solved ? "#4CAF50" : "#ff9800",
                    marginBottom: "1rem",
                  }}
                >
                  {result.is_solved ? "✅ Solution Found!" : "⚠️ Partial Solution"}
                </h2>
                <p
                  style={{
                    color: "#666",
                    marginBottom: "1.5rem",
                    fontStyle: "italic",
                  }}
                >
                  {result.message}
                </p>

                <div
                  style={{
                    display: "flex",
                    justifyContent: "center",
                  }}
                >
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "repeat(9, 3rem)",
                      gap: "0",
                      border: "3px solid #333",
                      backgroundColor: "#333",
                    }}
                  >
                    {result.solved_grid.flat().map((num, idx) => {
                      const r = Math.floor(idx / 9);
                      const c = idx % 9;
                      return (
                        <div
                          key={idx}
                          style={{
                            ...getSudokuCellStyle(r, c, false),
                            lineHeight: "3rem",
                            userSelect: "none",
                            backgroundColor: result.is_solved
                              ? "#e8f5e8"
                              : "#fff3e0",
                            color: num === 0 ? "#ccc" : "#333",
                          }}
                        >
                          {num === 0 ? "?" : num}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
