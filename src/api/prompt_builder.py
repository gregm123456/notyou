"""
Prompt builder utilities for the Not You installation.
"""

import logging
from typing import Dict, List, Optional
from config import (
    DEFAULT_STEPS, DEFAULT_CFG_SCALE, DEFAULT_SAMPLER,
    DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_SEED, NEGATIVE_PROMPT
)


logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builds API requests for image generation."""
    
    def __init__(self):
        """Initialize the prompt builder with default settings."""
        self.default_params = {
            "steps": DEFAULT_STEPS,
            "cfg_scale": DEFAULT_CFG_SCALE,
            "sampler_name": DEFAULT_SAMPLER,
            "width": DEFAULT_WIDTH,
            "height": DEFAULT_HEIGHT,
            "negative_prompt": NEGATIVE_PROMPT,
            "batch_size": 1,
            "n_iter": 1,
            "seed": DEFAULT_SEED,  # Configurable seed from config.py
            "restore_faces": True,
            "override_settings": {
                "sd_model_checkpoint": None  # Use current model
            }
        }
    
    def build_api_payload(self, prompt: str, seed: Optional[int] = None, **overrides) -> Dict:
        """
        Build the API payload for image generation.
        
        Args:
            prompt: Text prompt for image generation
            seed: Optional seed value (overrides default)
            **overrides: Parameter overrides
            
        Returns:
            Dictionary payload for the API request
        """
        payload = self.default_params.copy()
        payload["prompt"] = prompt
        
        # Override seed if provided
        if seed is not None:
            payload["seed"] = seed
        
        # Apply any parameter overrides
        for key, value in overrides.items():
            if key in payload:
                payload[key] = value
            else:
                logger.warning(f"Unknown parameter override: {key}")
        
        logger.info(f"Built API payload with prompt: {prompt}")
        logger.debug(f"Full payload: {payload}")
        
        return payload
    
    def enhance_prompt(self, base_prompt: str, enhancements: Optional[List[str]] = None) -> str:
        """
        Enhance a base prompt with additional descriptors.
        
        Args:
            base_prompt: Base prompt text
            enhancements: Additional descriptors to add
            
        Returns:
            Enhanced prompt string
        """
        if not enhancements:
            return base_prompt
        
        enhanced_parts = [base_prompt]
        enhanced_parts.extend(enhancements)
        
        enhanced_prompt = ", ".join(enhanced_parts)
        logger.debug(f"Enhanced prompt: {enhanced_prompt}")
        
        return enhanced_prompt
    
    def apply_emphasis(self, text: str, strength: float = 1.1) -> str:
        """
        Apply emphasis to text using parentheses notation.
        
        Args:
            text: Text to emphasize
            strength: Strength of emphasis (1.0 = normal, >1.0 = stronger)
            
        Returns:
            Text with emphasis notation
        """
        if strength == 1.0:
            return text
        elif strength > 1.0:
            # Use parentheses for emphasis
            emphasis_level = min(int((strength - 1.0) * 10), 3)  # Max 3 levels
            return "(" * emphasis_level + text + ")" * emphasis_level
        else:
            # Use brackets for de-emphasis
            de_emphasis_level = min(int((1.0 - strength) * 10), 3)  # Max 3 levels
            return "[" * de_emphasis_level + text + "]" * de_emphasis_level
    
    def build_quality_enhanced_prompt(self, base_prompt: str) -> str:
        """
        Add quality enhancing terms to a prompt.
        
        Args:
            base_prompt: Base prompt text
            
        Returns:
            Quality-enhanced prompt
        """
        quality_terms = [
            "high quality",
            "detailed",
            "professional photography",
            "studio lighting",
            "sharp focus",
            "8k resolution"
        ]
        
        return self.enhance_prompt(base_prompt, quality_terms)
    
    def validate_payload(self, payload: Dict) -> bool:
        """
        Validate that a payload contains required fields.
        
        Args:
            payload: API payload to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["prompt", "steps", "cfg_scale", "width", "height"]
        
        for field in required_fields:
            if field not in payload:
                logger.error(f"Missing required field in payload: {field}")
                return False
        
        # Validate numeric fields
        numeric_fields = {
            "steps": (1, 150),
            "cfg_scale": (1.0, 30.0),
            "width": (64, 2048),
            "height": (64, 2048)
        }
        
        for field, (min_val, max_val) in numeric_fields.items():
            value = payload.get(field)
            if not isinstance(value, (int, float)) or not (min_val <= value <= max_val):
                logger.error(f"Invalid value for {field}: {value} (expected {min_val}-{max_val})")
                return False
        
        return True
    
    def get_default_params(self) -> Dict:
        """
        Get a copy of the default parameters.
        
        Returns:
            Copy of default parameters dictionary
        """
        return self.default_params.copy()
