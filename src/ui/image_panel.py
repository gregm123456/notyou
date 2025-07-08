"""
Image panel for displaying generated portraits in the Not You installation.

This panel shows the AI-generated portrait image on the left side of the screen,
along with the prompt text used to generate it and status indicators.
"""

import logging
import time
from io import BytesIO
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock

from config import (
    IMAGE_SIZE, PLACEHOLDER_IMAGE, COLOR_BACKGROUND, COLOR_TEXT,
    COLOR_PRIMARY, COLOR_ACCENT, PADDING, SPACING, GENERATED_IMAGES_PATH, MAX_ARCHIVED_IMAGES,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, BUTTON_HEIGHT
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
        self.has_generated_image = False  # Track if first image has been generated
        self.tap_times = []  # For 5-tap exit gesture
        
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
            
            # Create bottom section with status and remix button
            self._create_bottom_section()
            
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
            size_hint=(1, 1),  # Use full container size
            fit_mode="contain"  # Modern way to fit image within bounds while keeping aspect ratio
        )
        # Bind to touch events for exit gesture detection
        self.image_widget.bind(on_touch_down=self._on_image_touch)
        
        image_container.add_widget(self.image_widget)
        
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
    
    def _create_bottom_section(self):
        """Create the bottom section with status and remix button."""
        # Bottom container for status and button
        bottom_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),  # Take 10% of panel height
            spacing=SPACING
        )
        
        # Status label (left side, takes most space)
        self.status_label = Label(
            text="Ready",
            font_size=12,
            color=COLOR_PRIMARY,
            size_hint=(0.6, 1),
            halign='left',
            valign='middle'
        )
        self.status_label.bind(size=lambda instance, size: setattr(instance, 'text_size', (size[0], None)))
        
        # Spacer to push remix button to the right
        spacer = Widget(size_hint=(0.2, 1))
        
        # Remix button (bottom left)
        self.remix_button = Button(
            text="Remix",
            font_size=FONT_SIZE_SMALL,
            size_hint=(0.2, 1),
            height=BUTTON_HEIGHT,
            background_color=COLOR_ACCENT,
            opacity=0  # Initially hidden
        )
        self.remix_button.bind(on_press=self._on_remix_pressed)
        
        # Add elements to bottom container
        bottom_container.add_widget(self.status_label)
        bottom_container.add_widget(spacer)
        bottom_container.add_widget(self.remix_button)
        
        self.add_widget(bottom_container)
    
    def _create_status_display(self):
        """Create the status indicator (legacy method for compatibility)."""
        # This method is kept for compatibility but functionality moved to _create_bottom_section
        pass
    
    def _update_prompt_text_size(self, instance, size):
        """Update prompt text wrapping based on widget size."""
        instance.text_size = (size[0] - 20, None)  # Leave some margin
    
    def _on_image_change(self, image_data):
        """Handle image state changes."""
        try:
            self._update_image(image_data)
            
            # Show remix button after first image is generated
            if image_data and not self.has_generated_image:
                self.has_generated_image = True
                self._show_remix_button()
                
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
            logger.info(f"Image panel: image_data is truthy: {bool(image_data)}")
            if image_data:
                logger.info(f"Image panel: Image data size: {len(image_data) if isinstance(image_data, bytes) else 'N/A'}")
                
                # Convert image data to displayable format
                if isinstance(image_data, bytes):
                    # Save to archive instead of temp file
                    import os
                    import datetime
                    
                    # Create archive directory if it doesn't exist
                    archive_dir = "generated_images"
                    os.makedirs(archive_dir, exist_ok=True)
                    
                    # Create filename with timestamp
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Include milliseconds
                    archive_path = os.path.join(archive_dir, f"portrait_{timestamp}.png")
                    
                    # Save image to archive
                    with open(archive_path, 'wb') as f:
                        f.write(image_data)
                    
                    logger.info(f"Image panel: Image saved to archive: {archive_path}")
                    
                    # Check if the archive file exists and has content
                    if os.path.exists(archive_path):
                        file_size = os.path.getsize(archive_path)
                        logger.info(f"Image panel: Archive file exists, size: {file_size} bytes")
                        
                        # Quick check if it's a valid PNG file
                        try:
                            with open(archive_path, 'rb') as f:
                                header = f.read(8)
                                if header.startswith(b'\x89PNG\r\n\x1a\n'):
                                    logger.info("Image panel: File has valid PNG header")
                                else:
                                    logger.error(f"Image panel: Invalid PNG header: {header}")
                        except Exception as header_check_error:
                            logger.error(f"Image panel: Error checking PNG header: {header_check_error}")
                    else:
                        logger.error(f"Image panel: Archive file was not created: {archive_path}")
                        return
                    
                    # Update image source to use archive file (use absolute path)
                    absolute_archive_path = os.path.abspath(archive_path)
                    logger.info(f"Image panel: Setting image source to: {absolute_archive_path}")
                    
                    # Schedule image update on main thread
                    def update_image_source(dt):
                        logger.info(f"Image panel: Actually setting source to: {absolute_archive_path}")
                        self.image_widget.source = absolute_archive_path
                        self.image_widget.nocache = True  # Prevent caching issues
                        logger.info(f"Image panel: Source set, widget.source = {self.image_widget.source}")
                        # Force reload and canvas update
                        self.image_widget.reload()
                        self.image_widget.canvas.ask_update()
                    
                    Clock.schedule_once(update_image_source, 0)
                    
                    # Add a small delay and check if image loaded
                    def check_image_loaded(dt):
                        if hasattr(self.image_widget, 'texture') and self.image_widget.texture:
                            logger.info(f"Image panel: Image loaded successfully, texture size: {self.image_widget.texture.size}")
                        else:
                            logger.warning("Image panel: Image may not have loaded properly - no texture")
                            # Try to reload one more time
                            self.image_widget.reload()
                    
                    Clock.schedule_once(check_image_loaded, 0.5)
                    
                    logger.info("Image updated successfully")
            else:
                # Reset to placeholder
                logger.info("Image panel: No image data provided, resetting to placeholder")
                self.image_widget.source = PLACEHOLDER_IMAGE
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating image")
            logger.error(f"Image panel: Exception in _update_image: {e}")
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
    
    def _show_remix_button(self):
        """Show the remix button with animation."""
        try:
            def fade_in(dt):
                if self.remix_button.opacity < 1.0:
                    self.remix_button.opacity = min(1.0, self.remix_button.opacity + 0.1)
                    Clock.schedule_once(fade_in, 0.02)
            
            Clock.schedule_once(fade_in, 0.1)
            logger.info("Remix button shown")
            
        except Exception as e:
            self.error_handler.handle_error(e, "Error showing remix button")
    
    def _on_remix_pressed(self, instance):
        """Handle remix button press."""
        try:
            logger.info("Remix button pressed")
            
            # Generate new random seed
            new_seed = self.app_state.generate_new_random_seed()
            logger.info(f"Generated new seed: {new_seed}")
            
            # Get current prompt and trigger regeneration
            current_prompt = self.app_state.get_current_prompt()
            if current_prompt:
                logger.info(f"Regenerating image with new seed and prompt: {current_prompt}")
                self._trigger_image_regeneration(current_prompt)
            else:
                logger.warning("No current prompt available for remix")
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error handling remix button press")
    
    def _trigger_image_regeneration(self, prompt):
        """Trigger image regeneration with current prompt but new seed."""
        try:
            # Import here to avoid circular imports
            from src.api.client import APIClient
            
            # Create a new API client instance or get existing one
            # For simplicity, we'll trigger through the main screen's method
            # by setting the prompt again which should trigger regeneration
            
            # Set generating state
            self.app_state.set_generating_image(True)
            
            # Get parent (main screen) and trigger regeneration
            parent = self.parent
            while parent and not hasattr(parent, '_trigger_image_generation'):
                parent = parent.parent
            
            if parent and hasattr(parent, '_trigger_image_generation'):
                # Use Clock to ensure this runs on main thread
                Clock.schedule_once(lambda dt: parent._trigger_image_generation(), 0.1)
            else:
                logger.error("Could not find main screen to trigger regeneration")
                self.app_state.set_generating_image(False)
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error triggering image regeneration")
            self.app_state.set_generating_image(False)
    
    def _on_image_touch(self, instance, touch):
        """Handle touch events on the image for exit pattern detection."""
        if instance.collide_point(*touch.pos):
            current_time = time.time()
            self.tap_times.append(current_time)
            # Keep only the 5 most recent taps
            if len(self.tap_times) > 5:
                self.tap_times.pop(0)
            # Check if we have 5 taps and they all occurred within 5 seconds
            if len(self.tap_times) == 5 and (current_time - self.tap_times[0] <= 5.0):
                logger.info("Exit pattern detected: 5 taps within 5 seconds")
                self._exit_fullscreen()
                self.tap_times = []
            return True  # Indicate that the touch was handled
        return False
    
    def _exit_fullscreen(self):
        """Exit the application for troubleshooting."""
        logger.info("Exit pattern detected - preparing to exit application")
        
        # Show confirmation message and exit when touched
        def show_exit_message(dt):
            from kivy.uix.label import Label
            from kivy.uix.popup import Popup
            from kivy.app import App
            
            content = Label(text='Touch anywhere to exit application')
            popup = Popup(
                title='Exiting Application',
                content=content,
                size_hint=(0.6, 0.3),
                auto_dismiss=False
            )
            
            # Exit the app when the popup is touched
            def on_popup_touch(instance, touch):
                if popup.content.collide_point(*touch.pos):
                    logger.info("User confirmed exit - stopping application")
                    popup.dismiss()
                    # Schedule app exit on next frame
                    Clock.schedule_once(lambda dt: App.get_running_app().stop(), 0.1)
                    return True
                return False
            
            popup.content.bind(on_touch_down=on_popup_touch)
            popup.open()
        
        Clock.schedule_once(show_exit_message, 0.5)
