#!/usr/bin/env python3
"""
Test UI components for the "Not You" installation.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

print("Testing UI imports...")

try:
    import kivy
    from kivy.config import Config
    from config import WINDOW_WIDTH, WINDOW_HEIGHT
    Config.set('graphics', 'width', str(WINDOW_WIDTH))
    Config.set('graphics', 'height', str(WINDOW_HEIGHT))
    Config.set('graphics', 'resizable', False)
    print("✓ Kivy configured")
except Exception as e:
    print(f"✗ Kivy config failed: {e}")

try:
    from src.data.state import ApplicationState
    app_state = ApplicationState()
    print("✓ ApplicationState created")
except Exception as e:
    print(f"✗ ApplicationState creation failed: {e}")

try:
    from src.ui.image_panel import ImagePanel
    print("✓ ImagePanel imported")
except Exception as e:
    print(f"✗ ImagePanel import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.ui.form_panel import FormPanel
    print("✓ FormPanel imported")
except Exception as e:
    print(f"✗ FormPanel import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.ui.main_screen import MainScreen
    print("✓ MainScreen imported")
except Exception as e:
    print(f"✗ MainScreen import failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting UI object creation...")

try:
    # Create a simple UI test
    image_panel = ImagePanel(app_state=app_state)
    print("✓ ImagePanel created")
except Exception as e:
    print(f"✗ ImagePanel creation failed: {e}")
    import traceback
    traceback.print_exc()

print("\nUI components tested!")
