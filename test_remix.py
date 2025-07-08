#!/usr/bin/env python3
"""
Test script for the remix functionality.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from src.data.state import ApplicationState
from config import DEFAULT_SEED

def test_remix_functionality():
    """Test the remix button functionality."""
    print("Testing remix functionality...")
    
    # Create application state
    app_state = ApplicationState()
    
    # Check initial seed
    initial_seed = app_state.get_current_seed()
    print(f"Initial seed: {initial_seed}")
    assert initial_seed == DEFAULT_SEED, f"Expected {DEFAULT_SEED}, got {initial_seed}"
    
    # Generate new random seed
    new_seed = app_state.generate_new_random_seed()
    print(f"Generated new seed: {new_seed}")
    
    # Verify seed changed
    current_seed = app_state.get_current_seed()
    print(f"Current seed after remix: {current_seed}")
    assert current_seed == new_seed, f"Seed not updated correctly"
    assert current_seed != DEFAULT_SEED, f"New seed should be different from default"
    
    # Test setting a specific seed
    test_seed = 12345
    app_state.set_current_seed(test_seed)
    assert app_state.get_current_seed() == test_seed, f"Failed to set specific seed"
    
    print("✅ All remix functionality tests passed!")

if __name__ == "__main__":
    test_remix_functionality()
