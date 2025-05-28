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

// Helper to generate consistent cell borders for both grids
function getCellBorderStyle(rowIdx, colIdx) {
  return {
    borderLeft:
      colIdx % 3 === 0 && colIdx !== 0
        ? "2px solid black"
        : "1px solid gray",
    borderRight:
      (colIdx + 1) % 3 === 0 && colIdx !== 8
        ? "2px solid black"
        : "1px solid gray",
    borderBottom:
      (rowIdx + 1) % 3 === 0 && rowIdx !== 8
        ? "2px solid black"
        : "1px solid gray",
    borderTop:
      rowIdx % 3 === 0 && rowIdx !== 0 
        ? "2px solid black"
        : "1px solid gray",
  };
}

export default function Page() {
  // Empty grid initialization
  const emptyGrid = Array(9)
    .fill(null)
    .map(() => Array(9).fill(0));

  const [puzzle, setPuzzle] = useState(emptyGrid);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

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
      alert(error.response?.data?.detail || error.message);
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
    <div style={{ padding: "1rem" }}>
      <h1>Editable Sudoku Grid</h1>

      {/* Editable Sudoku input grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(9, 2.5rem)",
          gap: "4px",
          marginBottom: "1rem",
        }}
      >
        {puzzle.map((row, rIdx) =>
          row.map((value, cIdx) => (
            <input
              key={`${rIdx}-${cIdx}`}
              type="text"
              maxLength={1}
              value={value === 0 ? "" : value}
              onChange={(e) => handleChange(rIdx, cIdx, e.target.value)}
              style={{
                width: "2.5rem",
                height: "2.5rem",
                textAlign: "center",
                fontSize: "1.5rem",
                ...getCellBorderStyle(rIdx, cIdx),
              }}
            />
          ))
        )}
      </div>

      {/* Buttons */}
      <button onClick={loadDefaultPuzzle} style={{ marginRight: "1rem" }}>
        Load Default Puzzle
      </button>

      <button onClick={clearPuzzle} style={{ marginRight: "1rem" }}>
        Clear
      </button>

      <button onClick={solvePuzzle} disabled={loading}>
        {loading ? "Solving..." : "Solve Puzzle"}
      </button>

      {/* Solution display grid */}
      {result && result.is_solved && (
        <>
          <h2 style={{ marginTop: "1rem" }}>Solution:</h2>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(9, 2.5rem)",
              gap: "4px",
              marginTop: "0.5rem",
            }}
          >
            {result.solved_grid.flat().map((num, idx) => {
              const r = Math.floor(idx / 9);
              const c = idx % 9;
              return (
                <div
                  key={idx}
                  style={{
                    width: "2.5rem",
                    height: "2.5rem",
                    textAlign: "center",
                    lineHeight: "2.5rem",
                    fontSize: "1.5rem",
                    userSelect: "none",
                    backgroundColor: "#e0f7fa",
                    ...getCellBorderStyle(r, c),
                  }}
                >
                  {num}
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}
