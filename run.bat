@echo off
echo ========================================
echo  Face Recognition System - Starting...
echo ========================================
echo.

REM Kiem tra .venv co ton tai khong
if not exist .venv (
    echo ERROR: Virtual environment chua duoc tao!
    echo Vui long chay setup.bat truoc.
    echo.
    pause
    exit /b 1
)

REM Chay truc tiep Python tu .venv (KHONG dung activate)
.venv\Scripts\python.exe face_recognition_with_blink.py

REM Neu loi, giu cua so mo
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo  LOI: Chuong trinh gap su co!
    echo ========================================
    echo.
    echo Cac nguyen nhan thuong gap:
    echo - Chua cai dat dependencies (chay setup.bat)
    echo - Camera khong hoat dong
    echo - Khong co anh trong known_faces/
    echo.
    pause
)
