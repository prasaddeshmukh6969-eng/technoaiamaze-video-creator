@echo off
echo ========================================
echo Technoaiamaze AI Video Creator
echo Local GPU Setup Script
echo ========================================
echo.

echo [1/4] Checking GPU Availability...
py -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU Count: {torch.cuda.device_count()}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')" 2>nul
if errorlevel 1 (
    echo WARNING: PyTorch not installed yet. Installing dependencies...
) else (
    echo.
)

echo [2/4] Installing GPU-optimized dependencies...
echo This may take 5-10 minutes...
pip install -r requirements-gpu.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/4] Verifying GPU setup...
py -c "import torch; assert torch.cuda.is_available(), 'CUDA not available!'; print(f'✓ GPU Ready: {torch.cuda.get_device_name(0)}')"
if errorlevel 1 (
    echo ERROR: GPU not available. Check NVIDIA drivers.
    pause
    exit /b 1
)

echo.
echo [4/4] Starting Real AI Backend...
echo.
echo ========================================
echo Backend will start at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

py main.py
