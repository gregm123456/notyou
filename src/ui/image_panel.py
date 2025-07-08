"""
Image panel for displaying generated portraits in the Not You installation.

This panel shows the AI-generated portrait image on the left side of the screen,
along with the prompt text used to generate it and status indicators.
"""

import logging
from io import BytesIO
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock

from config import (
    IMAGE_SIZE, PLACEHOLDER_IMAGE, COLOR_BACKGROUND, COLOR_TEXT,
    COLOR_PRIMARY, PADDING, SPACING
)
from src.utils.error_handling import ErrorHandler


logger = logging.getLogger(__name__)


class ImagePanel(BoxLayout):
    """Panel for displaying generated portrait images."""
    
    def __init__(self, app_state, **kwargs):
        super().__init__(**kwargs)
        
        # Configure layout
        self.orientation = 'vertical'
        self.spacing = SPACING
        self.padding = PADDING
        
        # Store references
        self.app_state = app_state
        self.error_handler = ErrorHandler()
        
        # Create UI elements
        self._create_ui()
        
        # Bind to state changes using proper observers
        self.app_state.add_observer('current_image', self._on_image_change)
        self.app_state.add_observer('current_prompt', self._on_prompt_change)
        self.app_state.add_observer('generating_image', self._on_generation_status_change)
        
        logger.info("Image panel initialized")
    
    def _create_ui(self):
        """Create the image panel UI elements."""
        try:
            # Create image display area
            self._create_image_display()
            
            # Create prompt text display
            self._create_prompt_display()
            
            # Create status display
            self._create_status_display()
            
        except Exception as e:
            self.error_handler.handle_error(e, "Failed to create image panel UI")
    
    def _create_image_display(self):
        """Create the main image display widget."""
        # Container for the image to center it
        image_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.7)  # Take 70% of panel height
        )
        
        # The actual image widget
        self.image_widget = Image(
            source=PLACEHOLDER_IMAGE,
            size_hint=(None, None),
            size=(IMAGE_SIZE, IMAGE_SIZE),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Add centering widget
        centering_widget = Widget()
        centering_widget.add_widget(self.image_widget)
        image_container.add_widget(centering_widget)
        
        self.add_widget(image_container)
    
    def _create_prompt_display(self):
        """Create the prompt text display."""
        self.prompt_label = Label(
            text="Select form options to generate a portrait...",
            font_size=14,
            color=COLOR_TEXT,
            text_size=(None, None),
            halign='center',
            valign='middle',
            size_hint=(1, 0.2)  # Take 20% of panel height
        )
        
        # Enable text wrapping
        self.prompt_label.bind(size=self._update_prompt_text_size)
        
        self.add_widget(self.prompt_label)
    
    def _create_status_display(self):
        """Create the status indicator."""
        self.status_label = Label(
            text="Ready",
            font_size=12,
            color=COLOR_PRIMARY,
            size_hint=(1, 0.1)  # Take 10% of panel height
        )
        
        self.add_widget(self.status_label)
    
    def _update_prompt_text_size(self, instance, size):
        """Update prompt text wrapping based on widget size."""
        instance.text_size = (size[0] - 20, None)  # Leave some margin
    
    def _on_image_change(self, image_data):
        """Handle image state changes."""
        try:
            self._update_image(image_data)
            # Don't manually override status - let the generation status observer handle it
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating image")
    
    def _on_prompt_change(self, prompt):
        """Handle prompt state changes."""
        try:
            self._update_prompt_text(prompt)
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating prompt text")
    
    def _on_generation_status_change(self, is_generating):
        """Handle generation status changes."""
        try:
            self._update_status(is_generating)
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating status")
    
    def _on_state_change(self, field_name, new_value):
        """Handle application state changes (legacy method - kept for compatibility)."""
        try:
            if field_name == 'current_image':
                self._update_image(new_value)
            elif field_name == 'current_prompt':
                self._update_prompt_text(new_value)
            elif field_name == 'generating_image':
                self._update_status(new_value)
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating image panel")
    
    def _update_image(self, image_data):
        """Update the displayed image."""
        try:
            logger.info(f"Image panel: Updating image with data: {type(image_data)}")
            if image_data:
                logger.info(f"Image panel: Image data size: {len(image_data) if isinstance(image_data, bytes) else 'N/A'}")
                
                # Convert image data to displayable format
                if isinstance(image_data, bytes):
                    # Create a temporary file-like object
                    image_stream = BytesIO(image_data)
                    
                    # Load image from stream
                    # Note: Kivy requires a file path, so we'll save temporarily
                    import tempfile
                    import os
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                        temp_file.write(image_data)
                        temp_path = temp_file.name
                    
                    # Also save a copy for debugging (don't delete this one)
                    import shutil
                    debug_path = "/tmp/debug_image.png"
                    shutil.copy2(temp_path, debug_path)
                    logger.info(f"Image panel: Debug copy saved to: {debug_path}")
                    
                    # Use the debug path instead of temp path to avoid cleanup issues
                    self.image_widget.source = debug_path
                    
                    # Force reload of the image
                    self.image_widget.reload()
                    
                    # Force canvas redraw
                    self.image_widget.canvas.ask_update()
                    
                    logger.info(f"Image panel: Image widget source set to: {debug_path}")
                    
                    # Also log widget properties for debugging
                    logger.info(f"Image widget properties: size={self.image_widget.size}, pos={self.image_widget.pos}, source={self.image_widget.source}")
                    
                    # Check if the debug file exists and has content
                    import os
                    if os.path.exists(debug_path):
                        file_size = os.path.getsize(debug_path)
                        logger.info(f"Image panel: Debug file exists, size: {file_size} bytes")
                    else:
                        logger.error(f"Image panel: Debug file does not exist: {debug_path}")
                        return
                    
                    # Add a small delay and check if image loaded
                    def check_image_loaded(dt):
                        if hasattr(self.image_widget, 'texture') and self.image_widget.texture:
                            logger.info(f"Image panel: Image loaded successfully, texture size: {self.image_widget.texture.size}")
                        else:
                            logger.warning("Image panel: Image may not have loaded properly - no texture")
                            # Try to reload one more time
                            self.image_widget.reload()
                    
                    Clock.schedule_once(check_image_loaded, 0.5)
                    
                    logger.info(f"Image panel: Image widget source set to: {self.image_widget.source}")
                    
                    # Schedule cleanup of temp file after a longer delay to ensure display
                    Clock.schedule_once(
                        lambda dt: self._cleanup_temp_file(temp_path), 
                        10.0  # Wait 10 seconds before cleanup
                    )
                    
                elif isinstance(image_data, str):
                    # Assume it's a file path
                    self.image_widget.source = image_data
                
                logger.info("Image updated successfully")
            else:
                # Reset to placeholder
                self.image_widget.source = PLACEHOLDER_IMAGE
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating image")
            self.image_widget.source = PLACEHOLDER_IMAGE
    
    def _cleanup_temp_file(self, file_path):
        """Clean up temporary image file."""
        try:
            import os
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.warning(f"Could not clean up temp file {file_path}: {e}")
    
    def _update_prompt_text(self, prompt):
        """Update the displayed prompt text."""
        try:
            if prompt:
                self.prompt_label.text = f"Prompt: {prompt}"
            else:
                self.prompt_label.text = "Select form options to generate a portrait..."
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating prompt text")
    
    def _update_status(self, is_generating):
        """Update the status indicator."""
        try:
            if is_generating:
                self.status_label.text = "Generating..."
                self.status_label.color = COLOR_PRIMARY
                
                # Add a simple animation for generating status
                self._start_generating_animation()
            else:
                self.status_label.text = "Ready"
                self.status_label.color = COLOR_TEXT
                self._stop_generating_animation()
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating status")
    
    def _start_generating_animation(self):
        """Start animation for generating status."""
        try:
            # Simple text animation
            self.animation_dots = 0
            self.animation_event = Clock.schedule_interval(
                self._animate_generating_text, 
                0.5
            )
        except Exception as e:
            logger.warning(f"Error starting animation: {e}")
    
    def _stop_generating_animation(self):
        """Stop the generating animation."""
        try:
            if hasattr(self, 'animation_event'):
                self.animation_event.cancel()
        except Exception as e:
            logger.warning(f"Error stopping animation: {e}")
    
    def _animate_generating_text(self, dt):
        """Animate the generating text."""
        try:
            self.animation_dots = (self.animation_dots + 1) % 4
            dots = "." * self.animation_dots
            self.status_label.text = f"Generating{dots}"
        except Exception as e:
            logger.warning(f"Error in generating animation: {e}")
