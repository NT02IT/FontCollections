@echo off
setlocal

rem Lấy đường dẫn thư mục chứa file .bat
set "SCRIPT_DIR=%~dp0"

rem Lấy đường dẫn folder App\targets
set "TARGETS_DIR=%SCRIPT_DIR%App\targets"

rem Thêm đường dẫn vào biến môi trường PATH
setx PATH "%TARGETS_DIR%;%PATH%" /M

echo Da cap nhat bien moi truong PATH voi: %TARGETS_DIR%
pause