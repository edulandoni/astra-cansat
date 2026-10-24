# ASTRA-20: compilo el sketch conservado; este comando no escribe en la placa.
param(
    [Parameter(Mandatory=$true)][string]$ArduinoCli,
    [Parameter(Mandatory=$true)][string]$ConfigFile,
    [Parameter(Mandatory=$true)][string]$OutputRoot,
    [string]$CompilerRoot
)
$ErrorActionPreference = 'Stop'
$taskSketch = Join-Path $PSScriptRoot '../banco-usb-v0.1/firmware/GCS_FlightSimulator'
$taskStamp = Get-Date -Format 'yyyyMMdd-HHmmss-ffff'
$taskDestination = Join-Path $OutputRoot $taskStamp
if (Test-Path -LiteralPath $taskDestination) { throw 'El destino existe; conservo la versión anterior.' }
New-Item -ItemType Directory -Path $taskDestination | Out-Null
$taskArguments = @('compile','--fqbn','esp32:esp32:esp32:FlashMode=dio,FlashFreq=40,FlashSize=4M,UploadSpeed=115200',
    '--config-file',$ConfigFile,'--build-path',(Join-Path $taskDestination 'build'),
    '--output-dir',(Join-Path $taskDestination 'artifacts'))
if ($CompilerRoot) { $taskArguments += @('--build-property',('runtime.tools.esp-x32.path='+$CompilerRoot)) }
$taskArguments += $taskSketch
& $ArduinoCli @taskArguments 2>&1 | Tee-Object -FilePath (Join-Path $taskDestination 'compilacion.txt')
if ($LASTEXITCODE -ne 0) { throw "La compilación falló. Conservo el diagnóstico en $taskDestination" }
Get-ChildItem (Join-Path $taskDestination 'artifacts') -File | Get-FileHash -Algorithm SHA256 |
    Select-Object Path,Hash | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $taskDestination 'huellas.json')
Write-Output "Compilación guardada en $taskDestination. Firmware todavía no cargado por este comando."
