@echo off
echo Starting SudokuSensei Frontend...

REM Check if node_modules exists
if not exist node_modules (
    echo Node modules not found. Installing dependencies...
    call npm install
)

echo Starting development server...
npm run dev