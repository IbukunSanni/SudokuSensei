$projectRoot = Split-Path -Parent $PSScriptRoot
$statePath = Join-Path $projectRoot ".dev-processes.json"

. (Join-Path $PSScriptRoot "dev-processes.ps1")
Stop-RecordedDevProcesses -StatePath $statePath

Write-Host "Recorded SudokuSensei development servers stopped."
