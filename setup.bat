@echo off
REM AI Blog Generator - Windows Setup Script
REM This script helps set up the project quickly on Windows

echo ================================
echo AI Blog Generator Setup
echo ================================
echo.

REM Check Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Check Node.js
echo [2/6] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from nodejs.org
    pause
    exit /b 1
)
echo [OK] Node.js found
echo.

REM Setup Backend
echo [3/6] Setting up backend...
cd backend

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo Downloading spaCy model...
python -m spacy download en_core_web_sm
if errorlevel 1 (
    echo [WARNING] Failed to download spaCy model
    echo You may need to run: python -m spacy download en_core_web_sm
)

echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo [INFO] .env file created. Please edit it with your credentials.
) else (
    echo [INFO] .env file already exists
)

cd ..
echo [OK] Backend setup complete
echo.

REM Setup Frontend
echo [4/6] Setting up frontend...
cd frontend

echo Installing Node.js dependencies...
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install frontend dependencies
    pause
    exit /b 1
)

cd ..
echo [OK] Frontend setup complete
echo.

REM Create start scripts
echo [5/6] Creating start scripts...

REM Create backend start script
echo @echo off > start-backend.bat
echo cd backend >> start-backend.bat
echo call venv\Scripts\activate.bat >> start-backend.bat
echo python app.py >> start-backend.bat

REM Create frontend start script
echo @echo off > start-frontend.bat
echo cd frontend >> start-frontend.bat
echo npm run dev >> start-frontend.bat

echo [OK] Start scripts created
echo.

REM Final instructions
echo [6/6] Setup complete!
echo ================================
echo.
echo NEXT STEPS:
echo.
echo 1. Edit backend\.env with your credentials:
echo    - MONGODB_URI (get from MongoDB Atlas)
echo    - JWT_SECRET_KEY (any random string)
echo    - OPENAI_API_KEY (get from OpenAI)
echo.
echo 2. Start the backend:
echo    - Run: start-backend.bat
echo    - Or manually: cd backend ^&^& venv\Scripts\activate ^&^& python app.py
echo.
echo 3. Start the frontend (in a new terminal):
echo    - Run: start-frontend.bat
echo    - Or manually: cd frontend ^&^& npm run dev
echo.
echo 4. Open http://localhost:5173 in your browser
echo.
echo ================================
echo Need help? Check QUICKSTART.md
echo ================================
echo.
pause
