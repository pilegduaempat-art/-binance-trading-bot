#!/bin/bash

# Binance Trading Bot - Run Script
# This script starts the trading bot application

echo "🚀 Starting Binance Trading Bot..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/Update dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit is not installed properly"
    exit 1
fi

# Clear cache (optional)
if [ "$1" == "--clear-cache" ]; then
    echo ""
    echo "🧹 Clearing Streamlit cache..."
    rm -rf .streamlit/cache
    echo "✓ Cache cleared"
fi

# Run the application
echo ""
echo "=================================="
echo "  🎯 STARTING TRADING BOT"
echo "=================================="
echo ""
echo "Access the app at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py

# Deactivate virtual environment on exit
deactivate
