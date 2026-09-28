$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$electronExe = Join-Path $projectPath "node_modules\electron\dist\electron.exe"

if (-not (Test-Path $electronExe)) {
    throw "Electron executable not found: $electronExe"
}

Start-Process -FilePath $electronExe -ArgumentList "`"$projectPath`"" -WorkingDirectory $projectPath
