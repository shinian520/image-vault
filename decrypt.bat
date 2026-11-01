@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo ============================================
echo  image-vault 解密
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [x] 没找到 python。装一个 Python 3.8+ 再来。
    pause
    exit /b 1
)

python -c "import cryptography" >nul 2>nul
if errorlevel 1 (
    echo [*] 首次运行，安装 cryptography ...
    python -m pip install --quiet cryptography
    if errorlevel 1 (
        echo [x] 安装失败。手动执行: python -m pip install cryptography
        pause
        exit /b 1
    )
)

echo [*] 开始解密 ...
python decrypt.py
if errorlevel 1 (
    echo.
    echo [x] 解密失败。常见原因：KEY.txt 与分卷不匹配，或文件下载不完整。
    pause
    exit /b 1
)

echo.
echo [ok] 完成，输出在 out\ 目录。
pause
