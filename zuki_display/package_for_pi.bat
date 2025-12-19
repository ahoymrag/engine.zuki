@echo off
REM Package Zuki Display for Raspberry Pi (Windows)
REM This script creates a zip file ready to copy to your Raspberry Pi

echo 📦 Packaging Zuki Display for Raspberry Pi...

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set PARENT_DIR=%SCRIPT_DIR%..

REM Create package directory
set PACKAGE_DIR=%TEMP%\zuki_display_pi
if exist "%PACKAGE_DIR%" rmdir /s /q "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%"

echo 📁 Creating package structure...

REM Copy zuki_display files
echo 📋 Copying zuki_display files...
xcopy /E /I /Y "%SCRIPT_DIR%*" "%PACKAGE_DIR%\"

REM Copy the Zuki folder if it exists
if exist "%PARENT_DIR%\Zuki" (
    echo 📋 Copying Zuki modules for full features...
    mkdir "%PACKAGE_DIR%\Zuki"
    xcopy /E /I /Y "%PARENT_DIR%\Zuki\*" "%PACKAGE_DIR%\Zuki\"
)

REM Create setup script for Raspberry Pi
echo #!/bin/bash > "%PACKAGE_DIR%\setup_pi.sh"
echo # Setup script for Raspberry Pi >> "%PACKAGE_DIR%\setup_pi.sh"
echo. >> "%PACKAGE_DIR%\setup_pi.sh"
echo echo "🤖 Setting up Zuki Display on Raspberry Pi..." >> "%PACKAGE_DIR%\setup_pi.sh"
echo echo "" >> "%PACKAGE_DIR%\setup_pi.sh"
echo. >> "%PACKAGE_DIR%\setup_pi.sh"
echo # Check Python >> "%PACKAGE_DIR%\setup_pi.sh"
echo if ! command -v python3 ^&^> /dev/null; then >> "%PACKAGE_DIR%\setup_pi.sh"
echo     echo "❌ Python 3 not found. Please install Python 3." >> "%PACKAGE_DIR%\setup_pi.sh"
echo     exit 1 >> "%PACKAGE_DIR%\setup_pi.sh"
echo fi >> "%PACKAGE_DIR%\setup_pi.sh"
echo. >> "%PACKAGE_DIR%\setup_pi.sh"
echo echo "✅ Python 3 found: $(python3 --version)" >> "%PACKAGE_DIR%\setup_pi.sh"
echo. >> "%PACKAGE_DIR%\setup_pi.sh"
echo # Install dependencies >> "%PACKAGE_DIR%\setup_pi.sh"
echo echo "" >> "%PACKAGE_DIR%\setup_pi.sh"
echo echo "📦 Installing Python dependencies..." >> "%PACKAGE_DIR%\setup_pi.sh"
echo python3 -m pip install --user -r requirements.txt >> "%PACKAGE_DIR%\setup_pi.sh"
echo python3 -m pip install --user flask-cors >> "%PACKAGE_DIR%\setup_pi.sh"
echo. >> "%PACKAGE_DIR%\setup_pi.sh"
echo chmod +x start.py >> "%PACKAGE_DIR%\setup_pi.sh"
echo chmod +x app.py >> "%PACKAGE_DIR%\setup_pi.sh"
echo. >> "%PACKAGE_DIR%\setup_pi.sh"
echo echo "" >> "%PACKAGE_DIR%\setup_pi.sh"
echo echo "✅ Setup complete!" >> "%PACKAGE_DIR%\setup_pi.sh"
echo echo "" >> "%PACKAGE_DIR%\setup_pi.sh"
echo echo "🚀 To run Zuki Display:" >> "%PACKAGE_DIR%\setup_pi.sh"
echo echo "   python3 start.py" >> "%PACKAGE_DIR%\setup_pi.sh"

REM Create run script
echo #!/bin/bash > "%PACKAGE_DIR%\run.sh"
echo cd "$(dirname "$0")" >> "%PACKAGE_DIR%\run.sh"
echo python3 start.py >> "%PACKAGE_DIR%\run.sh"

REM Create zip file
set ZIP_NAME=zuki_display_pi_%date:~-4,4%%date:~-10,2%%date:~-7,2%.zip
cd /d "%PARENT_DIR%"

REM Use PowerShell to create zip (Windows 10+)
powershell -Command "Compress-Archive -Path '%PACKAGE_DIR%' -DestinationPath '%PARENT_DIR%\%ZIP_NAME%' -Force"

echo.
echo ✅ Package created: %PARENT_DIR%\%ZIP_NAME%
echo.
echo 📦 To copy to Raspberry Pi:
echo    1. Copy %ZIP_NAME% to a USB drive
echo    2. On Raspberry Pi, unzip it: unzip %ZIP_NAME%
echo    3. Run: cd zuki_display_pi ^&^& bash setup_pi.sh
echo    4. Start: python3 start.py
echo.

REM Cleanup
rmdir /s /q "%PACKAGE_DIR%"

pause

