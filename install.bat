@echo off
echo Setting up Caption Edit Tool...

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.6 or later.
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo Failed to create virtual environment.
    exit /b 1
)

:: Activate virtual environment and install dependencies
echo Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install dependencies.
    exit /b 1
)

echo.
echo Caption Edit Tool setup complete!
echo You can now use run.bat to start the tool.
echo.
pause
