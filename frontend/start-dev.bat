@echo off
echo Starting SudokuSensei Frontend...

REM Always use the local FastAPI server during development.
set "NEXT_PUBLIC_BACKEND_URL_IP="
set "NEXT_PUBLIC_BACKEND_URL_LOCALHOST=http://localhost:8000"

REM Check if node_modules exists
if not exist node_modules (
    echo Node modules not found. Installing dependencies...
    call npm install
)

echo Starting development server...
npm run dev
