#!/bin/bash

echo "========================================"
echo "Medical Image Analyzer - Startup Script"
echo "========================================"
echo ""

echo "Installing Python packages..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Starting Medical Image Analyzer..."
echo "========================================"
echo ""
echo "Opening browser: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
