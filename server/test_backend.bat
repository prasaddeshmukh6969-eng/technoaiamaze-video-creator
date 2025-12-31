@echo off
echo ========================================
echo Technoaiamaze AI Video Creator
echo Quick Backend Test Script
echo ========================================
echo.

echo [1/3] Verifying GPU...
py -c "import torch; assert torch.cuda.is_available(), 'CUDA not available!'; print(f'✓  GPU Ready: {torch.cuda.get_device_name(0)}')"
if errorlevel 1 (
    echo ERROR: GPU not available
    pause
    exit /b 1
)

echo.
echo [2/3] Testing Backend Health...
echo Starting backend in background...
start /B py main.py

timeout /t 5 /nobreak > nul

curl http://localhost:8000/health

echo.
echo [3/3] Backend Status:
echo ----------------------------------------
echo Backend running at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
echo Press any key to stop the server...
pause > nul

echo Stopping server...
taskkill /F /FI "WINDOWTITLE eq main.py*" 2>nul
