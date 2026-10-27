param([switch]$TestDatabase)

$ErrorActionPreference = 'Stop'

$serviceDir = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $serviceDir '.env'
$schemaName = if ($TestDatabase) { 'schema.test.sql' } else { 'schema.sql' }
$schemaFile = Join-Path $serviceDir $schemaName

if (-not (Test-Path $envFile)) {
    throw "Missing $envFile. Copy .env.example to .env and configure a MySQL account first."
}

$mysqlCommand = Get-Command mysql.exe -ErrorAction SilentlyContinue
if ($mysqlCommand) {
    $mysql = $mysqlCommand.Source
} else {
    $mysql = 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe'
}
if (-not (Test-Path $mysql)) {
    throw 'mysql.exe was not found. Install MySQL 8 or add its bin folder to PATH.'
}

$hostName = '127.0.0.1'
$port = '3306'
foreach ($line in Get-Content $envFile) {
    if ($line -match '^\s*(DB_HOST|DB_PORT)\s*=\s*(.*?)\s*$') {
        if ($Matches[1] -eq 'DB_HOST') { $hostName = $Matches[2] }
        if ($Matches[1] -eq 'DB_PORT') { $port = $Matches[2] }
    }
}
$adminUser = Read-Host 'MySQL administrator username (default: root)'
if ([string]::IsNullOrWhiteSpace($adminUser)) { $adminUser = 'root' }
$sqlPath = $schemaFile.Replace('\', '/')

Write-Host "Initializing $schemaName on $hostName`:$port."
Write-Host 'The MySQL client will prompt for this administrator password.'
& $mysql --host=$hostName --port=$port --user=$adminUser --password --execute="source '$sqlPath'"
if ($LASTEXITCODE -ne 0) {
    throw 'Database initialization failed. Ensure this MySQL account can create databases and tables.'
}
Write-Host 'Database and seed records are ready.'
