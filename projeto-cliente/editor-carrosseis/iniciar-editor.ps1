$ErrorActionPreference = 'Stop'
$editorRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$service = Join-Path $editorRoot 'scripts\carrossel_service.py'

$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
    & $python.Source -3 $service start
} else {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        Write-Host 'Python 3 não foi encontrado. Instale-o em https://www.python.org/downloads/windows/' -ForegroundColor Red
        Read-Host 'Pressione Enter para fechar'
        exit 1
    }
    & $python.Source $service start
}

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Start-Process 'http://localhost:8797'
