# SmartSpend - Start All Services Script for Windows
# Run this script from the SmartSpendApp root directory

$ErrorActionPreference = "Stop"
$rootDir = $PSScriptRoot

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SmartSpend - Starting All Services" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command($command) {
    try {
        Get-Command $command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

if (-not (Test-Command "java")) {
    Write-Host "ERROR: Java is not installed. Please install Java 17+." -ForegroundColor Red
    exit 1
}

if (-not (Test-Command "mvn")) {
    Write-Host "ERROR: Maven is not installed. Please install Maven 3.8+." -ForegroundColor Red
    exit 1
}

if (-not (Test-Command "python")) {
    Write-Host "ERROR: Python is not installed. Please install Python 3.11+." -ForegroundColor Red
    exit 1
}

if (-not (Test-Command "node")) {
    Write-Host "ERROR: Node.js is not installed. Please install Node.js 20+." -ForegroundColor Red
    exit 1
}

Write-Host "All prerequisites found!" -ForegroundColor Green
Write-Host ""

# Start Backend
Write-Host "Starting Backend (Java Spring Boot) on port 8080..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\backend'; Write-Host 'Starting Java Backend...' -ForegroundColor Cyan; mvn spring-boot:run"

# Wait a moment for backend to initialize
Start-Sleep -Seconds 5

# Start Data Service
Write-Host "Starting Data Service (Python) on port 8001..." -ForegroundColor Yellow
$dataServiceCmd = @"
cd '$rootDir\data-service'
Write-Host 'Setting up Data Service...' -ForegroundColor Cyan
if (-not (Test-Path 'venv')) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt -q
Write-Host 'Starting Data Service on port 8001...' -ForegroundColor Green
uvicorn main:app --reload --port 8001
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $dataServiceCmd

# Wait a moment
Start-Sleep -Seconds 3

# Start AI Agent Service
Write-Host "Starting AI Agent Service (Python) on port 8002..." -ForegroundColor Yellow
$aiServiceCmd = @"
cd '$rootDir\ai-agent-service'
Write-Host 'Setting up AI Agent Service...' -ForegroundColor Cyan
if (-not (Test-Path 'venv')) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt -q
Write-Host 'Starting AI Agent Service on port 8002...' -ForegroundColor Green
uvicorn main:app --reload --port 8002
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $aiServiceCmd

# Wait a moment
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "Starting Frontend (React) on port 3000..." -ForegroundColor Yellow
$frontendCmd = @"
cd '$rootDir\frontend'
Write-Host 'Setting up Frontend...' -ForegroundColor Cyan
if (-not (Test-Path 'node_modules')) {
    npm install
}
Write-Host 'Starting Frontend on port 3000...' -ForegroundColor Green
npm run dev
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  All services are starting!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services will be available at:" -ForegroundColor Cyan
Write-Host "  Frontend:     http://localhost:3000" -ForegroundColor White
Write-Host "  Backend API:  http://localhost:8080" -ForegroundColor White
Write-Host "  Data Service: http://localhost:8001" -ForegroundColor White
Write-Host "  AI Agent:     http://localhost:8002" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to open the app in your browser..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Start-Process "http://localhost:3000"
