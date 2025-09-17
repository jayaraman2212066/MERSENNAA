@echo off
echo 🚀 STARTING REVOLUTIONARY MERSENNE DISCOVERY 🚀
echo ================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Install required packages if not already installed
echo 📦 Installing required packages...
pip install numpy psutil matplotlib >nul 2>&1

REM Run the discovery system
echo 🚀 Launching Revolutionary Mersenne Discovery System...
echo.

REM Quick test mode (small range for testing)
echo 🧪 Running in QUICK TEST mode (small range for testing)
python run_revolutionary_discovery.py --quick-test --dashboard --save-patterns

echo.
echo ✅ Discovery session complete!
echo 📁 Check the generated JSON files for results
echo.
pause
