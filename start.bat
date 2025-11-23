@echo off
echo ========================================
echo   FinAgent Pro - Starting All Services
echo ========================================
echo.

REM Set environment variable for demo mode
set DEMO_MODE=1

echo [1/3] Starting Backend Server (Port 8000)...
echo.
start "FinAgent Backend" cmd /k "cd /d %~dp0backend && set DEMO_MODE=1 && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo.
echo [2/3] Starting Frontend Server (Port 5173)...
echo.
start "FinAgent Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo [3/3] Opening Browser...
echo.
timeout /t 8 /nobreak >nul

REM Open browser
start http://localhost:5173

echo.
echo ========================================
echo   All Services Started Successfully!
echo ========================================
echo.
echo Backend API:     http://localhost:8000
echo API Docs:        http://localhost:8000/docs
echo Frontend:        http://localhost:5173
echo.
echo Press any key to stop all servers...
pause >nul

REM Kill the servers when user presses a key
taskkill /FI "WindowTitle eq FinAgent Backend*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq FinAgent Frontend*" /T /F >nul 2>&1

echo.
echo All servers stopped.
echo.
pause
