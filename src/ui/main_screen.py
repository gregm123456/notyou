"""
Main screen for the Not You art installation.

This is the primary UI component that manages the overall layout with
the image panel on the left and the demographics form panel on the right.
"""

import logging
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

from config import (
    IMAGE_PANEL_WIDTH_RATIO, FORM_PANEL_WIDTH_RATIO, 
    COLOR_BACKGROUND, PADDING
)
from src.ui.image_panel import ImagePanel
from src.ui.form_panel import FormPanel
from src.data.state import ApplicationState
from src.api.client import APIClient
from src.utils.error_handling import ErrorHandler


logger = logging.getLogger(__name__)


class MainScreen(BoxLayout):
    """Main screen containing image panel and form panel."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Configure layout
        self.orientation = 'horizontal'
        self.spacing = PADDING
        self.padding = PADDING
        
        # Set background color
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*COLOR_BACKGROUND)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_background, size=self._update_background)
        
        # Initialize components
        self.app_state = ApplicationState()
        self.api_client = APIClient()
        self.error_handler = ErrorHandler()
        
        # Import form mapper for prompt generation
        from src.data.form_mapping import FormToPromptMapper
        self.form_mapper = FormToPromptMapper()
        
        # Create UI panels
        self._create_panels()
        
        # Bind state changes to UI updates
        self.app_state.bind_callback(self._on_state_change)
        
        # Test image generation (temporary for debugging)
        from kivy.clock import Clock
        Clock.schedule_once(self._test_image_generation, 3.0)  # Wait 3 seconds for UI to be ready
        
        logger.info("Main screen initialized")
    
    def _test_image_generation(self, dt):
        """Test image generation with a simple prompt."""
        try:
            logger.info("Testing image generation with form data")
            
            # Only set form data - let the form mapping generate the prompt
            test_form_data = {"gender": "Male"}
            self.app_state.set_form_data(test_form_data)
            
        except Exception as e:
            logger.error(f"Error in test image generation: {e}")
    
    def _update_background(self, instance, value):
        """Update background rectangle size."""
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def _create_panels(self):
        """Create and add the image and form panels."""
        try:
            # Create image panel (left side)
            self.image_panel = ImagePanel(
                app_state=self.app_state,
                size_hint=(IMAGE_PANEL_WIDTH_RATIO, 1)
            )
            self.add_widget(self.image_panel)
            
            # Create form panel (right side)
            self.form_panel = FormPanel(
                app_state=self.app_state,
                size_hint=(FORM_PANEL_WIDTH_RATIO, 1)
            )
            self.add_widget(self.form_panel)
            
        except Exception as e:
            self.error_handler.handle_error(e, "Failed to create UI panels")
            # Add error message instead
            error_label = Label(
                text="UI Error - Please restart",
                font_size=24,
                color=(1, 0, 0, 1)
            )
            self.add_widget(error_label)
    
    def _on_state_change(self, field_name, new_value):
        """Handle application state changes."""
        try:
            # Log state changes but handle binary data appropriately
            if field_name == 'current_image':
                if new_value is not None:
                    logger.info(f"State change: {field_name} = <image data: {len(new_value)} bytes>")
                else:
                    logger.info(f"State change: {field_name} = None")
            else:
                logger.info(f"State change: {field_name} = {new_value}")
            
            # Trigger image generation when form data changes
            if field_name == 'form_data':
                # Build prompt from form data
                form_data = new_value or {}
                if form_data:  # Only build prompt if we have form data
                    prompt = self.form_mapper.build_prompt(form_data)
                    logger.info(f"Built prompt from form data: {prompt}")
                    self.app_state.set_current_prompt(prompt)
                    # Trigger generation after setting prompt
                    self._trigger_image_generation()
            # Don't trigger on current_prompt changes to avoid double generation
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error handling state change")
    
    def _trigger_image_generation(self):
        """Trigger image generation based on current form data."""
        try:
            # Cancel any pending requests
            self.api_client.cancel_pending_requests()
            
            # Get current prompt from state
            prompt = self.app_state.get_current_prompt()
            if prompt:
                logger.info(f"Triggering image generation with prompt: {prompt}")
                
                # Start image generation (non-blocking)
                Clock.schedule_once(
                    lambda dt: self._generate_image_async(prompt), 
                    0.1
                )
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error triggering image generation")
    
    def _generate_image_async(self, prompt):
        """Generate image asynchronously."""
        try:
            # Set generating state
            self.app_state.set_generating_image(True)
            
            # Make API request
            def on_success(image_data):
                """Called when image generation succeeds."""
                try:
                    self.app_state.set_current_image(image_data)
                    self.app_state.set_generating_image(False)
                    logger.info("Image generated successfully")
                except Exception as e:
                    self.error_handler.handle_error(e, "Error processing generated image")
                    self.app_state.set_generating_image(False)
            
            def on_error(error):
                """Called when image generation fails."""
                self.error_handler.handle_error(error, "Image generation failed")
                self.app_state.set_generating_image(False)
            
            # Submit request to API client
            self.api_client.generate_image(
                prompt=prompt,
                on_success=on_success,
                on_error=on_error
            )
            
        except Exception as e:
            self.error_handler.handle_error(e, "Error in async image generation")
            self.app_state.set_generating_image(False)
