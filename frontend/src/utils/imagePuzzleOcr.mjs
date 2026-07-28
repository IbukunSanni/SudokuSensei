import { prepareSudokuCells } from "./imageGridProcessing.mjs";

const GRID_SIZE = 9;

function collectSymbols(node, output = [], seen = new Set()) {
  if (!node || typeof node !== "object") return output;
  const text = typeof node.text === "string" ? node.text.trim() : "";
  if (/^[1-9]$/.test(text) && node.bbox) {
    const key = `${text}:${node.bbox.x0}:${node.bbox.y0}:${node.bbox.x1}:${node.bbox.y1}`;
    if (!seen.has(key)) {
      seen.add(key);
      output.push({
        digit: Number(text),
        confidence: Number(node.confidence || 0),
        bbox: node.bbox,
      });
    }
  }
  for (const key of ["blocks", "paragraphs", "lines", "words", "symbols"]) {
    if (Array.isArray(node[key])) {
      node[key].forEach((child) => collectSymbols(child, output, seen));
    }
  }
  return output;
}

export function mapRecognizedSymbols(symbols, nonBlankCells, sheetSize = 576) {
  const grid = Array.from({ length: GRID_SIZE }, () =>
    Array(GRID_SIZE).fill(0)
  );
  const confidence = Array.from({ length: GRID_SIZE }, () =>
    Array(GRID_SIZE).fill(null)
  );
  const expected = new Set(
    nonBlankCells.map(({ row, col }) => `${row}-${col}`)
  );

  for (const symbol of symbols) {
    const centerX = (symbol.bbox.x0 + symbol.bbox.x1) / 2;
    const centerY = (symbol.bbox.y0 + symbol.bbox.y1) / 2;
    const row = Math.min(8, Math.max(0, Math.floor(centerY / (sheetSize / 9))));
    const col = Math.min(8, Math.max(0, Math.floor(centerX / (sheetSize / 9))));
    if (!expected.has(`${row}-${col}`)) continue;
    if (
      confidence[row][col] === null ||
      symbol.confidence > confidence[row][col]
    ) {
      grid[row][col] = symbol.digit;
      confidence[row][col] = symbol.confidence;
    }
  }

  for (const { row, col } of nonBlankCells) {
    if (confidence[row][col] === null) confidence[row][col] = 0;
  }
  return { grid, confidence };
}

export async function recognizeSudokuImage(file, _dimensions, onProgress) {
  const { createWorker, PSM } = await import("tesseract.js");
  let activeRow = 0;
  let activeRowCount = 9;
  const worker = await createWorker("eng", 1, {
    logger: (message) => {
      if (message.status === "recognizing text") {
        onProgress?.(
          15 +
          Math.round(
            ((activeRow + (message.progress || 0)) / activeRowCount) * 85
          )
        );
      }
    },
  });

  try {
    await worker.setParameters({
      tessedit_char_whitelist: "123456789",
      tessedit_pageseg_mode: PSM.SINGLE_LINE,
    });
    onProgress?.(5);
    const { cells, ocrSheet } = await prepareSudokuCells(file);
    onProgress?.(15);
    const nonBlank = cells.filter((cell) => !cell.isBlank);
    const rowsToRecognize = [...new Set(nonBlank.map((cell) => cell.row))];
    activeRowCount = Math.max(1, rowsToRecognize.length);
    const symbols = [];
    for (let index = 0; index < rowsToRecognize.length; index++) {
      activeRow = index;
      const row = rowsToRecognize[index];
      const rowCanvas = document.createElement("canvas");
      rowCanvas.width = ocrSheet.width;
      rowCanvas.height = 64;
      rowCanvas.getContext("2d").drawImage(
        ocrSheet,
        0,
        row * 64,
        ocrSheet.width,
        64,
        0,
        0,
        ocrSheet.width,
        64
      );
      const result = await worker.recognize(rowCanvas, {}, { blocks: true });
      for (const symbol of collectSymbols(result.data)) {
        symbols.push({
          ...symbol,
          bbox: {
            ...symbol.bbox,
            y0: symbol.bbox.y0 + row * 64,
            y1: symbol.bbox.y1 + row * 64,
          },
        });
      }
    }
    return mapRecognizedSymbols(
      symbols,
      nonBlank,
      ocrSheet.width
    );
  } finally {
    await worker.terminate();
  }
}
