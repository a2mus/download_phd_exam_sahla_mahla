@echo off
echo PhD Exam Downloader for sahla-dz.com
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking and installing requirements...
pip install -r requirements.txt

echo.
echo Starting the downloader...
echo.

python download_exams.py

echo.
echo Download process completed.
echo Check the 'downloaded_exams' folder for the downloaded files.
echo.

pause