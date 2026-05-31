param(
    [switch]$SkipFrontend,
    [switch]$KeepImage
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$backendDir = Join-Path $repoRoot "backend"
$frontendDir = Join-Path $repoRoot "frontend"
$runId = [Guid]::NewGuid().ToString("N").Substring(0, 8)

$imageName = "abp-retogen-backend-preflight:$runId"
$networkName = "retogen-preflight-$runId"
$mongoName = "retogen-mongo-preflight-$runId"
$backendName = "retogen-backend-preflight-$runId"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message"
}

function Remove-IfExists {
    param([scriptblock]$Command)
    try {
        & $Command | Out-Null
    } catch {
    }
}

function Get-DockerLogs {
    param([string]$ContainerName)

    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        return (docker logs $ContainerName 2>&1 | Out-String)
    } finally {
        $ErrorActionPreference = $previousPreference
    }
}

try {
    Write-Step "Building backend Docker image"
    docker build -t $imageName $backendDir

    Write-Step "Starting isolated MongoDB"
    docker network create $networkName | Out-Null
    docker run -d --name $mongoName --network $networkName -e MONGO_INITDB_DATABASE=Retogen mongo:7 | Out-Null

    $mongoReady = $false
    for ($i = 0; $i -lt 30; $i++) {
        try {
            $ping = docker exec $mongoName mongosh --quiet --eval "db.adminCommand('ping').ok" 2>$null
            if (($ping | Select-Object -Last 1) -eq "1") {
                $mongoReady = $true
                break
            }
        } catch {
        }
        Start-Sleep -Seconds 2
    }
    if (-not $mongoReady) {
        throw "MongoDB did not become ready during preflight."
    }

    Write-Step "Starting backend image as non-root"
    docker run -d `
        --name $backendName `
        --network $networkName `
        -e JWT_SECRET="preflight-secret-change-in-production" `
        -e MONGO_URL="mongodb://${mongoName}:27017" `
        -e MONGO_DB_NAME="Retogen" `
        -e ALLOWED_ORIGINS="https://example.up.railway.app" `
        $imageName | Out-Null

    $apiReady = $false
    $apiResponse = ""
    for ($i = 0; $i -lt 30; $i++) {
        $status = docker inspect -f "{{.State.Status}}" $backendName
        if ($status -ne "running") {
            throw "Backend container exited early. Logs:`n$(Get-DockerLogs $backendName)"
        }

        try {
            $apiResponse = docker exec $backendName curl -fsS "http://localhost:8000/" 2>$null
            if ($apiResponse -match '"message"\s*:\s*"API Ready"') {
                $apiReady = $true
                break
            }
        } catch {
        }
        Start-Sleep -Seconds 2
    }
    if (-not $apiReady) {
        throw "Backend did not return API Ready. Last response: $apiResponse`nLogs:`n$(Get-DockerLogs $backendName)"
    }

    $backendLogs = Get-DockerLogs $backendName
    if ($backendLogs -match "Failed to install|pytest_metadata|pytest|Permission denied") {
        throw "Backend logs contain dependency-sync or permission failure markers:`n$backendLogs"
    }

    Write-Step "Backend smoke test passed"

    if (-not $SkipFrontend) {
        Write-Step "Building frontend with Railway-style API URL"
        Push-Location $frontendDir
        try {
            $env:NUXT_PUBLIC_API_BASE = "https://example.up.railway.app"
            npm ci
            npm run build
        } finally {
            Pop-Location
            Remove-Item -Recurse -Force (Join-Path $frontendDir ".output") -ErrorAction SilentlyContinue
        }
    }

    Write-Step "Deployment preflight passed"
} finally {
    Remove-IfExists { docker rm -f $backendName }
    Remove-IfExists { docker rm -f $mongoName }
    Remove-IfExists { docker network rm $networkName }
    if (-not $KeepImage) {
        Remove-IfExists { docker rmi -f $imageName }
    }
}
