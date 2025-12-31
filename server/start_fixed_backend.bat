@echo off
REM ============================================================
REM Technoaiamaze Backend Startup Script
REM Starts the FastAPI backend with proper environment setup
REM ============================================================

echo.
echo ========================================================
echo TECHNOAIAMAZE AI VIDEO CREATOR - BACKEND
echo ========================================================
echo.

REM Change to server directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run install_gpu_deps.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

echo [1/4] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo   ✅ Virtual environment activated
echo.

echo [2/4] Checking CUDA availability...
python -c "import torch; cuda=torch.cuda.is_available(); print(f'  GPU Mode: {\"ENABLED\" if cuda else \"DISABLED (CPU)\" }'); print(f'  Device: {torch.cuda.get_device_name(0) if cuda else \"CPU\"}') if 'torch' else print('  PyTorch not installed')" 2>nul
if errorlevel 1 (
    echo   ⚠️  PyTorch not available - some features will not work
    echo   Run install_gpu_deps.bat to install dependencies
)
echo.

echo [3/4] Setting environment variables...
REM Set CUDA device (use GPU 0)
set CUDA_VISIBLE_DEVICES=0

REM Optional: Set HuggingFace token if you have one
REM set HF_TOKEN=your_token_here

echo   ✅ Environment configured
echo.

echo [4/4] Starting FastAPI backend...
echo.
echo ========================================================
echo Backend starting on http://localhost:8000
echo ========================================================
echo.
echo Available endpoints:
echo   - http://localhost:8000/                  (Health check)
echo   - http://localhost:8000/docs              (API documentation)
echo   - http://localhost:8000/api/v1/generate   (Video generation)
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================================
echo.

REM Start the server
python main.py

REM If server exits
echo.
echo ========================================================
echo Backend stopped
echo ========================================================
pause
