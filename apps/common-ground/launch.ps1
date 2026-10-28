$ErrorActionPreference = 'Stop'
$prototypeRoot = $PSScriptRoot
$enginePython = Join-Path (Split-Path -Parent $prototypeRoot) 'Mystic-Rebels\.runtime\python.exe'
if (-not (Test-Path -LiteralPath $enginePython)) {
    $enginePython = Join-Path (Split-Path -Parent (Split-Path -Parent $prototypeRoot)) '.runtime\python.exe'
}
if (-not (Test-Path -LiteralPath $enginePython)) {
    throw 'The installed Mystic Rebels Python runtime was not found.'
}
Set-Location -LiteralPath $prototypeRoot
& $enginePython -B (Join-Path $prototypeRoot 'app.py')

