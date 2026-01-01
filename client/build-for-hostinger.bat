@echo off
echo ====================================
echo  HOSTINGER DEPLOYMENT SCRIPT
echo ====================================
echo.

echo [1/3] Installing dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: npm install failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Building for production...
call npm run build
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Build complete!
echo.
echo ====================================
echo  FILES READY FOR UPLOAD
echo ====================================
echo.
echo Location: %cd%\out
echo.
echo NEXT STEPS:
echo 1. Login to Hostinger hPanel
echo 2. Open File Manager
echo 3. Go to public_html folder
echo 4. Upload ALL files from 'out' folder
echo 5. Visit your domain!
echo.
echo Press any key to open the 'out' folder...
pause
explorer "%cd%\out"
