@echo off
REM FloodWatch - Setup Script for Windows
REM This script installs all dependencies and prepares the system

echo.
echo ======================================
echo  FloodWatch - Setup & Initialization
echo ======================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [2/5] Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\Activate.bat
) else (
    echo [2/5] Virtual environment already exists, activating...
    call .venv\Scripts\Activate.bat
)
echo.

REM Upgrade pip
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
pip install -r webapp\requirements.txt --quiet
echo.

REM Install additional development dependencies
echo [5/5] Installing development dependencies...
pip install jupyter jupyterlab scipy scikit-optimize --quiet
echo.

echo ======================================
echo ✓ Setup Complete!
echo ======================================
echo.
echo Available Commands:
echo.
echo   Flask Dashboard:    python webapp\app.py
echo   Streamlit App:      streamlit run webapp\streamlit_app.py
echo   Attention Analysis: jupyter notebook notebooks\attention_analysis.ipynb
echo   Report Generator:   python notebooks\generate_attention_report.py
echo.
echo Open http://localhost:5000 after running Flask dashboard
echo.
pause

