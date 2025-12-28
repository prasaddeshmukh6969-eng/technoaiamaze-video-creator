@echo off
echo ========================================
echo Technoaiamaze - Indian Marketing Video Platform
echo ========================================
echo.
echo Starting backend server...
start cmd /k "cd server && python -m uvicorn mock_server:app --reload --port 8000"

timeout /t 3 >nul

echo Starting frontend...
start cmd /k "cd client && npm run dev"

echo.
echo ========================================
echo Servers starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to exit (servers will continue running)
pause >nul
