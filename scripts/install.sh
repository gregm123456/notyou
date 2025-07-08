#!/bin/bash

# Installation script for the Not You art installation
# This script sets up the Python environment and dependencies

set -e

echo "Installing Not You art installation..."

# Check if Python 3.11 is available
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11 not found. Please install Python 3.11 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p assets/ui_elements
mkdir -p assets/fonts

# Set executable permissions
echo "Setting permissions..."
chmod +x scripts/start_kiosk.sh

echo "Installation complete!"
echo "To start the application:"
echo "  - For development: source venv/bin/activate && python main.py"
echo "  - For kiosk mode: ./scripts/start_kiosk.sh"
echo ""
echo "Make sure to:"
echo "  1. Update secrets.py with your AUTOMATIC1111 API credentials"
echo "  2. Ensure the AUTOMATIC1111 API is running with --api-auth username:password"
echo "  3. Place your placeholder image at assets/ui_elements/unknown_portrait.png"
