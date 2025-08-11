@echo off
echo Installing requirements for PhD Exam Downloader...
echo.

echo Installing Python packages...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✓ Requirements installed successfully!
    echo.
    echo Note: Make sure Google Chrome is installed for Selenium WebDriver support.
    echo If Chrome is not available, the tool will automatically fall back to requests-only mode.
    echo.
    pause
) else (
    echo.
    echo ✗ Error installing requirements. Please check your Python and pip installation.
    echo.
    pause
)