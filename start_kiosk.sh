#!/bin/bash
# Startup script for Not You art installation
# This script configures the display environment and starts the application

# Set display environment variables for Raspberry Pi
export DISPLAY=:0
export SDL_VIDEODRIVER=wayland,x11  # Try Wayland first, fallback to X11
export KIVY_WINDOW=sdl2

# Optimize for Wayland/Xwayland environment
# This reduces xinput calls that cause the warnings
export KIVY_INPUT_PROVIDER=mouse,keyboard

# Disable screen blanking and screensaver for kiosk mode
# Redirect stderr to reduce console noise from xset on Wayland
xset s off 2>/dev/null
xset -dpms 2>/dev/null
xset s noblank 2>/dev/null

# Hide mouse cursor after 2 seconds of inactivity
unclutter -idle 2 &

# Change to application directory
cd /home/notyou/notyou

# Activate virtual environment
source venv/bin/activate

# Start the application
python main.py

# If the application exits, restart it after 5 seconds
while true; do
    echo "Application exited. Restarting in 5 seconds..."
    sleep 5
    source venv/bin/activate  # Re-activate in case it was lost
    python main.py
done
