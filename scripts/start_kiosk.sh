#!/bin/bash

# Kiosk mode startup script for the Not You art installation
# This script starts the application in full-screen kiosk mode

set -e

# Configuration
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_VENV="$APP_DIR/venv"
LOG_FILE="$APP_DIR/logs/kiosk_startup.log"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "Starting Not You art installation in kiosk mode..."

# Change to application directory
cd "$APP_DIR"

# Check if virtual environment exists
if [ ! -d "$PYTHON_VENV" ]; then
    log "ERROR: Virtual environment not found at $PYTHON_VENV"
    log "Please run scripts/install.sh first"
    exit 1
fi

# Activate virtual environment
log "Activating virtual environment..."
source "$PYTHON_VENV/bin/activate"

# Check if main.py exists
if [ ! -f "main.py" ]; then
    log "ERROR: main.py not found in $APP_DIR"
    exit 1
fi

# Set environment variables for kiosk mode
export KIVY_WINDOW_WIDTH=1024
export KIVY_WINDOW_HEIGHT=600
export KIVY_NO_CONSOLE=1

# Disable screen saver and power management (on Raspberry Pi)
if command -v xset &> /dev/null; then
    log "Disabling screen saver and power management..."
    xset s off
    xset -dpms
    xset s noblank
fi

# Hide mouse cursor (if unclutter is available)
if command -v unclutter &> /dev/null; then
    log "Hiding mouse cursor..."
    unclutter -idle 0.5 -root &
fi

# Function to restart the application on failure
restart_app() {
    log "Application stopped or crashed. Restarting in 5 seconds..."
    sleep 5
    exec "$0"  # Restart this script
}

# Main application loop with auto-restart
log "Starting main application..."
while true; do
    # Set fullscreen mode in config
    python -c "
import sys
sys.path.insert(0, '.')
from config import *
# Update config for kiosk mode
import configparser
config = configparser.ConfigParser()
config.read_dict({'graphics': {'fullscreen': '1', 'borderless': '1'}})
"

    # Start the application
    if python main.py; then
        log "Application exited normally"
        break
    else
        exit_code=$?
        log "Application exited with code $exit_code"
        
        # If exit code indicates a restart is needed, restart
        if [ $exit_code -eq 2 ]; then
            restart_app
        else
            log "Application stopped. Exiting kiosk mode."
            break
        fi
    fi
done

log "Kiosk mode stopped"
