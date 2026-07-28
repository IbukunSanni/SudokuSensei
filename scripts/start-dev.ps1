$projectRoot = Split-Path -Parent $PSScriptRoot
$statePath = Join-Path $projectRoot ".dev-processes.json"

. (Join-Path $PSScriptRoot "dev-processes.ps1")
Stop-RecordedDevProcesses -StatePath $statePath

$backendDirectory = Join-Path $projectRoot "backend"
$frontendDirectory = Join-Path $projectRoot "frontend"

$backendCommand = "cd /d `"$backendDirectory`" && call start-dev.bat"
$frontendCommand = "cd /d `"$frontendDirectory`" && call start-dev.bat"

$backendProcess = Start-Process `
    -FilePath "cmd.exe" `
    -ArgumentList "/k", $backendCommand `
    -PassThru

$frontendProcess = Start-Process `
    -FilePath "cmd.exe" `
    -ArgumentList "/k", $frontendCommand `
    -PassThru

@(
    @{
        name = "backend"
        pid = $backendProcess.Id
        startedAt = $backendProcess.StartTime.ToUniversalTime().ToString("o")
    },
    @{
        name = "frontend"
        pid = $frontendProcess.Id
        startedAt = $frontendProcess.StartTime.ToUniversalTime().ToString("o")
    }
) | ConvertTo-Json | Set-Content -LiteralPath $statePath -Encoding utf8

Write-Host "SudokuSensei development servers started."
Write-Host "Frontend: http://localhost:3000"
Write-Host "Backend:  http://localhost:8000"
Write-Host "API docs: http://localhost:8000/docs"
