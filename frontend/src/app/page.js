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
  const [puzzle, setPuzzle] = useState(emptyGrid); // Current puzzle state
  const [originalPuzzle, setOriginalPuzzle] = useState(emptyGrid); // Original puzzle for tracking solved cells
  const [result, setResult] = useState(null); // Complete solving result
  const [loading, setLoading] = useState(false); // Loading state for API calls
  const [currentStepIndex, setCurrentStepIndex] = useState(-1); // Current step in navigation (-1 = original)
  const [techniqueHighlight, setTechniqueHighlight] = useState(null); // Current technique highlighting info

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
    setOriginalPuzzle(puzzle.map(row => [...row])); // Save original state
    const result = await apiService.solvePuzzle(puzzle);
    setResult(result);
    setCurrentStepIndex(-1);
    setTechniqueHighlight(null);
    setLoading(false);
  };

  /**
   * Apply a single solving step with technique highlighting
   * 
   * This function calls the backend to apply only one technique and then
   * updates the UI to show:
   * - Green highlighting on focus cells where the technique is applied
   * - Blue styling on newly solved cells
   * - Technique information display with description
   */
  const applySingleStep = async () => {
    setLoading(true);
    if (originalPuzzle.every(row => row.every(cell => cell === 0))) {
      setOriginalPuzzle(puzzle.map(row => [...row])); // Save original state if not set
    }
    const result = await apiService.applySingleStep(puzzle);
    if (result && !result.error && result.solving_steps && result.solving_steps.length > 0) {
      const step = result.solving_steps[0];
      // Update puzzle with the new grid state
      setPuzzle(result.solved_grid);
      // Set technique highlighting for visual feedback
      setTechniqueHighlight({
        focusCells: step.focus_cells || [], // Cells to highlight in green
        technique: step.technique, // Technique name (e.g., "Naked Single")
        description: step.description, // Human-readable explanation
        value: step.value // Value that was placed (if any)
      });
    }
    setResult(result);
    setLoading(false);
  };

  /**
   * Navigate through solving steps for educational review
   * 
   * Allows users to step forward/backward through the solving process
   * to understand how each technique was applied with visual highlighting.
   */
  const navigateStep = (direction) => {
    if (!result || !result.solving_steps) return;
    
    const steps = result.solving_steps;
    let newIndex = currentStepIndex;
    
    if (direction === 'next' && currentStepIndex < steps.length - 1) {
      newIndex = currentStepIndex + 1;
    } else if (direction === 'prev' && currentStepIndex > -1) {
      newIndex = currentStepIndex - 1;
    }
    
    setCurrentStepIndex(newIndex);
    
    if (newIndex >= 0) {
      const step = steps[newIndex];
      setPuzzle(step.grid);
      setTechniqueHighlight({
        focusCells: step.focus_cells || [],
        technique: step.technique,
        description: step.description,
        value: step.value
      });
    } else {
      // Back to original puzzle
      setPuzzle(originalPuzzle);
      setTechniqueHighlight(null);
    }
  };

  /**
   * Loads the default example puzzle
   */
  const loadDefaultPuzzle = () => {
    setPuzzle(defaultPuzzle);
    setOriginalPuzzle(emptyGrid);
    setResult(null);
    setCurrentStepIndex(-1);
    setTechniqueHighlight(null);
  };

  /**
   * Clears the puzzle grid
   */
  const clearPuzzle = () => {
    setPuzzle(emptyGrid);
    setOriginalPuzzle(emptyGrid);
    setResult(null);
    setCurrentStepIndex(-1);
    setTechniqueHighlight(null);
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
          originalPuzzle={originalPuzzle}
          highlightInfo={highlightInfo}
          onCellChange={handleChange}
          techniqueHighlight={techniqueHighlight}
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
            text={loading ? "Applying..." : "Apply Step"}
            color="purple"
            onClick={applySingleStep}
            disabled={loading}
          />
          <ActionButton
            text={loading ? "Solving..." : "Solve Puzzle"}
            color="blue"
            onClick={solvePuzzle}
            disabled={loading}
          />
        </div>

        {/* Step navigation */}
        {result && result.solving_steps && result.solving_steps.length > 0 && (
          <div style={{...buttonContainerStyle, marginTop: "1rem"}}>
            <ActionButton
              text="← Previous"
              color="gray"
              onClick={() => navigateStep('prev')}
              disabled={currentStepIndex <= -1}
            />
            <span style={{
              padding: "0.5rem 1rem",
              fontSize: "0.9rem",
              color: "#666"
            }}>
              Step {currentStepIndex + 1} of {result.solving_steps.length}
            </span>
            <ActionButton
              text="Next →"
              color="gray"
              onClick={() => navigateStep('next')}
              disabled={currentStepIndex >= result.solving_steps.length - 1}
            />
          </div>
        )}

        {/* Technique information */}
        {techniqueHighlight && (
          <div style={{
            backgroundColor: "#f0f8ff",
            border: "1px solid #4CAF50",
            borderRadius: "5px",
            padding: "1rem",
            margin: "1rem 0",
            textAlign: "center"
          }}>
            <h3 style={{margin: "0 0 0.5rem 0", color: "#4CAF50"}}>
              {techniqueHighlight.technique}
            </h3>
            <p style={{margin: "0", fontSize: "0.9rem", color: "#666"}}>
              {techniqueHighlight.description}
            </p>
            {techniqueHighlight.value && (
              <p style={{margin: "0.5rem 0 0 0", fontWeight: "bold", color: "#333"}}>
                Value: {techniqueHighlight.value}
              </p>
            )}
          </div>
        )}

        {/* Results display */}
        <ResultDisplay result={result} />
      </div>
    </div>
  );
}
