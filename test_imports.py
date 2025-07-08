#!/usr/bin/env python3
"""
Minimal test for the "Not You" art installation components.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

print("Testing imports...")

try:
    from config import WINDOW_WIDTH, WINDOW_HEIGHT
    print("✓ Config imported")
except Exception as e:
    print(f"✗ Config import failed: {e}")

try:
    from src.utils.logging import setup_logging
    print("✓ Logging utils imported")
except Exception as e:
    print(f"✗ Logging utils import failed: {e}")

try:
    from src.utils.error_handling import ErrorHandler
    print("✓ Error handling imported")
except Exception as e:
    print(f"✗ Error handling import failed: {e}")

try:
    from src.data.state import ApplicationState
    print("✓ Application state imported")
except Exception as e:
    print(f"✗ Application state import failed: {e}")

try:
    from src.data.form_mapping import FormToPromptMapper
    print("✓ Form mapping imported")
except Exception as e:
    print(f"✗ Form mapping import failed: {e}")

try:
    from src.api.client import APIClient
    print("✓ API client imported")
except Exception as e:
    print(f"✗ API client import failed: {e}")

print("\nTesting object creation...")

try:
    app_state = ApplicationState()
    print("✓ ApplicationState created")
except Exception as e:
    print(f"✗ ApplicationState creation failed: {e}")
    import traceback
    traceback.print_exc()

try:
    error_handler = ErrorHandler()
    print("✓ ErrorHandler created")
except Exception as e:
    print(f"✗ ErrorHandler creation failed: {e}")

try:
    form_mapper = FormToPromptMapper()
    print("✓ FormToPromptMapper created")
except Exception as e:
    print(f"✗ FormToPromptMapper creation failed: {e}")

try:
    api_client = APIClient()
    print("✓ APIClient created")
except Exception as e:
    print(f"✗ APIClient creation failed: {e}")

print("\nAll basic components tested!")
