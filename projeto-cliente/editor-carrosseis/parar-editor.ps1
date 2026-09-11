$ErrorActionPreference = 'Stop'
$editorRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$service = Join-Path $editorRoot 'scripts\carrossel_service.py'
$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) { & $python.Source -3 $service stop; exit $LASTEXITCODE }
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { Write-Error 'Python 3 não foi encontrado.' }
& $python.Source $service stop
exit $LASTEXITCODE
