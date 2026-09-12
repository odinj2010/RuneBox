@echo off
setlocal enabledelayedexpansion

echo =====================================================================
echo   RuneBox // Subwoofer Enclosure Lab - Standalone Compiler (.exe)
echo   Engineered by NfgOdin
echo =====================================================================
echo.

:: Detect virtual environment python or fallback to system python
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    set "PYINSTALLER_EXE=.venv\Scripts\pyinstaller.exe"
    echo [OK] Using virtual environment Python: !PYTHON_EXE!
) else (
    set "PYTHON_EXE=python"
    set "PYINSTALLER_EXE=pyinstaller"
    echo [NOTICE] Using system Python: !PYTHON_EXE!
)

echo.
echo [1/3] Checking and installing dependencies...
!PYTHON_EXE! -m pip install --upgrade pip
!PYTHON_EXE! -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements.txt!
    pause
    exit /b %errorlevel%
)

echo.
echo [2/3] Compiling standalone Windows executable with PyInstaller...
!PYINSTALLER_EXE! --noconfirm --onefile --windowed --name "RuneBox" --add-data "assets;assets" --collect-all customtkinter main.py
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller compilation failed!
    pause
    exit /b %errorlevel%
)

echo.
echo =====================================================================
echo [3/3] Build complete! 
echo Executable is located in the dist\ folder: dist\RuneBox.exe
echo =====================================================================
echo.
pause
