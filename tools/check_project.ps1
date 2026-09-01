[CmdletBinding()]
param(
    [string] $SdkPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $SdkPath) {
    $SdkPath = Join-Path $PSScriptRoot "..\..\renpy-8.5.3-sdk"
}

$projectPath = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$sdkPathResolved = (Resolve-Path -LiteralPath $SdkPath).Path
$renpyPython = Join-Path $sdkPathResolved "lib\py3-windows-x86_64\python.exe"
$renpyScript = Join-Path $sdkPathResolved "renpy.py"

if (-not (Test-Path -LiteralPath $renpyPython -PathType Leaf)) {
    throw "Ren'Py console Python not found: $renpyPython"
}

if (-not (Test-Path -LiteralPath $renpyScript -PathType Leaf)) {
    throw "Ren'Py entry point not found: $renpyScript"
}

Write-Host "Compiling $projectPath"
& $renpyPython $renpyScript $projectPath compile --compile-python
if ($LASTEXITCODE -ne 0) {
    throw "Ren'Py compile failed with exit code $LASTEXITCODE."
}

Write-Host "Running strict Ren'Py lint"
& $renpyPython $renpyScript $projectPath lint `
    --error-code `
    --reserved-parameters `
    --check-unclosed-tags `
    --all-problems
if ($LASTEXITCODE -ne 0) {
    throw "Ren'Py lint failed with exit code $LASTEXITCODE."
}

Write-Host "Running minigame smoke tests"
& $renpyPython $renpyScript $projectPath test global --hide-execution all
if ($LASTEXITCODE -ne 0) {
    throw "Ren'Py smoke test failed with exit code $LASTEXITCODE."
}

Write-Host "Ren'Py checks passed."
