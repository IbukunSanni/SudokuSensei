"use client";

import { useState } from "react";
import {
  parsePuzzleText,
  PuzzleParseError,
} from "@/utils/puzzleParser.mjs";
import styles from "./PuzzleImport.module.css";

const EXAMPLE_FORMAT = `53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79`;

export default function PuzzleImport({ onImport }) {
  const [text, setText] = useState("");
  const [error, setError] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const importPuzzle = () => {
    try {
      const puzzle = parsePuzzleText(text);
      onImport(puzzle);
      setError("");
      setIsOpen(false);
    } catch (parseError) {
      setError(
        parseError instanceof PuzzleParseError
          ? parseError.message
          : "The puzzle could not be imported."
      );
    }
  };

  const handleKeyDown = (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      event.preventDefault();
      importPuzzle();
    }
  };

  return (
    <section className={styles.container}>
      <button
        type="button"
        className={styles.toggle}
        aria-expanded={isOpen}
        aria-controls="puzzle-import-panel"
        onClick={() => setIsOpen((open) => !open)}
      >
        <span>Paste a puzzle</span>
        <span aria-hidden="true">{isOpen ? "−" : "+"}</span>
      </button>

      {isOpen && (
        <div id="puzzle-import-panel" className={styles.panel}>
          <label className={styles.label} htmlFor="puzzle-import-text">
            Puzzle text
          </label>
          <textarea
            id="puzzle-import-text"
            className={styles.textarea}
            value={text}
            placeholder={EXAMPLE_FORMAT}
            spellCheck={false}
            onChange={(event) => {
              setText(event.target.value);
              setError("");
            }}
            onKeyDown={handleKeyDown}
          />
          <p className={styles.help}>
            Enter 81 cells or nine rows. Use 0 or . for blanks.
          </p>
          {error && (
            <p className={styles.error} role="alert">
              {error}
            </p>
          )}
          <div className={styles.actions}>
            <button
              type="button"
              className={styles.secondaryButton}
              onClick={() => {
                setText("");
                setError("");
              }}
            >
              Clear text
            </button>
            <button
              type="button"
              className={styles.primaryButton}
              onClick={importPuzzle}
            >
              Import puzzle
            </button>
          </div>
          <p className={styles.shortcut}>Ctrl/Cmd + Enter to import</p>
        </div>
      )}
    </section>
  );
}
