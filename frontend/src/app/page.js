"use client";

import { useState } from "react";
import SudokuGrid from "@/components/sudoku/SudokuGrid";
import DuplicateWarning from "@/components/sudoku/DuplicateWarning";
import ResultDisplay from "@/components/sudoku/ResultDisplay";
import ActionButton from "@/components/ui/ActionButton";
import apiService from "@/services/apiService";
import {
  defaultPuzzle,
  emptyGrid,
  getHighlightInfo,
} from "@/utils/sudokuUtils";

/**
 * SudokuSensei - An educational Sudoku solver that highlights rule violations
 * and provides step-by-step solving explanations.
 *
 * This application connects to a FastAPI backend that implements various
 * Sudoku solving techniques including naked singles, hidden singles,
 * hidden pairs, and naked pairs.
 */
export default function Page() {
  // State management
  const [puzzle, setPuzzle] = useState(emptyGrid);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Calculate highlighting information for the current puzzle
  const highlightInfo = getHighlightInfo(puzzle);

  /**
   * Handles input changes in the Sudoku grid
   *
   * @param {number} row - Row index (0-8)
   * @param {number} col - Column index (0-8)
   * @param {string} value - New cell value
   */
  const handleChange = (row, col, value) => {
    // Only allow empty cells or digits 1-9
    if (value === "" || /^[1-9]$/.test(value)) {
      const newGrid = puzzle.map((r) => [...r]);
      newGrid[row][col] = value === "" ? 0 : parseInt(value);
      setPuzzle(newGrid);
    }
  };

  /**
   * Sends the puzzle to the backend for solving
   */
  const solvePuzzle = async () => {
    setLoading(true);
    const result = await apiService.solvePuzzle(puzzle);
    setResult(result);
    setLoading(false);
  };

  /**
   * Loads the default example puzzle
   */
  const loadDefaultPuzzle = () => {
    setPuzzle(defaultPuzzle);
    setResult(null);
  };

  /**
   * Clears the puzzle grid
   */
  const clearPuzzle = () => {
    setPuzzle(emptyGrid);
    setResult(null);
  };

  const pageStyle = {
    padding: "2rem",
    fontFamily: "Arial, sans-serif",
    backgroundColor: "#f5f5f5",
    minHeight: "100vh",
  };

  const containerStyle = {
    maxWidth: "600px",
    margin: "0 auto",
    backgroundColor: "white",
    padding: "2rem",
    borderRadius: "10px",
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
  };

  const titleStyle = {
    textAlign: "center",
    color: "#333",
    marginBottom: "2rem",
    fontSize: "2.5rem",
  };

  const buttonContainerStyle = {
    display: "flex",
    justifyContent: "center",
    gap: "1rem",
    marginBottom: "2rem",
  };

  return (
    <div style={pageStyle}>
      <div style={containerStyle}>
        <h1 style={titleStyle}>SudokuSensei</h1>

        {/* Editable Sudoku input grid */}
        <SudokuGrid
          puzzle={puzzle}
          highlightInfo={highlightInfo}
          onCellChange={handleChange}
        />

        {/* Duplicate warning */}
        {highlightInfo.duplicates.size > 0 && <DuplicateWarning />}

        {/* Action buttons */}
        <div style={buttonContainerStyle}>
          <ActionButton
            text="Load Example"
            color="green"
            onClick={loadDefaultPuzzle}
          />
          <ActionButton text="Clear" color="red" onClick={clearPuzzle} />
          <ActionButton
            text={loading ? "Solving..." : "Solve Puzzle"}
            color="blue"
            onClick={solvePuzzle}
            disabled={loading}
          />
        </div>

        {/* Results display */}
        <ResultDisplay result={result} />
      </div>
    </div>
  );
}
