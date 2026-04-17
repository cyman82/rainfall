# FloodWatch - Setup Script for Windows PowerShell
# This script installs all dependencies and prepares the system

Write-Host "`n" -NoNewline
Write-Host "======================================"
Write-Host " FloodWatch - Setup & Initialization"
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "`n"

# Check Python version
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[1/5] Checking Python installation..." -ForegroundColor Green
    Write-Host "Found $pythonVersion`n"
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    pause
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Green
    python -m venv .venv
    & ".\.venv\Scripts\Activate.ps1"
} else {
    Write-Host "[2/5] Virtual environment already exists, activating..." -ForegroundColor Green
    & ".\.venv\Scripts\Activate.ps1"
}
Write-Host "`n"

# Upgrade pip
Write-Host "[3/5] Upgrading pip..." -ForegroundColor Green
python -m pip install --upgrade pip --quiet
Write-Host "`n"

# Install dependencies
Write-Host "[4/5] Installing main dependencies..." -ForegroundColor Green
pip install -r webapp/requirements.txt --quiet
Write-Host "`n"

# Install additional development dependencies
Write-Host "[5/5] Installing development dependencies..." -ForegroundColor Green
pip install jupyter jupyterlab scipy scikit-optimize --quiet
Write-Host "`n"

Write-Host "======================================"
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "======================================`n"

Write-Host "Available Commands:`n"
Write-Host "  Flask Dashboard:    python webapp\app.py" -ForegroundColor Cyan
Write-Host "  Streamlit App:      streamlit run webapp\streamlit_app.py" -ForegroundColor Cyan
Write-Host "  Attention Analysis: jupyter notebook notebooks\attention_analysis.ipynb" -ForegroundColor Cyan
Write-Host "  Report Generator:   python notebooks\generate_attention_report.py" -ForegroundColor Cyan
Write-Host "`n"
Write-Host "Open http://localhost:5000 after running Flask dashboard`n" -ForegroundColor Yellow
Write-Host "Documentation: See README.md for detailed setup guide`n" -ForegroundColor Yellow

Read-Host "Press Enter to exit"

