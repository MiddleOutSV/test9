@echo off
echo Starting Stock Lineup Visualizer...
echo.

REM Check if virtual environment exists
if not exist "backend\venv\" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
)

REM Check if node_modules exists
if not exist "frontend\node_modules\" (
    echo Installing frontend dependencies...
    cd frontend
    npm install
    cd ..
)

echo.
echo Setup complete!
echo.
echo Starting servers...
echo   - Backend: http://localhost:5000
echo   - Frontend: http://localhost:3000
echo.
echo Press Ctrl+C to stop both servers
echo.

REM Start backend
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python app.py"

REM Wait a bit for backend to start
timeout /t 2 /nobreak > nul

REM Start frontend
start "Frontend Server" cmd /k "cd frontend && npm start"
