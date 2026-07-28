# SudokuSensei

SudokuSensei is an educational Sudoku solver that shows **why** a logical move
works. It visualizes candidate eliminations, pattern cells, placements, and
step-by-step teaching phases instead of returning only a completed grid.

## Live application

- App: https://sudoku-sensei.vercel.app
- API: https://sudoku-sensei-backend.vercel.app
- API documentation: https://sudoku-sensei-backend.vercel.app/docs

## What users can do

- Enter a puzzle manually.
- Paste compact, nine-line, or ASCII-formatted puzzle text.
- Import a screenshot or camera image with on-device OCR.
- Review and correct recognized clues before importing.
- Highlight the active cell, row, column, and 3x3 box.
- Display candidate pencil marks.
- Apply one logical step at a time.
- See which candidates are removed and why.
- Watch each step progress through `prepare`, `focus`, `explain`, `remove`,
  `place`, and `settle` phases.
- Solve the full puzzle and navigate its recorded steps.

Image recognition runs in the browser. Puzzle images are not uploaded to the
backend.

## Supported solving techniques

- Naked Single
- Hidden Single
- Naked Pair
- Hidden Pair
- Naked Triple
- X-Wing
- Swordfish

Every solving step uses a replayable contract containing the resulting grid,
candidate snapshot, focus cells, explanations, and complete before/after
candidate changes.

## Architecture

```text
Next.js frontend
├── puzzle entry and validation
├── local image processing and OCR
├── candidate and unit visualization
└── deterministic teaching timeline
            │
            │ HTTPS / JSON
            ▼
FastAPI backend
├── request validation
├── step-by-step solver orchestration
├── logical technique implementations
└── replayable solving-step responses
```

The production frontend and backend are deployed as separate Vercel projects.
The API is stateless, and the current MVP does not require user accounts.

## Technology

### Frontend

- Next.js 16
- React 19
- Tesseract.js
- Axios
- CSS Modules
- Node.js test runner
- ESLint

### Backend

- Python 3.10+
- FastAPI
- Pydantic
- Pytest
- Uvicorn

### Delivery

- GitHub Actions
- Vercel
- Environment-restricted CORS
- Request IDs and server timing
- Production smoke testing

## Run locally

### Prerequisites

- Node.js 20+
- Python 3.10+
- Git

### Install dependencies

From the repository root:

```powershell
python -m pip install -r backend/requirements-dev.txt
cd frontend
npm install
cd ..
```

### Start both applications

```powershell
.\start-dev.bat
```

The root launcher stops only previously recorded SudokuSensei processes before
starting a new backend and frontend pair.

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API documentation: http://localhost:8000/docs

Stop both tracked applications with:

```powershell
.\stop-dev.bat
```

## Test and build

Backend:

```powershell
cd backend
python -m pytest -q
```

Frontend:

```powershell
cd frontend
npm test
npm run lint
npm run build
```

GitHub Actions runs the same backend and frontend checks for pushes and pull
requests.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Deployment and operational health |
| `POST` | `/candidates` | Candidate snapshot for an unchanged puzzle |
| `POST` | `/solve-step` | Apply one logical technique |
| `POST` | `/solve` | Solve until complete or logically blocked |

Example:

```json
{
  "puzzle": [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
  ]
}
```

## Production configuration

Frontend:

```text
NEXT_PUBLIC_API_URL=https://sudoku-sensei-backend.vercel.app
```

Backend:

```text
CORS_ORIGINS=https://sudoku-sensei.vercel.app
```

Run the production smoke test with:

```powershell
node scripts/smoke-production.mjs
```

See [deployment and rollback instructions](docs/deployment.md) and the
[solving-step contract](docs/solving-step-contract.md) for implementation
details.

## Project status

The core MVP is complete and deployed. Future work is evidence-driven:

- broader OCR evaluation and performance improvements;
- playback controls and teaching lessons;
- bounded anonymous batch processing;
- Canvas and WebGL renderers;
- authentication only when persistent private data or recoverable jobs require
  it.

The prioritized engineering roadmap is maintained in [TODO.md](TODO.md).
