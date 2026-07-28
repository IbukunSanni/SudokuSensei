const DEFAULT_SIZE = 720;

export function computeAdaptiveMask(gray, width, height, radius = 8, bias = 9) {
  const integral = new Float64Array((width + 1) * (height + 1));
  for (let y = 0; y < height; y++) {
    let rowSum = 0;
    for (let x = 0; x < width; x++) {
      rowSum += gray[y * width + x];
      integral[(y + 1) * (width + 1) + x + 1] =
        integral[y * (width + 1) + x + 1] + rowSum;
    }
  }

  const mask = new Uint8Array(width * height);
  for (let y = 0; y < height; y++) {
    const y0 = Math.max(0, y - radius);
    const y1 = Math.min(height - 1, y + radius);
    for (let x = 0; x < width; x++) {
      const x0 = Math.max(0, x - radius);
      const x1 = Math.min(width - 1, x + radius);
      const sum =
        integral[(y1 + 1) * (width + 1) + x1 + 1] -
        integral[y0 * (width + 1) + x1 + 1] -
        integral[(y1 + 1) * (width + 1) + x0] +
        integral[y0 * (width + 1) + x0];
      const mean = sum / ((x1 - x0 + 1) * (y1 - y0 + 1));
      mask[y * width + x] = gray[y * width + x] < mean - bias ? 1 : 0;
    }
  }
  return mask;
}

export function findLargestComponent(mask, width, height) {
  const visited = new Uint8Array(mask.length);
  const queue = new Int32Array(mask.length);
  let best = [];

  for (let start = 0; start < mask.length; start++) {
    if (!mask[start] || visited[start]) continue;
    let head = 0;
    let tail = 0;
    const component = [];
    queue[tail++] = start;
    visited[start] = 1;

    while (head < tail) {
      const index = queue[head++];
      component.push(index);
      const x = index % width;
      const y = Math.floor(index / width);

      for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
          if (dx === 0 && dy === 0) continue;
          const nx = x + dx;
          const ny = y + dy;
          if (nx < 0 || nx >= width || ny < 0 || ny >= height) continue;
          const neighbor = ny * width + nx;
          if (mask[neighbor] && !visited[neighbor]) {
            visited[neighbor] = 1;
            queue[tail++] = neighbor;
          }
        }
      }
    }

    if (component.length > best.length) best = component;
  }

  return best;
}

export function componentCorners(component, width) {
  if (component.length < 4) {
    throw new Error("A complete Sudoku grid could not be detected.");
  }

  let topLeft;
  let topRight;
  let bottomRight;
  let bottomLeft;
  let minSum = Infinity;
  let maxSum = -Infinity;
  let minDiff = Infinity;
  let maxDiff = -Infinity;

  for (const index of component) {
    const point = { x: index % width, y: Math.floor(index / width) };
    const sum = point.x + point.y;
    const diff = point.x - point.y;
    if (sum < minSum) [minSum, topLeft] = [sum, point];
    if (sum > maxSum) [maxSum, bottomRight] = [sum, point];
    if (diff > maxDiff) [maxDiff, topRight] = [diff, point];
    if (diff < minDiff) [minDiff, bottomLeft] = [diff, point];
  }

  return [topLeft, topRight, bottomRight, bottomLeft];
}

function solveLinearSystem(matrix, values) {
  const rows = matrix.map((row, index) => [...row, values[index]]);
  for (let pivot = 0; pivot < rows.length; pivot++) {
    let best = pivot;
    for (let row = pivot + 1; row < rows.length; row++) {
      if (Math.abs(rows[row][pivot]) > Math.abs(rows[best][pivot])) best = row;
    }
    [rows[pivot], rows[best]] = [rows[best], rows[pivot]];
    if (Math.abs(rows[pivot][pivot]) < 1e-9) {
      throw new Error("The detected grid perspective is not usable.");
    }
    const divisor = rows[pivot][pivot];
    for (let col = pivot; col <= rows.length; col++) rows[pivot][col] /= divisor;
    for (let row = 0; row < rows.length; row++) {
      if (row === pivot) continue;
      const factor = rows[row][pivot];
      for (let col = pivot; col <= rows.length; col++) {
        rows[row][col] -= factor * rows[pivot][col];
      }
    }
  }
  return rows.map((row) => row[rows.length]);
}

export function unitSquareToQuadrilateral(corners) {
  const targets = [
    [0, 0, corners[0]],
    [1, 0, corners[1]],
    [1, 1, corners[2]],
    [0, 1, corners[3]],
  ];
  const matrix = [];
  const values = [];
  for (const [u, v, point] of targets) {
    matrix.push([u, v, 1, 0, 0, 0, -point.x * u, -point.x * v]);
    values.push(point.x);
    matrix.push([0, 0, 0, u, v, 1, -point.y * u, -point.y * v]);
    values.push(point.y);
  }
  return solveLinearSystem(matrix, values);
}

export function projectPoint(transform, u, v) {
  const denominator = transform[6] * u + transform[7] * v + 1;
  return {
    x: (transform[0] * u + transform[1] * v + transform[2]) / denominator,
    y: (transform[3] * u + transform[4] * v + transform[5]) / denominator,
  };
}

