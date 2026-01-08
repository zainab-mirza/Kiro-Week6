@echo off
echo 🏆 BiteBalance - Dual Launch
echo ============================

echo.
echo 🚀 Starting both versions of BiteBalance...
echo.

echo 📱 Original Version: http://localhost:8502
echo 🏆 Executive Dashboard: http://localhost:8503
echo.

echo ✅ Both applications are now running!
echo.
echo Choose your version:
echo [1] Original BiteBalance - http://localhost:8502
echo [2] Executive Dashboard - http://localhost:8503
echo.

start http://localhost:8502
start http://localhost:8503

echo 🎯 Both browsers should open automatically
echo Press any key to continue...
pause > nul