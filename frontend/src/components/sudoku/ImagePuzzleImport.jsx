"use client";

import { useRef, useState } from "react";
import { getHighlightInfo } from "@/utils/sudokuUtils";
import { recognizeSudokuImage } from "@/utils/imagePuzzleOcr.mjs";
import styles from "./ImagePuzzleImport.module.css";

const emptyReview = () =>
  Array.from({ length: 9 }, () => Array(9).fill(0));

export default function ImagePuzzleImport({ onImport }) {
  const inputRef = useRef(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [reviewGrid, setReviewGrid] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState("");

  const recognize = async (file) => {
    if (!file?.type.startsWith("image/")) {
      setError("Choose a PNG, JPEG, WebP, or other image file.");
      return;
    }

    const imageUrl = URL.createObjectURL(file);
    setPreviewUrl((previous) => {
      if (previous) URL.revokeObjectURL(previous);
      return imageUrl;
    });
    setReviewGrid(null);
    setConfidence(null);
    setError("");
    setProgress(0);

    try {
      const bitmap = await createImageBitmap(file);
      const result = await recognizeSudokuImage(
        file,
        { width: bitmap.width, height: bitmap.height },
        setProgress
      );
      bitmap.close();
      setReviewGrid(result.grid);
      setConfidence(result.confidence);
    } catch (recognitionError) {
      setReviewGrid(emptyReview());
      setError(
        `Recognition did not complete: ${recognitionError.message}. You can still enter the clues in the review grid.`
      );
    } finally {
      setProgress(null);
    }
  };

  const updateCell = (row, col, value) => {
    if (value !== "" && !/^[1-9]$/.test(value)) return;
    setReviewGrid((current) =>
      current.map((cells, rowIndex) =>
        cells.map((cell, colIndex) =>
          rowIndex === row && colIndex === col
            ? value === "" ? 0 : Number(value)
            : cell
        )
      )
    );
    setConfidence((current) => {
      if (!current) return current;
      return current.map((cells, rowIndex) =>
        cells.map((cell, colIndex) =>
          rowIndex === row && colIndex === col ? 100 : cell
        )
      );
    });
    setError("");
  };

  const duplicates = reviewGrid
    ? getHighlightInfo(reviewGrid).duplicates
    : new Set();
  const uncertainCount = confidence
    ? confidence.flat().filter((value) => value !== null && value < 70).length
    : 0;
  const clueCount = reviewGrid
    ? reviewGrid.flat().filter(Boolean).length
    : 0;
  const canImport =
    reviewGrid && clueCount > 0 && duplicates.size === 0 && uncertainCount === 0;

  return (
    <section className={styles.container}>
      <h2 className={styles.heading}>Import from an image</h2>
      <p className={styles.help}>
        Images are recognized in your browser and are not uploaded. For this
        first baseline, crop the image closely around a straight 9×9 grid.
      </p>
      <input
        ref={inputRef}
        className={styles.hiddenInput}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={(event) => recognize(event.target.files?.[0])}
      />
      <button
        type="button"
        className={styles.pickButton}
        disabled={progress !== null}
        onClick={() => inputRef.current?.click()}
      >
        {progress === null ? "Choose or take a photo" : `Recognizing… ${progress}%`}
      </button>

      {previewUrl && (
        <img className={styles.preview} src={previewUrl} alt="Selected Sudoku" />
      )}

      {error && <p className={styles.error} role="alert">{error}</p>}

      {reviewGrid && (
        <div className={styles.review}>
          <h3>Review every clue</h3>
          <p className={styles.help}>
            {clueCount} clues found. Correct highlighted cells before importing.
          </p>
          <div className={styles.grid} aria-label="Recognized puzzle review grid">
            {reviewGrid.flatMap((row, rowIndex) =>
              row.map((value, colIndex) => {
                const key = `${rowIndex}-${colIndex}`;
                const uncertain =
                  confidence?.[rowIndex]?.[colIndex] !== null &&
                  confidence?.[rowIndex]?.[colIndex] < 70;
                return (
                  <input
                    key={key}
                    aria-label={`Row ${rowIndex + 1}, column ${colIndex + 1}`}
                    className={`${styles.cell} ${
                      duplicates.has(key) || uncertain ? styles.needsReview : ""
                    }`}
                    inputMode="numeric"
                    maxLength={1}
                    value={value || ""}
                    onChange={(event) =>
                      updateCell(rowIndex, colIndex, event.target.value)
                    }
                  />
                );
              })
            )}
          </div>
          {(duplicates.size > 0 || uncertainCount > 0) && (
            <p className={styles.warning} role="status">
              Resolve {duplicates.size > 0 ? "duplicate clues" : ""}
              {duplicates.size > 0 && uncertainCount > 0 ? " and " : ""}
              {uncertainCount > 0 ? `${uncertainCount} uncertain cells` : ""}.
            </p>
          )}
          <button
            type="button"
            className={styles.importButton}
            disabled={!canImport}
            onClick={() => onImport(reviewGrid)}
          >
            Import reviewed puzzle
          </button>
        </div>
      )}
    </section>
  );
}
