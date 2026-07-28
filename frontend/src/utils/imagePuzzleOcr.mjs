const GRID_SIZE = 9;

function collectSymbols(node, symbols = []) {
  if (!node || typeof node !== "object") return symbols;

  if (
    typeof node.text === "string" &&
    /^[1-9]$/.test(node.text.trim()) &&
    node.bbox
  ) {
    symbols.push({
      digit: Number(node.text.trim()),
      confidence: Number(node.confidence ?? 0),
      bbox: node.bbox,
    });
  }

  for (const key of ["blocks", "paragraphs", "lines", "words", "symbols"]) {
    if (Array.isArray(node[key])) {
      node[key].forEach((child) => collectSymbols(child, symbols));
    }
  }

  return symbols;
}

export function mapOcrSymbolsToGrid(symbols, width, height) {
  if (!(width > 0) || !(height > 0)) {
    throw new Error("The image dimensions could not be read.");
  }

  const grid = Array.from({ length: GRID_SIZE }, () =>
    Array(GRID_SIZE).fill(0)
  );
  const confidence = Array.from({ length: GRID_SIZE }, () =>
    Array(GRID_SIZE).fill(null)
  );

  for (const symbol of symbols) {
    const centerX = (symbol.bbox.x0 + symbol.bbox.x1) / 2;
    const centerY = (symbol.bbox.y0 + symbol.bbox.y1) / 2;
    const row = Math.min(GRID_SIZE - 1, Math.max(0, Math.floor((centerY / height) * GRID_SIZE)));
    const col = Math.min(GRID_SIZE - 1, Math.max(0, Math.floor((centerX / width) * GRID_SIZE)));

    if (
      confidence[row][col] === null ||
      symbol.confidence > confidence[row][col]
    ) {
      grid[row][col] = symbol.digit;
      confidence[row][col] = symbol.confidence;
    }
  }

  return { grid, confidence };
}

export async function recognizeSudokuImage(file, dimensions, onProgress) {
  const { createWorker, PSM } = await import("tesseract.js");
  const worker = await createWorker("eng", 1, {
    logger: (message) => {
      if (message.status === "recognizing text") {
        onProgress?.(Math.round((message.progress || 0) * 100));
      }
    },
  });

  try {
    await worker.setParameters({
      tessedit_char_whitelist: "123456789",
      tessedit_pageseg_mode: PSM.SPARSE_TEXT,
    });
    const result = await worker.recognize(file, {}, { blocks: true });
    const symbols = collectSymbols(result.data);
    return mapOcrSymbolsToGrid(symbols, dimensions.width, dimensions.height);
  } finally {
    await worker.terminate();
  }
}
