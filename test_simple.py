#!/usr/bin/env python3
"""
Simple test for the "Not You" art installation.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.config import Config

# Configure Kivy before importing other Kivy modules
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FULLSCREEN

# Set window size for consistent development
Config.set('graphics', 'width', str(WINDOW_WIDTH))
Config.set('graphics', 'height', str(WINDOW_HEIGHT))
Config.set('graphics', 'resizable', False)

class SimpleTestApp(App):
    """Simple test application."""
    
    def build(self):
        """Build and return the root widget."""
        try:
            print("Building test app...")
            
            root = BoxLayout(orientation='horizontal')
            
            # Test left panel
            left_panel = Label(
                text="Image Panel\n(512x512 placeholder)",
                size_hint=(0.45, 1)
            )
            root.add_widget(left_panel)
            
            # Test right panel  
            right_panel = Label(
                text="Form Panel\n(Demographics form will go here)",
                size_hint=(0.55, 1)
            )
            root.add_widget(right_panel)
            
            print("Test app built successfully!")
            return root
            
        except Exception as e:
            print(f"Error building test app: {e}")
            import traceback
            traceback.print_exc()
            return Label(text="Error - see console")

def main():
    """Main function to run the test application."""
    try:
        print("Starting simple test...")
        app = SimpleTestApp()
        app.run()
        
    except Exception as e:
        print(f"Fatal error starting test application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
