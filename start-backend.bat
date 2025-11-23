@echo off
echo ========================================
echo   Starting FinAgent Pro Backend
echo ========================================
echo.

cd /d d:\Fintech\backend

echo Setting DEMO_MODE...
set DEMO_MODE=1

echo.
echo Starting backend server on port 8000...
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
