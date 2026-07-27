@echo off
setlocal

set "PROJECT_ROOT=%~dp0"

echo Starting SudokuSensei development servers...

start "SudokuSensei Backend" cmd /k "pushd ""%PROJECT_ROOT%backend"" && call start-dev.bat"
start "SudokuSensei Frontend" cmd /k "pushd ""%PROJECT_ROOT%frontend"" && set NEXT_PUBLIC_BACKEND_URL_IP= && set NEXT_PUBLIC_BACKEND_URL_LOCALHOST=http://localhost:8000 && call start-dev.bat"

echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API docs: http://localhost:8000/docs
echo.
echo Close the two server windows or press Ctrl+C in each to stop.

endlocal
