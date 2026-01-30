@echo off
echo ========================================
echo  Face Recognition System - Auto Setup
echo ========================================
echo.

echo [1/5] Kiem tra Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python chua duoc cai dat!
    echo Tai Python tai: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK - Python da duoc cai dat
echo.

echo [2/5] Tao virtual environment...
if exist .venv (
    echo Virtual environment da ton tai, skip...
) else (
    python -m venv .venv
    echo OK - Da tao .venv
)
echo.

echo [3/5] Cai dat dependencies...
echo (Co the mat 2-3 phut, vui long doi...)
echo Dang dung Python tu .venv (tranh conflict voi Python global)
echo.
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip.exe install mediapipe==0.10.9 protobuf==3.20.3
.venv\Scripts\pip.exe uninstall tensorflow tensorflow-intel -y
.venv\Scripts\pip.exe install tensorflow==2.16.1 tf-keras==2.16.0
.venv\Scripts\pip.exe install deepface opencv-contrib-python numpy scipy pillow
echo.

echo [4/5] Kiem tra cai dat...
.venv\Scripts\python.exe -c "import mediapipe as mp; print('MediaPipe:', mp.__version__)"
.venv\Scripts\python.exe -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
.venv\Scripts\python.exe -c "from deepface import DeepFace; print('DeepFace: OK')"
.venv\Scripts\python.exe -c "import cv2; print('OpenCV:', cv2.__version__)"
echo.

echo ========================================
echo  CAI DAT THANH CONG!
echo ========================================
echo.
echo Huong dan su dung:
echo 1. Them anh vao thu muc known_faces/
echo 2. Chay: run.bat
echo 3. Nhan SPACE de nhan dien
echo.
echo Doc them: QUICKSTART.md
echo ========================================
pause
