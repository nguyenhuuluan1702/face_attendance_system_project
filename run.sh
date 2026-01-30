#!/bin/bash

echo "========================================"
echo " Face Recognition System - Starting..."
echo "========================================"
echo ""

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not created!"
    echo "Please run setup.sh first."
    echo ""
    exit 1
fi

# Run program directly with venv Python (NO activate needed)
.venv/bin/python face_recognition_with_blink.py

# If error, show help
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo " ERROR: Program encountered an issue!"
    echo "========================================"
    echo ""
    echo "Common causes:"
    echo "- Dependencies not installed (run setup.sh)"
    echo "- Camera not working"
    echo "- No photos in known_faces/"
    echo ""
fi
