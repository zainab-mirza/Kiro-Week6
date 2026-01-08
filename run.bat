@echo off
echo 🥗 Starting BiteBalance - The AI Menu Referee
echo ============================================

REM Check if .env exists
if not exist .env (
    echo ❌ .env file not found!
    echo Please run: python setup.py
    pause
    exit /b 1
)

REM Start the Streamlit app
echo 🚀 Launching BiteBalance...
streamlit run app.py

pause