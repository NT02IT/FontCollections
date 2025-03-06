@echo off
chcp 65001 > nul
color e
:: Lấy thư mục cha của thư mục hiện tại (%~dp0)
for %%I in ("%~dp0..") do set "PARENT_PATH=%%~fI"

:: Gán đường dẫn đến main.py
set "MAIN_PATH=%PARENT_PATH%\main.py"
python -u "%MAIN_PATH%" %*