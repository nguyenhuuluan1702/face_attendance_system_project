#!/bin/bash

echo "========================================"
echo " Face Recognition System - Auto Setup"
echo "========================================"
echo ""

echo "[1/5] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed!"
    echo "Install: sudo apt-get install python3 python3-venv python3-pip"
    exit 1
fi
python3 --version
echo "OK - Python is installed"
echo ""

echo "[2/5] Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv .venv
    echo "OK - Created .venv"
fi
echo ""

echo "[3/5] Installing dependencies..."
echo "(This may take 2-3 minutes, please wait...)"
echo "Using Python from .venv (avoiding global Python conflict)"
echo ""
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install mediapipe==0.10.9 protobuf==3.20.3
.venv/bin/pip uninstall tensorflow tensorflow-intel -y
.venv/bin/pip install tensorflow==2.16.1 tf-keras==2.16.0
.venv/bin/pip install deepface opencv-contrib-python numpy scipy pillow
echo ""

echo "[4/5] Verifying installation..."
.venv/bin/python -c "import mediapipe as mp; print('MediaPipe:', mp.__version__)"
.venv/bin/python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
.venv/bin/python -c "from deepface import DeepFace; print('DeepFace: OK')"
.venv/bin/python -c "import cv2; print('OpenCV:', cv2.__version__)"
echo ""

echo "========================================"
echo " INSTALLATION SUCCESSFUL!"
echo "========================================"
echo ""
echo "How to use:"
echo "1. Add photos to known_faces/"
echo "2. Run: ./run.sh"
echo "3. Press SPACE to recognize"
echo ""
echo "Read more: QUICKSTART.md"
echo "========================================"
