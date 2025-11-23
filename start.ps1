# FinAgent Pro - Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FinAgent Pro - Starting All Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set environment variable
$env:DEMO_MODE = "1"

# Start Backend
Write-Host "[1/3] Starting Backend Server (Port 8000)..." -ForegroundColor Yellow
Write-Host ""
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; `$env:DEMO_MODE='1'; Write-Host 'Backend Server Starting...' -ForegroundColor Green; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

Write-Host "Waiting for backend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# Start Frontend
Write-Host ""
Write-Host "[2/3] Starting Frontend Server (Port 5173)..." -ForegroundColor Yellow
Write-Host ""
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; Write-Host 'Frontend Server Starting...' -ForegroundColor Green; npm run dev"

Write-Host "Waiting for frontend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 8

# Open Browser
Write-Host ""
Write-Host "[3/3] Opening Browser..." -ForegroundColor Yellow
Write-Host ""
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  All Services Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend API:     http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs:        http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Frontend:        http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop this script (servers will continue running)" -ForegroundColor Yellow
Write-Host "To stop servers, close their PowerShell windows" -ForegroundColor Yellow
Write-Host ""

# Keep script running
Write-Host "Script completed. Servers are running in separate windows." -ForegroundColor Green
Read-Host "Press Enter to exit this window"
