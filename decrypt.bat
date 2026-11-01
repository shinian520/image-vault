@echo off
setlocal
cd /d "%~dp0"
echo ============================================
echo  image-vault decrypt
echo ============================================
echo.
where python >nul 2>nul
if errorlevel 1 (
    echo [x] python not found. Install Python 3.8+ first.
    pause
    exit /b 1
)
python -c "import cryptography" >nul 2>nul
if errorlevel 1 (
    echo [*] installing cryptography ...
    python -m pip install --quiet cryptography
    if errorlevel 1 (
        echo [x] pip install failed. Run manually: python -m pip install cryptography
        pause
        exit /b 1
    )
)
echo [*] decrypting ...
python decrypt.py
if errorlevel 1 (
    echo.
    echo [x] failed. Check: KEY.txt matches parts, all parts downloaded fully.
    pause
    exit /b 1
)
echo.
echo [ok] done. files are in .\out\
pause
