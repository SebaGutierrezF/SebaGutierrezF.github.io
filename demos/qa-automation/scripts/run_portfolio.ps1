# Ejecuta los casos del Starter Kit Free SIN copiar ni modificar sus fuentes.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$StarterKitPath,
    [Parameter(Mandatory=$true)][string]$PythonExecutable,
    [switch]$IncludeUI
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path -LiteralPath $StarterKitPath).Path
$edition = if (Test-Path -LiteralPath (Join-Path $repo 'free-v0.1.1\tests')) {
    Join-Path $repo 'free-v0.1.1'
} elseif (Test-Path -LiteralPath (Join-Path $repo 'tests')) {
    $repo
} else {
    throw 'La ruta no contiene el Starter Kit Free v0.1.1 (tests/).'
}
$python = (Resolve-Path -LiteralPath $PythonExecutable).Path
$src = Join-Path $edition 'src'
$tests = Join-Path $edition 'tests'
$verify = Join-Path $edition 'tools\verify_pytest_junit.py'
if (!(Test-Path -LiteralPath $verify -PathType Leaf)) { throw 'Falta el verificador original JUnit.' }
$env:PYTHONPATH = "$src;$edition"
$env:NO_PROXY = '127.0.0.1,localhost'
$env:no_proxy = '127.0.0.1,localhost'
$env:PIP_NO_INDEX = '1'
$env:PYTHONNOUSERSITE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
& $python -c "import importlib.metadata as m; assert m.version('pytest')=='8.3.4'; print('PYTEST_PIN_OK')"
if ($LASTEXITCODE -ne 0) { throw 'Se requiere pytest==8.3.4' }
$names = @('test_api_001_health','test_api_002_catalog')
if ($IncludeUI) {
    if (!$env:CHROMEDRIVER_PATH -or !(Test-Path -LiteralPath $env:CHROMEDRIVER_PATH -PathType Leaf)) {
        throw 'Falta CHROMEDRIVER_PATH apuntando a un driver local, sin descargas automáticas.'
    }
    & $python -c "import importlib.metadata as m; assert m.version('selenium')=='4.28.1'; print('SELENIUM_PIN_OK')"
    if ($LASTEXITCODE -ne 0) { throw 'Se requiere selenium==4.28.1' }
    $names += @('test_ui_001_login_success','test_ui_002_invalid_login')
    $suite = $tests
} else {
    $suite = Join-Path $tests 'api'
}
$evidence = Join-Path (Split-Path -Parent $PSScriptRoot) 'evidence'
New-Item -ItemType Directory -Path $evidence -Force | Out-Null
$junit = Join-Path $evidence 'pytest.xml'
& $python -m pytest -q -ra "--junitxml=$junit" $suite
$pytestCode = $LASTEXITCODE
if (!(Test-Path -LiteralPath $junit -PathType Leaf)) { throw 'No se generó el XML de resultados.' }
& $python $verify $junit @names
$verifyCode = $LASTEXITCODE
& $python (Join-Path $PSScriptRoot 'junit_to_portfolio.py') $junit --output $evidence
$reportCode = $LASTEXITCODE
Write-Host "EVIDENCE_JUNIT=$junit"
Write-Host "EVIDENCE_HTML=$(Join-Path $evidence 'index.html')"
if ($pytestCode -ne 0 -or $verifyCode -ne 0 -or $reportCode -ne 0) {
    throw "QA_PORTFOLIO_NOT_PASS | pytest=$pytestCode verify=$verifyCode report=$reportCode"
}
Write-Host "QA_PORTFOLIO_PASS | MODE=$(if($IncludeUI){'API_AND_UI'}else{'API_ONLY'})"
