"""
Form field to prompt mapping for the Not You installation.
"""

import logging
from typing import Dict, List, Optional
from config import DEMOGRAPHICS_FIELDS, PROMPT_PREFIX, PROMPT_SUFFIX


logger = logging.getLogger(__name__)


class FormToPromptMapper:
    """Maps form selections to AI prompt text."""
    
    def __init__(self):
        """Initialize the mapper with configuration data."""
        self.fields = DEMOGRAPHICS_FIELDS
        self.prefix = PROMPT_PREFIX
        self.suffix = PROMPT_SUFFIX
        
    def get_field_options(self, field_name: str) -> List[str]:
        """
        Get the available options for a specific form field.
        
        Args:
            field_name: Name of the form field
            
        Returns:
            List of available options
        """
        if field_name not in self.fields:
            logger.warning(f"Unknown field: {field_name}")
            return []
        
        return self.fields[field_name]["options"]
    
    def get_field_label(self, field_name: str) -> str:
        """
        Get the display label for a form field.
        
        Args:
            field_name: Name of the form field
            
        Returns:
            Display label for the field
        """
        if field_name not in self.fields:
            logger.warning(f"Unknown field: {field_name}")
            return field_name.title()
        
        return self.fields[field_name]["label"]
    
    def map_selection_to_prompt(self, field_name: str, selection: str) -> Optional[str]:
        """
        Map a form selection to prompt text.
        
        Args:
            field_name: Name of the form field
            selection: Selected value
            
        Returns:
            Mapped prompt text or None if invalid selection
        """
        if field_name not in self.fields:
            logger.warning(f"Unknown field: {field_name}")
            return None
        
        if selection == "?" or selection is None:
            return None
        
        prompt_mapping = self.fields[field_name].get("prompt_mapping", {})
        mapped_text = prompt_mapping.get(selection)
        
        if mapped_text is None:
            logger.warning(f"No mapping found for {field_name}: {selection}")
            return selection.lower()
        
        return mapped_text
    
    def build_prompt(self, form_data: Dict[str, str]) -> str:
        """
        Build a complete prompt from form data.
        
        Args:
            form_data: Dictionary of field_name -> selected_value
            
        Returns:
            Complete prompt string
        """
        prompt_parts = []
        
        # Add prefix
        if self.prefix:
            prompt_parts.append(self.prefix)
        
        # Process each field in a specific order for better prompt flow
        field_order = ["age", "gender", "ethnicity", "education", "employment", "income"]
        
        descriptors = []
        for field_name in field_order:
            if field_name in form_data:
                selection = form_data[field_name]
                mapped_text = self.map_selection_to_prompt(field_name, selection)
                if mapped_text:
                    descriptors.append(mapped_text)
        
        # Handle any additional fields not in the standard order
        for field_name, selection in form_data.items():
            if field_name not in field_order:
                mapped_text = self.map_selection_to_prompt(field_name, selection)
                if mapped_text:
                    descriptors.append(mapped_text)
        
        # Join descriptors
        if descriptors:
            prompt_parts.append(" ".join(descriptors))
        
        # Add suffix
        if self.suffix:
            prompt_parts.append(self.suffix)
        
        # If no descriptors were added, create a generic prompt
        if len(prompt_parts) <= 2:  # Only prefix and suffix
            prompt_parts.insert(-1 if self.suffix else len(prompt_parts), "person")
        
        full_prompt = " ".join(prompt_parts)
        logger.info(f"Generated prompt: {full_prompt}")
        return full_prompt
    
    def get_all_field_names(self) -> List[str]:
        """
        Get all available field names.
        
        Returns:
            List of field names
        """
        return list(self.fields.keys())
    
    def validate_selection(self, field_name: str, selection: str) -> bool:
        """
        Validate that a selection is valid for a given field.
        
        Args:
            field_name: Name of the form field
            selection: Selected value
            
        Returns:
            True if selection is valid
        """
        if field_name not in self.fields:
            return False
        
        return selection in self.fields[field_name]["options"]
