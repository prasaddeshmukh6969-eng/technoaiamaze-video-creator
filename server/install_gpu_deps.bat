@echo off
REM ============================================================
REM Technoaiamaze GPU Dependencies Installer
REM Installs PyTorch with CUDA 11.8 for NVIDIA GTX 1650
REM ============================================================

echo.
echo ========================================================
echo TECHNOAIAMAZE GPU DEPENDENCIES INSTALLER
echo ========================================================
echo.
echo System Info:
echo   - GPU: NVIDIA GTX 1650
echo   - CUDA: 12.1 (Will install PyTorch for CUDA 11.8)
echo   - Target: Python 3.8-3.11 required
echo.

REM Change to server directory
cd /d "%~dp0"

echo [PRE-CHECK] Checking if virtual environment exists...
if not exist ".venv" (
    echo.
    echo WARNING: Virtual environment not found!
    echo Creating new virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python is installed and in PATH
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
)

echo [STEP 1/6] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo   OK
echo.

echo [STEP 2/6] Checking Python version...
python --version
python -c "import sys; v=sys.version_info; exit(0 if (3,8)<=( v.major,v.minor)<=(3,11) else 1)"
if errorlevel 1 (
    echo.
    echo WARNING: Python version should be between 3.8 and 3.11 for PyTorch
    echo Your version might not be  compatible.
    echo Continue anyway? (Y/N)
    choice /c YN /n /m "Press Y to continue or N to exit: "
    if errorlevel 2 exit /b 1
)
echo.

echo [STEP 3/6] Upgrading pip...
python -m pip install --upgrade pip
echo   OK
echo.

echo [STEP 4/6] Installing PyTorch with CUDA 11.8...
echo   This may take several minutes...
echo.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if errorlevel 1 (
    echo.
    echo ERROR: PyTorch installation failed
    echo.
    echo Troubleshooting:
    echo   1. Check internet connection
    echo   2. Try running as Administrator
    echo   3. Check disk space
    pause
    exit /b 1
)
echo   OK
echo.

echo [STEP 5/6] Installing additional GPU libraries...
echo   - GFPGAN (face enhancement)
echo   - BasicSR (super-resolution)
echo   - Gradio Client (for LivePortrait API)
echo.
pip install gfpgan basicsr gradio-client
if errorlevel 1 (
    echo WARNING: Some packages failed to install
    echo You can continue, but some features may not work
    pause
)
echo   OK
echo.

echo [STEP 6/6] Testing CUDA availability...
echo.
python -c "import torch; print('PyTorch Version:', torch.__version__); print('CUDA Available:', torch.cuda.is_available()); print('CUDA Version (PyTorch):', torch.version.cuda); print('GPU Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU detected')"
echo.

REM Check if CUDA is truly available
python -c "import torch; exit(0 if torch.cuda.is_available() else 1)"
if errorlevel 1 (
    echo.
    echo ========================================================
    echo WARNING: CUDA NOT AVAILABLE
    echo ========================================================
    echo.
    echo Possible reasons:
    echo   1. NVIDIA drivers not installed or outdated
    echo   2. CUDA toolkit not properly configured
    echo   3. GPU not supported
    echo.
    echo The system will work in CPU mode, but will be MUCH slower.
    echo.
    echo Recommended actions:
    echo   1. Update NVIDIA drivers from nvidia.com
    echo   2. Restart computer after driver update
    echo   3. Run this installer again
    echo.
    pause
) else (
    echo.
    echo ========================================================
    echo SUCCESS! GPU DEPENDENCIES INSTALLED
    echo ========================================================
    echo.
    echo   GPU is detected and ready to use!
    echo.
    echo Next steps:
    echo   1. Run test_components.py to verify components
    echo   2. Run test_full.py for end-to-end test
    echo   3. Start backend with start_fixed_backend.bat
    echo.
)

pause
