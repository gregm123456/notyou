"""
AUTOMATIC1111 Stable Diffusion API client for the Not You installation.

This module handles communication with the Stable Diffusion API,
including authentication, request queuing, and response processing.
"""

import logging
import base64
import requests
import time
import threading
from typing import Optional, Callable, Dict, Any
from io import BytesIO

from config import (
    API_TIMEOUT, MAX_RETRIES, REQUEST_DELAY,
    DEFAULT_STEPS, DEFAULT_CFG_SCALE, DEFAULT_SAMPLER,
    DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_SEED, NEGATIVE_PROMPT
)
from secrets import API_USERNAME, API_PASSWORD, API_BASE_URL
from src.utils.error_handling import ErrorHandler


logger = logging.getLogger(__name__)


class APIClient:
    """Client for AUTOMATIC1111 Stable Diffusion API."""
    
    def __init__(self):
        """Initialize the API client."""
        self.base_url = API_BASE_URL
        self.username = API_USERNAME
        self.password = API_PASSWORD
        self.error_handler = ErrorHandler()
        
        # Request management
        self.current_request_id = 0
        self.active_requests = set()
        self.request_lock = threading.Lock()
        
        logger.info(f"API client initialized for {self.base_url}")
    
    def generate_image(self, prompt: str, app_state, on_success: Callable[[bytes], None], 
                      on_error: Callable[[Exception], None]):
        """
        Generate an image from a text prompt asynchronously.
        
        Args:
            prompt: Text prompt for image generation
            app_state: Application state for getting current seed
            on_success: Callback for successful generation (receives image bytes)
            on_error: Callback for errors (receives Exception)
        """
        try:
            # Generate unique request ID
            with self.request_lock:
                request_id = self.current_request_id
                self.current_request_id += 1
                self.active_requests.add(request_id)
            
            logger.info(f"Starting image generation request {request_id}")
            
            # Start generation in separate thread
            thread = threading.Thread(
                target=self._generate_image_worker,
                args=(request_id, prompt, app_state, on_success, on_error),
                daemon=True
            )
            thread.start()
            
        except Exception as e:
            self.error_handler.handle_error(e, "Error starting image generation")
            on_error(e)
    
    def _generate_image_worker(self, request_id: int, prompt: str, app_state,
                              on_success: Callable[[bytes], None],
                              on_error: Callable[[Exception], None]):
        """Worker thread for image generation."""
        try:
            # Check if request was cancelled
            if not self._is_request_active(request_id):
                logger.info(f"Request {request_id} was cancelled before starting")
                return
            
            # Prepare API payload
            payload = self._create_api_payload(prompt, app_state)
            
            # Check again before making request
            if not self._is_request_active(request_id):
                logger.info(f"Request {request_id} was cancelled before API call")
                return
            
            # Make API request with retries
            response_data = self._make_api_request(payload, request_id)
            
            # Check if request is still active after API call
            if not self._is_request_active(request_id):
                logger.info(f"Request {request_id} was cancelled after API call")
                return
            
            # Process response
            if response_data and 'images' in response_data:
                image_bytes = self._process_image_response(response_data)
                
                # Final check before callback
                if self._is_request_active(request_id):
                    on_success(image_bytes)
                    logger.info(f"Image generation request {request_id} completed successfully")
            else:
                raise Exception("No images in API response")
                
        except Exception as e:
            # Only call error callback if request is still active
            if self._is_request_active(request_id):
                self.error_handler.handle_error(e, f"Image generation failed for request {request_id}")
                on_error(e)
        finally:
            # Clean up request tracking
            with self.request_lock:
                self.active_requests.discard(request_id)
    
    def _is_request_active(self, request_id: int) -> bool:
        """Check if a request is still active (not cancelled)."""
        with self.request_lock:
            return request_id in self.active_requests
    
    def cancel_pending_requests(self):
        """Cancel all pending image generation requests."""
        try:
            with self.request_lock:
                cancelled_count = len(self.active_requests)
                self.active_requests.clear()
                
            if cancelled_count > 0:
                logger.info(f"Cancelled {cancelled_count} pending requests")
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error cancelling requests")
    
    def _create_api_payload(self, prompt: str, app_state) -> Dict[str, Any]:
        """Create the API request payload."""
        # Get current seed from app state
        current_seed = app_state.get_current_seed() if app_state else DEFAULT_SEED
        
        return {
            "prompt": prompt,
            "negative_prompt": NEGATIVE_PROMPT,
            "steps": DEFAULT_STEPS,
            "cfg_scale": DEFAULT_CFG_SCALE,
            "sampler_name": DEFAULT_SAMPLER,
            "width": DEFAULT_WIDTH,
            "height": DEFAULT_HEIGHT,
            "batch_size": 1,
            "n_iter": 1,
            "seed": current_seed,  # Use dynamic seed from app state
            "restore_faces": False,
            "tiling": False,
            "do_not_save_samples": True,
            "do_not_save_grid": True
        }
    
    def _make_api_request(self, payload: Dict[str, Any], request_id: int) -> Optional[Dict[str, Any]]:
        """Make the actual API request with retries."""
        url = f"{self.base_url}/sdapi/v1/txt2img"
        auth = (self.username, self.password)
        
        for attempt in range(MAX_RETRIES):
            try:
                # Check if request was cancelled during retries
                if not self._is_request_active(request_id):
                    return None
                
                logger.debug(f"Making API request attempt {attempt + 1} for request {request_id}")
                
                response = requests.post(
                    url=url,
                    json=payload,
                    auth=auth,
                    timeout=API_TIMEOUT
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    logger.debug(f"API response received with {len(response_data.get('images', []))} images")
                    return response_data
                else:
                    # Don't log the full response text as it might contain large data
                    error_msg = f"API request failed with status {response.status_code}"
                    logger.warning(error_msg)
                    
                    if attempt == MAX_RETRIES - 1:
                        raise Exception(error_msg)
                    
            except requests.exceptions.Timeout:
                error_msg = f"API request timeout (attempt {attempt + 1})"
                logger.warning(error_msg)
                
                if attempt == MAX_RETRIES - 1:
                    raise Exception("API request timed out after all retries")
                    
            except requests.exceptions.ConnectionError:
                error_msg = f"API connection error (attempt {attempt + 1})"
                logger.warning(error_msg)
                
                if attempt == MAX_RETRIES - 1:
                    raise Exception("Could not connect to API after all retries")
            
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    raise e
                else:
                    logger.warning(f"API request error (attempt {attempt + 1}): {e}")
            
            # Wait before retry (unless request was cancelled)
            if self._is_request_active(request_id) and attempt < MAX_RETRIES - 1:
                time.sleep(REQUEST_DELAY)
        
        return None
    
    def _process_image_response(self, response_data: Dict[str, Any]) -> bytes:
        """Process the API response and extract image bytes."""
        try:
            # Get the first image from the response
            if 'images' not in response_data or not response_data['images']:
                raise Exception("No images in response")
            
            base64_image = response_data['images'][0]
            
            # Validate base64 data length before processing
            if len(base64_image) > 10000000:  # ~10MB limit
                logger.warning(f"Base64 image data is very large: {len(base64_image)} characters")
            
            # Decode base64 image
            image_bytes = base64.b64decode(base64_image)
            
            logger.debug(f"Processed image response: {len(image_bytes)} bytes")
            return image_bytes
            
        except Exception as e:
            # Don't log the full response data as it might contain large base64 images
            raise Exception(f"Error processing image response: {str(e)[:100]}")  # Truncate error message
    
    def test_connection(self) -> bool:
        """Test the API connection."""
        try:
            url = f"{self.base_url}/sdapi/v1/options"
            auth = (self.username, self.password)
            
            response = requests.get(url, auth=auth, timeout=10)
            
            if response.status_code == 200:
                logger.info("API connection test successful")
                return True
            else:
                logger.warning(f"API connection test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.warning(f"API connection test error: {e}")
            return False
    
    def get_api_info(self) -> Optional[Dict[str, Any]]:
        """Get API information and status."""
        try:
            url = f"{self.base_url}/sdapi/v1/options"
            auth = (self.username, self.password)
            
            response = requests.get(url, auth=auth, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            logger.warning(f"Error getting API info: {e}")
            return None
