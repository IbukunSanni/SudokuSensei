@echo off
echo Starting SudokuSensei Frontend...

REM Check if node_modules exists
if not exist node_modules (
    echo Node modules not found. Running setup first...
    call setup.bat
)

echo Starting development server...
npm run dev