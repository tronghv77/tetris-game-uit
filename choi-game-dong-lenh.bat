@echo off
rem ============================================================
rem  Ban chay trong cua so dong lenh, dung nhu ma nguon goc.
rem ============================================================
cd /d "%~dp0"
setlocal

set "PY="
for %%P in (python.exe) do if not defined PY set "PY=%%~$PATH:P"
if not defined PY for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if exist "%%D\python.exe" set "PY=%%D\python.exe"
)
if not defined PY for /d %%D in ("%ProgramFiles%\Python3*") do (
    if exist "%%D\python.exe" set "PY=%%D\python.exe"
)
if not defined PY if exist "%WINDIR%\py.exe" set "PY=%WINDIR%\py.exe"

if not defined PY goto khong_co_python

title Tetris - Nhom 07
mode con cols=50 lines=32
"%PY%" "%~dp0tetris.py"
echo.
echo   Game da ket thuc. Bam phim bat ky de dong cua so.
pause >nul
exit /b 0

:khong_co_python
echo.
echo   Khong tim thay Python tren may nay.
echo   Tai tai: https://www.python.org/downloads/
echo.
pause
exit /b 1
