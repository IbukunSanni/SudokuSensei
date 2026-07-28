function Stop-RecordedDevProcesses {
    param(
        [Parameter(Mandatory = $true)]
        [string]$StatePath
    )

    if (-not (Test-Path -LiteralPath $StatePath)) {
        return
    }

    $recordedProcesses = Get-Content -LiteralPath $StatePath -Raw |
        ConvertFrom-Json

    foreach ($record in @($recordedProcesses)) {
        $process = Get-Process -Id $record.pid -ErrorAction SilentlyContinue
        if (-not $process) {
            continue
        }

        $recordedStart = [DateTime]::Parse($record.startedAt).ToUniversalTime()
        $actualStart = $process.StartTime.ToUniversalTime()
        if ([Math]::Abs(($actualStart - $recordedStart).TotalSeconds) -lt 2) {
            taskkill.exe /PID $record.pid /T /F | Out-Null
        }
    }

    Remove-Item -LiteralPath $StatePath -Force
}
