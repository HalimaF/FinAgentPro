@echo off
setlocal ENABLEDELAYEDEXPANSION

REM FinAgent Pro - Windows Demo Runner
REM Starts backend and runs all demo scripts sequentially

set ROOT=D:\Fintech
set BACKEND=%ROOT%\backend
set DEMOS=%ROOT%\demos

echo Starting FinAgent Pro Demo Suite
echo =================================

REM 1) Ensure demo dependencies are installed
cd /d %DEMOS%
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher not found. Please install Python 3.11+ from python.org.
  goto :end
)

py -m pip install --upgrade pip >nul
py -m pip install -r requirements.txt || goto :end

REM 2) Start backend API server in a new window
cd /d %BACKEND%
if not exist requirements.txt (
  echo backend\requirements.txt not found. Please check your workspace.
  goto :end
)

REM Ensure backend deps (use lightweight demo requirements on Windows)
if exist requirements-demo.txt (
  py -m pip install -r requirements-demo.txt || goto :end
)

REM Enable demo mode to avoid heavy ML deps and DB init
set DEMO_MODE=1

REM Launch Uvicorn (FastAPI) in a separate window
start "FinAgent Backend" cmd /c "set DEMO_MODE=1 && py -m uvicorn main:app --host 127.0.0.1 --port 8000"

REM Give server time to start
timeout /t 5 /nobreak >nul

REM 3) Run demos
cd /d %DEMOS%

echo.
echo Running Demo 1: Expense Processing
py expense_processing_demo.py

echo.
pause

echo Running Demo 2: Invoice Creation
py invoice_creation_demo.py

echo.
pause

echo Running Demo 3: Fraud Detection
py fraud_detection_demo.py

echo.
pause

echo Running Demo 4: Cashflow Forecast
py cashflow_forecast_demo.py

echo.
echo All demos complete.
echo If desired, close the 'FinAgent Backend' window to stop the server.

echo Done.

:end
endlocal
