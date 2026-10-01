@echo off
rem ============================================================
rem  Bam dup vao file nay de choi Tetris ban do hoa.
rem  File tu do duong dan Python, khong can Python nam trong PATH.
rem ============================================================
cd /d "%~dp0"
setlocal

set "PY="

rem 1. Thu tim trong PATH truoc
for %%P in (pythonw.exe) do if not defined PY set "PY=%%~$PATH:P"

rem 2. Thu thu muc cai dat cho tung nguoi dung
if not defined PY for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if exist "%%D\pythonw.exe" set "PY=%%D\pythonw.exe"
)

rem 3. Thu thu muc cai dat cho ca may
if not defined PY for /d %%D in ("%ProgramFiles%\Python3*") do (
    if exist "%%D\pythonw.exe" set "PY=%%D\pythonw.exe"
)

rem 4. Thu bo khoi dong pyw cua Python
if not defined PY if exist "%WINDIR%\pyw.exe" set "PY=%WINDIR%\pyw.exe"

if not defined PY goto khong_co_python

start "Tetris" "%PY%" "%~dp0tetris_gui.py"
exit /b 0

:khong_co_python
echo.
echo   Khong tim thay Python tren may nay.
echo.
echo   Tai ban moi nhat tai: https://www.python.org/downloads/
echo   Khi cai nho tick o "Add Python to PATH".
echo.
pause
exit /b 1
