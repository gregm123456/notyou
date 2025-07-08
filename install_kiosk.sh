#!/bin/bash
# Installation script for Not You art installation kiosk

echo "Setting up Not You art installation kiosk..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Install required system packages for proper display handling
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y unclutter xserver-xorg-legacy x11-xserver-utils

# Configure X11 to allow any user to start X (needed for kiosk mode)
echo "Configuring X11 permissions..."
sudo dpkg-reconfigure xserver-xorg-legacy

# Copy systemd service file
echo "Installing systemd service..."
sudo cp notyou-kiosk.service /etc/systemd/system/
sudo systemctl daemon-reload

# Test virtual environment and dependencies
echo "Testing virtual environment and dependencies..."
source venv/bin/activate
python -c "import kivy; print('Kivy version:', kivy.__version__)"
python -c "import requests; print('Requests imported successfully')"
python -c "import PIL; print('Pillow imported successfully')"
deactivate

# Enable the service (optional - uncomment to auto-start on boot)
# sudo systemctl enable notyou-kiosk.service

echo "Setup complete!"
echo ""
echo "Virtual environment created and dependencies installed."
echo "To test the application manually:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "To start the kiosk manually:"
echo "  ./start_kiosk.sh"
echo ""
echo "To enable auto-start on boot:"
echo "  sudo systemctl enable notyou-kiosk.service"
echo "  sudo systemctl start notyou-kiosk.service"
echo ""
echo "To disable auto-start:"
echo "  sudo systemctl disable notyou-kiosk.service"
