# Production deployment

SudokuSensei uses two Vercel projects so the Next.js frontend and FastAPI
backend can be deployed and rolled back independently.

## Topology

- Frontend project root: `frontend`
- Backend project root: `backend`
- Frontend URL: `https://sudoku-sensei.vercel.app`
- Backend URL: `https://sudoku-sensei-backend.vercel.app`
- OCR runs in the browser; puzzle images are not uploaded.
- The API is stateless and does not require authentication.

## Environment variables

Set this on the frontend project for Production and Preview:

```text
NEXT_PUBLIC_API_URL=https://sudoku-sensei-backend.vercel.app
```

Set this on the backend project for Production:

```text
CORS_ORIGINS=https://sudoku-sensei.vercel.app
```

The backend also accepts this optional comma-separated value when more trusted
origins are required:

```text
CORS_ORIGINS=https://sudoku-sensei.vercel.app,https://example.com
```

Vercel preview URLs for this project are accepted through a narrow origin
regular expression. Override `CORS_ORIGIN_REGEX` if the project name changes.

## Release procedure

1. Run backend tests.
2. Run frontend tests, lint, and the production build.
3. Deploy the backend and verify `/health`.
4. Deploy the frontend with `NEXT_PUBLIC_API_URL` pointing at the verified API.
5. Run the production smoke test:

```powershell
node scripts/smoke-production.mjs
```

Override URLs for previews:

```powershell
$env:SUDOKU_FRONTEND_URL="https://preview.example"
$env:SUDOKU_BACKEND_URL="https://api-preview.example"
node scripts/smoke-production.mjs
```

## Rollback

Use the Vercel project dashboard to promote the last known-good deployment for
the affected project. Roll back the backend first when its API contract is the
source of the failure; otherwise roll back only the frontend.

After rollback, rerun the smoke test and confirm browser CORS requests succeed.
