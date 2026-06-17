$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"

Set-Location $ProjectDir

if (-not (Test-Path $PythonExe)) {
    Write-Host "Python virtual environment tidak ditemukan di .venv\Scripts\python.exe"
    Write-Host "Jalankan dari PowerShell:"
    Write-Host "python -m venv .venv"
    exit 1
}

& $PythonExe "main.py"