function grayscaleFromImageData(imageData) {
  const gray = new Uint8ClampedArray(imageData.width * imageData.height);
  for (let index = 0; index < gray.length; index++) {
    const offset = index * 4;
    gray[index] = Math.round(
      imageData.data[offset] * 0.299 +
      imageData.data[offset + 1] * 0.587 +
      imageData.data[offset + 2] * 0.114
    );
  }
  return gray;
}

function sampleBilinear(imageData, x, y) {
  const x0 = Math.max(0, Math.min(imageData.width - 1, Math.floor(x)));
  const y0 = Math.max(0, Math.min(imageData.height - 1, Math.floor(y)));
  const x1 = Math.min(imageData.width - 1, x0 + 1);
  const y1 = Math.min(imageData.height - 1, y0 + 1);
  const dx = x - x0;
  const dy = y - y0;
  let value = 0;
  for (const [sampleX, sampleY, weight] of [
    [x0, y0, (1 - dx) * (1 - dy)],
    [x1, y0, dx * (1 - dy)],
    [x0, y1, (1 - dx) * dy],
    [x1, y1, dx * dy],
  ]) {
    const offset = (sampleY * imageData.width + sampleX) * 4;
    const gray =
      imageData.data[offset] * 0.299 +
      imageData.data[offset + 1] * 0.587 +
      imageData.data[offset + 2] * 0.114;
    value += gray * weight;
  }
  return value;
}

export function warpGrid(imageData, corners, outputSize = DEFAULT_SIZE) {
  const transform = unitSquareToQuadrilateral(corners);
  const pixels = new Uint8ClampedArray(outputSize * outputSize * 4);
  for (let y = 0; y < outputSize; y++) {
    for (let x = 0; x < outputSize; x++) {
      const point = projectPoint(
        transform,
        x / (outputSize - 1),
        y / (outputSize - 1)
      );
      const gray = sampleBilinear(imageData, point.x, point.y);
      const offset = (y * outputSize + x) * 4;
      pixels[offset] = gray;
      pixels[offset + 1] = gray;
      pixels[offset + 2] = gray;
      pixels[offset + 3] = 255;
    }
  }
  return { data: pixels, width: outputSize, height: outputSize };
}

async function decodeImage(file) {
  try {
    const bitmap = await createImageBitmap(file);
    return {
      source: bitmap,
      width: bitmap.width,
      height: bitmap.height,
      dispose: () => bitmap.close(),
    };
  } catch {
    const url = URL.createObjectURL(file);
    const image = new Image();
    try {
      await new Promise((resolve, reject) => {
        image.onload = resolve;
        image.onerror = () => reject(new Error("The source image could not be decoded."));
        image.src = url;
      });
      return {
        source: image,
        width: image.naturalWidth,
        height: image.naturalHeight,
        dispose: () => URL.revokeObjectURL(url),
      };
    } catch (error) {
      URL.revokeObjectURL(url);
      throw error;
    }
  }
}

export async function prepareSudokuCells(file) {
  const decoded = await decodeImage(file);
  const scale = Math.min(1, 1000 / Math.max(decoded.width, decoded.height));
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(decoded.width * scale);
  canvas.height = Math.round(decoded.height * scale);
  const context = canvas.getContext("2d", { willReadFrequently: true });
  context.drawImage(decoded.source, 0, 0, canvas.width, canvas.height);
  decoded.dispose();

  const source = context.getImageData(0, 0, canvas.width, canvas.height);
  const gray = grayscaleFromImageData(source);
  const mask = computeAdaptiveMask(gray, source.width, source.height);
  const component = findLargestComponent(mask, source.width, source.height);
  if (component.length < source.width + source.height) {
    throw new Error("A connected 9×9 grid could not be found.");
  }

  const corners = componentCorners(component, source.width);
  const warped = warpGrid(source, corners);
  const normalized = document.createElement("canvas");
  normalized.width = warped.width;
  normalized.height = warped.height;
  normalized.getContext("2d").putImageData(
    new ImageData(warped.data, warped.width, warped.height),
    0,
    0
  );

  const cells = [];
  const ocrSheet = document.createElement("canvas");
  ocrSheet.width = 576;
  ocrSheet.height = 576;
  const sheetContext = ocrSheet.getContext("2d");
  sheetContext.fillStyle = "white";
  sheetContext.fillRect(0, 0, ocrSheet.width, ocrSheet.height);
  const cellSize = warped.width / 9;
  const padding = Math.round(cellSize * 0.16);
  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      const cell = document.createElement("canvas");
      cell.width = 64;
      cell.height = 64;
      const cellContext = cell.getContext("2d", { willReadFrequently: true });
      cellContext.fillStyle = "white";
      cellContext.fillRect(0, 0, 64, 64);
      cellContext.drawImage(
        normalized,
        col * cellSize + padding,
        row * cellSize + padding,
        cellSize - padding * 2,
        cellSize - padding * 2,
        6,
        6,
        52,
        52
      );
      const data = cellContext.getImageData(0, 0, 64, 64);
      const cellGray = grayscaleFromImageData(data);
      const inkRatio =
        cellGray.reduce((count, value) => count + (value < 175 ? 1 : 0), 0) /
        cellGray.length;
      const isBlank = inkRatio < 0.018;
      if (!isBlank) sheetContext.drawImage(cell, col * 64, row * 64);
      cells.push({ row, col, canvas: cell, isBlank });
    }
  }

  return { cells, normalized, ocrSheet, corners };
}
