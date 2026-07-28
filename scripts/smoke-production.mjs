const frontendUrl =
  process.env.SUDOKU_FRONTEND_URL || "https://sudoku-sensei.vercel.app";
const backendUrl =
  process.env.SUDOKU_BACKEND_URL ||
  "https://sudoku-sensei-backend.vercel.app";

async function check(name, url, validate) {
  const started = Date.now();
  const response = await fetch(url, {
    headers: { "x-request-id": `smoke-${Date.now()}` },
    signal: AbortSignal.timeout(15000),
  });
  if (!response.ok) {
    throw new Error(`${name} returned HTTP ${response.status}`);
  }
  const body = await response.text();
  if (!validate(response, body)) {
    throw new Error(`${name} returned an unexpected response`);
  }
  console.log(`${name}: OK (${Date.now() - started} ms)`);
}

await check("Frontend", frontendUrl, (_response, body) =>
  body.includes("SudokuSensei")
);
await check("Backend", `${backendUrl}/health`, (response, body) => {
  const payload = JSON.parse(body);
  return (
    payload.status === "healthy" &&
    response.headers.has("x-request-id") &&
    response.headers.has("server-timing")
  );
});
