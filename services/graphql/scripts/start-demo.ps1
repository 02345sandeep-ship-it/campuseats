$ErrorActionPreference = 'Stop'

$serviceDir = Split-Path -Parent $PSScriptRoot
Set-Location $serviceDir

if (-not (Test-Path '.env')) {
    throw 'Missing services/graphql/.env. Run: Copy-Item .env.example .env, then set your MySQL credentials.'
}
if (-not (Test-Path 'node_modules')) {
    throw 'Dependencies are missing. Run npm ci from services/graphql first.'
}

$settings = @{}
foreach ($line in Get-Content '.env') {
    if ($line -match '^\s*(DB_HOST|DB_PORT)\s*=\s*(.*?)\s*$') {
        $settings[$Matches[1]] = $Matches[2]
    }
}
$hostName = if ($settings.DB_HOST) { $settings.DB_HOST } else { '127.0.0.1' }
$port = if ($settings.DB_PORT) { [int]$settings.DB_PORT } else { 3306 }
$tcp = [System.Net.Sockets.TcpClient]::new()
try {
    $pending = $tcp.BeginConnect($hostName, $port, $null, $null)
    if (-not $pending.AsyncWaitHandle.WaitOne(2000)) {
        throw "MySQL is not reachable at ${hostName}:$port. Start the MySQL80 Windows service, then retry."
    }
    $tcp.EndConnect($pending)
} catch {
    $service = Get-Service -Name MySQL80 -ErrorAction SilentlyContinue
    if ($service -and $service.Status -ne 'Running') {
        Write-Host 'MySQL80 is stopped. Start it from an elevated PowerShell window with: Start-Service MySQL80'
    }
    throw "Could not reach MySQL at ${hostName}:$port. $($_.Exception.Message)"
} finally {
    $tcp.Dispose()
}

Write-Host 'MySQL accepts connections. The application will verify credentials and schema before listening.'
npm start
