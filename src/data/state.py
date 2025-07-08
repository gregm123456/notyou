"""
Application state management for the Not You installation.
"""

import logging
from typing import Dict, Optional, Callable, Any
from threading import Lock


logger = logging.getLogger(__name__)


class ApplicationState:
    """Thread-safe application state manager."""
    
    def __init__(self):
        """Initialize the application state."""
        self._state = {}
        self._lock = Lock()
        self._observers = {}
        self._general_callback = None
        
        # Initialize default state
        self._state['form_data'] = {}
        self._state['current_image'] = None
        self._state['current_prompt'] = ""
        self._state['generating_image'] = False
        self._state['api_status'] = "idle"
        self._state['last_generation_time'] = None
        
    def reset_form_data(self):
        """Reset all form data to default values."""
        with self._lock:
            self._state['form_data'] = {
                'age': '?',
                'gender': '?',
                'ethnicity': '?',
                'education': '?',
                'employment': '?',
                'income': '?'
            }
        self._notify_observers('form_data_reset')
    
    def update_form_field(self, field_name: str, value: str):
        """
        Update a single form field value.
        
        Args:
            field_name: Name of the form field
            value: New value for the field
        """
        with self._lock:
            if 'form_data' not in self._state:
                self._state['form_data'] = {}
            self._state['form_data'][field_name] = value
        
        logger.info(f"Form field updated: {field_name} = {value}")
        self._notify_observers('form_field_changed', field_name, value)
    
    def get_form_data(self) -> Dict[str, str]:
        """
        Get all current form data.
        
        Returns:
            Dictionary of form field values
        """
        with self._lock:
            return self._state.get('form_data', {}).copy()
    
    def get_form_field(self, field_name: str) -> Optional[str]:
        """
        Get the value of a specific form field.
        
        Args:
            field_name: Name of the form field
            
        Returns:
            Current value of the field or None if not set
        """
        with self._lock:
            return self._state.get('form_data', {}).get(field_name)
    
    def get_current_image(self) -> Optional[bytes]:
        """
        Get the current generated image data.
        
        Returns:
            Raw image bytes or None
        """
        with self._lock:
            return self._state.get('current_image')
    
    def set_current_prompt(self, prompt: str):
        """
        Set the current prompt text.
        
        Args:
            prompt: Prompt text used for generation
        """
        with self._lock:
            self._state['current_prompt'] = prompt
        
        self._notify_observers('prompt_updated', prompt)
    
    def get_current_prompt(self) -> str:
        """
        Get the current prompt text.
        
        Returns:
            Current prompt text
        """
        with self._lock:
            return self._state.get('current_prompt', '')
    
    def set_api_status(self, status: str):
        """
        Set the current API status.
        
        Args:
            status: API status ('idle', 'generating', 'error')
        """
        with self._lock:
            self._state['api_status'] = status
        
        logger.info(f"API status changed: {status}")
        self._notify_observers('api_status_changed', status)
    
    def get_api_status(self) -> str:
        """
        Get the current API status.
        
        Returns:
            Current API status
        """
        with self._lock:
            return self._state.get('api_status', 'idle')
    
    def set_last_generation_time(self, timestamp: Optional[float]):
        """
        Set the timestamp of the last image generation.
        
        Args:
            timestamp: Unix timestamp or None
        """
        with self._lock:
            self._state['last_generation_time'] = timestamp
        
        self._notify_observers('generation_time_updated', timestamp)
    
    def get_last_generation_time(self) -> Optional[float]:
        """
        Get the timestamp of the last image generation.
        
        Returns:
            Unix timestamp or None
        """
        with self._lock:
            return self._state.get('last_generation_time')
    
    def has_any_selections(self) -> bool:
        """
        Check if any form fields have been selected (not '?').
        
        Returns:
            True if at least one field has a non-default value
        """
        form_data = self.get_form_data()
        return any(value != '?' for value in form_data.values())
    
    def add_observer(self, event_type: str, callback: Callable):
        """
        Add an observer for state changes.
        
        Args:
            event_type: Type of event to observe
            callback: Function to call when event occurs
        """
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(callback)
        logger.debug(f"Observer added for event: {event_type}")
    
    def remove_observer(self, event_type: str, callback: Callable):
        """
        Remove an observer for state changes.
        
        Args:
            event_type: Type of event
            callback: Function to remove
        """
        if event_type in self._observers:
            try:
                self._observers[event_type].remove(callback)
                logger.debug(f"Observer removed for event: {event_type}")
            except ValueError:
                logger.warning(f"Observer not found for event: {event_type}")
    
    def _notify_observers(self, event_type: str, *args, **kwargs):
        """
        Notify all observers of a state change.
        
        Args:
            event_type: Type of event that occurred
            *args: Additional arguments to pass to observers
            **kwargs: Additional keyword arguments to pass to observers
        """
        if event_type in self._observers:
            for callback in self._observers[event_type]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in observer callback for {event_type}: {e}")
    
    def bind_callback(self, callback: Callable):
        """
        Bind a callback to state changes (simplified interface for UI).
        
        Args:
            callback: Function to call when state changes (field_name, new_value)
        """
        self._general_callback = callback
    
    def set_form_data(self, form_data: Dict[str, str]):
        """
        Set the complete form data and notify observers.
        
        Args:
            form_data: Dictionary of form field values
        """
        with self._lock:
            self._state['form_data'] = form_data.copy()
        
        self._notify_observers('form_data', form_data)
        if hasattr(self, '_general_callback'):
            try:
                self._general_callback('form_data', form_data)
            except Exception as e:
                logger.error(f"Error in general callback: {e}")
    
    def set_generating_image(self, is_generating: bool):
        """
        Set whether an image is currently being generated.
        
        Args:
            is_generating: True if generating, False otherwise
        """
        with self._lock:
            self._state['generating_image'] = is_generating
        
        self._notify_observers('generating_image', is_generating)
        if hasattr(self, '_general_callback'):
            try:
                self._general_callback('generating_image', is_generating)
            except Exception as e:
                logger.error(f"Error in general callback: {e}")
    
    def set_current_image(self, image_data: Optional[bytes]):
        """
        Set the current generated image data.
        
        Args:
            image_data: Raw image bytes or None
        """
        with self._lock:
            self._state['current_image'] = image_data
        
        self._notify_observers('current_image', image_data)
        if hasattr(self, '_general_callback'):
            try:
                self._general_callback('current_image', image_data)
            except Exception as e:
                logger.error(f"Error in general callback: {e}")
    
    def set_current_prompt(self, prompt: str):
        """
        Set the current prompt text.
        
        Args:
            prompt: Prompt text used for generation
        """
        with self._lock:
            self._state['current_prompt'] = prompt
        
        self._notify_observers('current_prompt', prompt)
        if hasattr(self, '_general_callback'):
            try:
                self._general_callback('current_prompt', prompt)
            except Exception as e:
                logger.error(f"Error in general callback: {e}")
    
    def get_state_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current application state.
        
        Returns:
            Dictionary with state summary
        """
        with self._lock:
            return {
                'form_data': self._state.get('form_data', {}),
                'current_prompt': self._state.get('current_prompt', ''),
                'api_status': self._state.get('api_status', 'idle'),
                'has_image': self._state.get('current_image') is not None,
                'last_generation_time': self._state.get('last_generation_time'),
                'has_selections': self.has_any_selections()
            }


# Global application state instance
app_state = ApplicationState()
