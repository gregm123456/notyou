"""
Error handling utilities for the Not You installation.
"""

import logging
import sys
import traceback
from typing import Optional, Callable, Any


logger = logging.getLogger(__name__)


class NotYouException(Exception):
    """Base exception for Not You application errors."""
    pass


class APIException(NotYouException):
    """Exception for API-related errors."""
    pass


class UIException(NotYouException):
    """Exception for UI-related errors."""
    pass


class ConfigurationException(NotYouException):
    """Exception for configuration-related errors."""
    pass


def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler for unhandled exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.critical(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )


def safe_execute(func: Callable, *args, **kwargs) -> tuple[bool, Any]:
    """
    Safely execute a function and return success status and result.
    
    Args:
        func: Function to execute
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function
        
    Returns:
        tuple: (success: bool, result: Any)
    """
    try:
        result = func(*args, **kwargs)
        return True, result
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {e}")
        logger.debug(traceback.format_exc())
        return False, None


def log_and_continue(func: Callable) -> Callable:
    """
    Decorator that logs exceptions and continues execution.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            logger.debug(traceback.format_exc())
            return None
    return wrapper


def retry_on_failure(max_retries: int = 3, delay: float = 1.0) -> Callable:
    """
    Decorator that retries a function on failure.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            import time
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                        raise
                    else:
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                        time.sleep(delay)
            
        return wrapper
    return decorator


def validate_config(config_dict: dict, required_keys: list) -> bool:
    """
    Validate that a configuration dictionary contains required keys.
    
    Args:
        config_dict: Configuration dictionary to validate
        required_keys: List of required keys
        
    Returns:
        True if all required keys are present
        
    Raises:
        ConfigurationException: If required keys are missing
    """
    missing_keys = [key for key in required_keys if key not in config_dict]
    if missing_keys:
        raise ConfigurationException(f"Missing required configuration keys: {missing_keys}")
    return True


class ErrorHandler:
    """Centralized error handling for the Not You application."""
    
    def __init__(self):
        """Initialize the error handler."""
        self.error_count = 0
        self.last_error_time = None
        
    def handle_error(self, error: Exception, context: str = ""):
        """
        Handle an error with appropriate logging and recovery.
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
        """
        import time
        
        self.error_count += 1
        self.last_error_time = time.time()
        
        # Log the error
        if context:
            logger.error(f"{context}: {error}")
        else:
            logger.error(f"Error: {error}")
        
        # Log the stack trace for debugging
        logger.debug(traceback.format_exc())
        
        # Could add additional error recovery logic here
        # For example, restarting components, showing user messages, etc.
    
    def get_error_stats(self) -> dict:
        """Get error statistics."""
        return {
            'error_count': self.error_count,
            'last_error_time': self.last_error_time
        }
    
    def reset_error_count(self):
        """Reset the error count."""
        self.error_count = 0
        self.last_error_time = None


def setup_global_exception_handler():
    """Set up the global exception handler."""
    sys.excepthook = handle_exception
