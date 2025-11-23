@echo off
echo ========================================
echo   Installing Backend Dependencies
echo ========================================
echo.

cd /d d:\Fintech\backend

echo Installing Python packages...
echo This may take a few minutes...
echo.

pip install uvicorn fastapi python-multipart python-dotenv loguru pydantic

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo You can now run: start-backend.bat
echo.

pause
