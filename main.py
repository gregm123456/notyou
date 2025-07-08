#!/usr/bin/env python3
"""
Main entry point for the "Not You" art installation.

This kiosk application explores demographics and inherent biases in AI-generated images
by allowing users to interact with a demographics form and generating portraits
based on their selections using Stable Diffusion API.
"""

import sys
import os
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config

# Configure Kivy before importing other Kivy modules
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FULLSCREEN

# Set window size for consistent development
Config.set('graphics', 'width', str(WINDOW_WIDTH))
Config.set('graphics', 'height', str(WINDOW_HEIGHT))
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'borderless', str(FULLSCREEN))

from src.utils.logging import setup_logging
from src.utils.error_handling import ErrorHandler
from src.ui.main_screen import MainScreen


class NotYouApp(App):
    """Main Kivy application for the Not You installation."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Not You - Art Installation"
        self.error_handler = ErrorHandler()
        
    def build(self):
        """Build and return the root widget."""
        try:
            # Skip logging setup for now
            print("Creating main screen...")
            main_screen = MainScreen()
            print("Main screen created successfully")
            
            # Schedule error recovery check
            Clock.schedule_interval(self.check_health, 30.0)  # Every 30 seconds
            
            return main_screen
            
        except Exception as e:
            print(f"Error in build(): {e}")
            import traceback
            traceback.print_exc()
            # Return a minimal error screen
            from kivy.uix.label import Label
            return Label(text="Application Error - Please restart", 
                        font_size=32, halign="center")
    
    def check_health(self, dt):
        """Periodic health check for the application."""
        try:
            # Check if main components are responsive
            # This could include API connectivity, memory usage, etc.
            logger = logging.getLogger(__name__)
            logger.debug("Health check passed")
        except Exception as e:
            self.error_handler.handle_error(e, "Health check failed")
    
    def on_stop(self):
        """Called when the application is about to stop."""
        logger = logging.getLogger(__name__)
        logger.info("Stopping Not You art installation")


def main():
    """Main function to run the application."""
    try:
        # Ensure required directories exist
        os.makedirs("logs", exist_ok=True)
        os.makedirs("assets/ui_elements", exist_ok=True)
        
        # Run the application
        app = NotYouApp()
        app.run()
        
    except Exception as e:
        print(f"Fatal error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
