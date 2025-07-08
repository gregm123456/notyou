"""
Demographics form panel for the Not You art installation.

This panel contains the interactive form elements that allow users to select
demographic characteristics. Changes to form fields trigger image generation.
"""

import logging
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView

from config import (
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_TEXT, COLOR_BACKGROUND,
    COLOR_TEXT_LIGHT, COLOR_SELECTED, COLOR_UNSELECTED,
    PADDING, SPACING, BUTTON_HEIGHT, BUTTON_WIDTH_TOUCH,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
)
from src.data.form_mapping import FormToPromptMapper
from src.utils.error_handling import ErrorHandler


logger = logging.getLogger(__name__)


class FormPanel(BoxLayout):
    """Panel containing the demographics form."""
    
    def __init__(self, app_state, **kwargs):
        super().__init__(**kwargs)
        
        # Configure layout
        self.orientation = 'vertical'
        self.spacing = SPACING
        self.padding = PADDING
        
        # Store references
        self.app_state = app_state
        self.error_handler = ErrorHandler()
        self.form_mapper = FormToPromptMapper()
        
        # Track form widgets
        self.form_widgets = {}
        
        # Create UI
        self._create_ui()
        
        logger.info("Form panel initialized")
    
    def _create_ui(self):
        """Create the form panel UI elements."""
        try:
            # Create title
            title_label = Label(
                text="Demographics Form",
                font_size=FONT_SIZE_LARGE,
                color=COLOR_TEXT,
                size_hint=(1, None),
                height=35,  # Smaller title height
                halign='center',
                bold=True
            )
            title_label.bind(size=title_label.setter('text_size'))
            self.add_widget(title_label)
            
            # Create instruction text
            instruction_label = Label(
                text="Select any characteristics to generate a portrait.\nNo fields are required.",
                font_size=FONT_SIZE_SMALL,
                color=COLOR_TEXT,
                size_hint=(1, None),
                height=35,  # Smaller instruction height
                halign='center',
                text_size=(None, None)
            )
            instruction_label.bind(size=self._update_instruction_text_size)
            self.add_widget(instruction_label)
            
            # Create scrollable form area
            self._create_form_area()
            
        except Exception as e:
            self.error_handler.handle_error(e, "Failed to create form panel UI")
    
    def _update_instruction_text_size(self, instance, size):
        """Update instruction text wrapping."""
        instance.text_size = (size[0] - 20, None)
    
    def _update_button_text_size(self, instance, size):
        """Update button text wrapping for long option names."""
        instance.text_size = (size[0] - 20, None)  # Allow height to expand
        instance.halign = 'center'
        instance.valign = 'middle'
    
    def _create_form_area(self):
        """Create the scrollable form area with all form fields."""
        # Create scroll view for form fields
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=8,
            bar_color=COLOR_PRIMARY,
            bar_inactive_color=COLOR_SECONDARY
        )
        
        # Container for form fields
        form_container = BoxLayout(
            orientation='vertical',
            spacing=SPACING,
            size_hint_y=None,
            padding=(PADDING, 0)
        )
        form_container.bind(minimum_height=form_container.setter('height'))
        
        # Create form fields
        self._create_form_fields(form_container)
        
        scroll_view.add_widget(form_container)
        self.add_widget(scroll_view)
    
    def _create_form_fields(self, container):
        """Create all form field widgets."""
        try:
            field_names = self.form_mapper.get_all_field_names()
            
            for field_name in field_names:
                field_widget = self._create_form_field(field_name)
                container.add_widget(field_widget)
                
        except Exception as e:
            self.error_handler.handle_error(e, "Error creating form fields")
    
    def _create_form_field(self, field_name):
        """Create a single form field widget."""
        try:
            # Field container with adaptive height
            field_container = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                spacing=2  # Much tighter spacing
            )
            
            # Field label with better styling
            label_text = self.form_mapper.get_field_label(field_name)
            field_label = Label(
                text=label_text,
                font_size=FONT_SIZE_SMALL,
                color=COLOR_TEXT,
                size_hint=(1, None),
                height=20,  # Much smaller label height
                halign='left',
                valign='middle',
                bold=True
            )
            field_label.bind(size=field_label.setter('text_size'))
            field_container.add_widget(field_label)
            
            # Create dropdown for field options
            dropdown_button = self._create_dropdown_field(field_name)
            field_container.add_widget(dropdown_button)
            
            # Set compact container height
            field_container.height = 20 + BUTTON_HEIGHT + 4  # label + button + spacing
            
            return field_container
            
        except Exception as e:
            self.error_handler.handle_error(e, f"Error creating field {field_name}")
            return Label(text=f"Error creating {field_name}", color=(1, 0, 0, 1))
    
    def _create_dropdown_field(self, field_name):
        """Create a dropdown field for selecting options."""
        try:
            options = self.form_mapper.get_field_options(field_name)
            
            # Create main button with better styling
            dropdown_button = Button(
                text="?",  # Default unselected state
                size_hint=(1, None),
                height=BUTTON_HEIGHT,
                background_color=COLOR_UNSELECTED,
                color=COLOR_TEXT,
                font_size=FONT_SIZE_MEDIUM,
                bold=True,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            
            # Enable text wrapping for the main button
            dropdown_button.bind(size=self._update_button_text_size)
            
            # Create dropdown with improved styling
            dropdown = DropDown(
                max_height=300  # Limit dropdown height
            )
            
            # Add options to dropdown
            for option in options:
                # Determine styling for each option
                if option == "?":
                    bg_color = COLOR_UNSELECTED
                    text_color = COLOR_TEXT
                else:
                    bg_color = COLOR_PRIMARY
                    text_color = COLOR_TEXT_LIGHT
                
                # Calculate compact height based on text length for long options
                text_height = BUTTON_HEIGHT
                if len(option) > 30:  # Long text needs a bit more height
                    text_height = BUTTON_HEIGHT + 10
                elif len(option) > 45:  # Very long text needs more height
                    text_height = BUTTON_HEIGHT + 20
                
                option_button = Button(
                    text=option,
                    size_hint_y=None,
                    height=text_height,
                    background_color=bg_color,
                    color=text_color,
                    font_size=FONT_SIZE_SMALL,
                    halign='center',
                    valign='middle',
                    text_size=(None, None)
                )
                
                # Enable text wrapping for long options
                option_button.bind(size=self._update_button_text_size)
                
                # Bind option selection
                option_button.bind(
                    on_release=lambda btn, field=field_name, opt=option: 
                    self._on_option_selected(field, opt, dropdown_button, dropdown)
                )
                
                dropdown.add_widget(option_button)
            
            # Bind dropdown to main button
            dropdown_button.bind(on_release=dropdown.open)
            dropdown.bind(on_select=lambda instance, value: setattr(dropdown_button, 'text', value))
            
            # Store reference
            self.form_widgets[field_name] = {
                'button': dropdown_button,
                'dropdown': dropdown,
                'current_value': "?"
            }
            
            return dropdown_button
            
        except Exception as e:
            self.error_handler.handle_error(e, f"Error creating dropdown for {field_name}")
            return Button(text=f"Error: {field_name}", background_color=(1, 0, 0, 1))
    
    def _on_option_selected(self, field_name, option, button, dropdown):
        """Handle option selection in a form field."""
        try:
            logger.info(f"Option selected: {field_name} = {option}")
            
            # Update button text
            button.text = option
            
            # Update stored value
            if field_name in self.form_widgets:
                self.form_widgets[field_name]['current_value'] = option
            
            # Close dropdown
            dropdown.dismiss()
            
            # Update application state
            self._update_form_data()
            
            # Provide visual feedback
            self._provide_selection_feedback(button, option)
            
        except Exception as e:
            self.error_handler.handle_error(e, f"Error handling option selection for {field_name}")
    
    def _provide_selection_feedback(self, button, option):
        """Provide visual feedback for option selection."""
        try:
            # Change button color and text styling based on selection
            if option == "?":
                button.background_color = COLOR_UNSELECTED
                button.color = COLOR_TEXT
                button.height = BUTTON_HEIGHT
            else:
                button.background_color = COLOR_SELECTED
                button.color = COLOR_TEXT_LIGHT
                
                # Adjust button height for long text
                if len(option) > 25:
                    button.height = BUTTON_HEIGHT + 20
                elif len(option) > 40:
                    button.height = BUTTON_HEIGHT + 40
                else:
                    button.height = BUTTON_HEIGHT
                
            # Enable text wrapping for the main button
            button.bind(size=self._update_button_text_size)
            
        except Exception as e:
            logger.warning(f"Error providing selection feedback: {e}")
    
    def _update_form_data(self):
        """Update the application state with current form data."""
        try:
            # Collect current form data
            form_data = {}
            for field_name, widget_data in self.form_widgets.items():
                current_value = widget_data['current_value']
                if current_value != "?":
                    form_data[field_name] = current_value
            
            # Update application state
            self.app_state.set_form_data(form_data)
            
            # Generate and set new prompt
            prompt = self.form_mapper.build_prompt(form_data)
            self.app_state.set_current_prompt(prompt)
            
            logger.info(f"Form data updated: {form_data}")
            
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating form data")
    
    def get_current_selections(self):
        """Get current form selections."""
        try:
            selections = {}
            for field_name, widget_data in self.form_widgets.items():
                selections[field_name] = widget_data['current_value']
            return selections
        except Exception as e:
            self.error_handler.handle_error(e, "Error getting current selections")
            return {}
    
    def reset_form(self):
        """Reset all form fields to unselected state."""
        try:
            for field_name, widget_data in self.form_widgets.items():
                button = widget_data['button']
                button.text = "?"
                button.background_color = COLOR_UNSELECTED
                button.color = COLOR_TEXT
                widget_data['current_value'] = "?"
            
            # Update application state
            self.app_state.set_form_data({})
            self.app_state.set_current_prompt("")
            
            logger.info("Form reset to default state")
            
        except Exception as e:
            self.error_handler.handle_error(e, "Error resetting form")
