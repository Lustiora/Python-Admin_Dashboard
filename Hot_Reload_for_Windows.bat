@echo off
chcp 65001 >nul
cd /d "%~dp0"

set PYTHONPATH=%~dp0

taskkill /F /IM python.exe /T >nul 2>&1

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate
) else (
    echo ❌ Error: .venv not found.
    pause
    exit /b
)

echo ---------------------------------------------------
echo 🚀 Flet Hot Reload (Source Isolated & PYTHONPATH Fixed)
echo [Web Mode] http://localhost:34636
echo ---------------------------------------------------

start http://localhost:34636
set FLET_NO_BROWSER=1

watchfiles "python class_src/test_main_ui.py" src

pause
