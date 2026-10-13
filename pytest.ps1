param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ArgsList
)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
$VenvPytest = Join-Path $Root ".venv\Scripts\pytest.exe"

if (Test-Path $VenvPython) {
    & $VenvPython -m pytest @ArgsList
    exit $LASTEXITCODE
} elseif (Test-Path $VenvPytest) {
    & $VenvPytest @ArgsList
    exit $LASTEXITCODE
} else {
    & python (Join-Path $Root "run_tests.py") @ArgsList
    exit $LASTEXITCODE
}
