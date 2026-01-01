# SmartSpend Services Runner
# This script starts all services in the background using PowerShell jobs

Write-Host "Starting SmartSpend Services..." -ForegroundColor Cyan
Write-Host ""

# Kill any existing processes on our ports
Write-Host "Cleaning up existing processes..." -ForegroundColor Yellow
Get-NetTCPConnection -LocalPort 8080,8001,8002,3000 -ErrorAction SilentlyContinue | ForEach-Object { 
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue 
}
Start-Sleep -Seconds 2

$workspaceRoot = "c:\Users\bruno\Documents\CodingProjects\SmartSpendApp"

# Start Backend (Spring Boot)
Write-Host "Starting Java Backend on port 8080..." -ForegroundColor Green
$backendJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location $root
    mvn -f "$root\backend\pom.xml" spring-boot:run 2>&1
} -ArgumentList $workspaceRoot

Start-Sleep -Seconds 15  # Wait for backend to start

# Start Data Service (Python)
Write-Host "Starting Python Data Service on port 8001..." -ForegroundColor Green
$dataServiceJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location "$root\data-service"
    if (-not (Test-Path venv)) { python -m venv venv }
    & "$root\data-service\venv\Scripts\Activate.ps1"
    pip install -r requirements.txt --quiet
    python -m uvicorn main:app --host 0.0.0.0 --port 8001 2>&1
} -ArgumentList $workspaceRoot

Start-Sleep -Seconds 5

# Start AI Agent Service (Python)
Write-Host "Starting Python AI Agent Service on port 8002..." -ForegroundColor Green
$aiAgentJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location "$root\ai-agent-service"
    if (-not (Test-Path venv)) { python -m venv venv }
    & "$root\ai-agent-service\venv\Scripts\Activate.ps1"
    pip install -r requirements.txt --quiet
    python -m uvicorn main:app --host 0.0.0.0 --port 8002 2>&1
} -ArgumentList $workspaceRoot

Start-Sleep -Seconds 5

# Start Frontend (React/Vite)
Write-Host "Starting React Frontend on port 3000..." -ForegroundColor Green
$frontendJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location "$root\frontend"
    npm run dev 2>&1
} -ArgumentList $workspaceRoot

Write-Host ""
Write-Host "All services starting... Job IDs:" -ForegroundColor Cyan
Write-Host "Backend: $($backendJob.Id)" -ForegroundColor White
Write-Host "Data Service: $($dataServiceJob.Id)" -ForegroundColor White
Write-Host "AI Agent: $($aiAgentJob.Id)" -ForegroundColor White
Write-Host "Frontend: $($frontendJob.Id)" -ForegroundColor White
Write-Host ""
Write-Host "Use 'Receive-Job <ID>' to see output, 'Stop-Job <ID>' to stop" -ForegroundColor Yellow
Write-Host ""
Write-Host "Services:" -ForegroundColor Cyan
Write-Host "  Backend API:    http://localhost:8080" -ForegroundColor White
Write-Host "  Data Service:   http://localhost:8001" -ForegroundColor White  
Write-Host "  AI Agent:       http://localhost:8002" -ForegroundColor White
Write-Host "  Frontend:       http://localhost:3000" -ForegroundColor White
