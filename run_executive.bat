@echo off
echo 🏆 Starting BiteBalance Executive Dashboard
echo ==========================================

REM Check if .env exists
if not exist .env (
    echo ❌ .env file not found!
    echo Please run: python setup.py
    pause
    exit /b 1
)

REM Start the Executive Dashboard
echo 🚀 Launching Executive Decision Intelligence Dashboard...
echo.
echo 📊 Professional-grade meal optimization
echo 🎯 Multi-dimensional trade-off analysis
echo 🛡️ Executive constraint enforcement
echo.
echo Access at: http://localhost:8502
echo.

streamlit run app_executive.py

pause