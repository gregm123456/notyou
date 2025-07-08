"""
Configuration settings for the Not You art installation.
Non-sensitive configuration only - secrets go in secrets.py
"""

# Display Settings
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600
FULLSCREEN = False  # Set to True for kiosk mode

# Image Display Settings
IMAGE_SIZE = 512  # Display size for generated images
IMAGE_PANEL_WIDTH_RATIO = 0.45  # Left panel takes 45% of width
FORM_PANEL_WIDTH_RATIO = 0.55   # Right panel takes 55% of width

# API Settings
API_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
REQUEST_DELAY = 0.5  # seconds between retries

# Image Generation Settings
DEFAULT_STEPS = 5
DEFAULT_CFG_SCALE = 2
DEFAULT_SAMPLER = "Euler a"
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
DEFAULT_SEED = 888  # -1 for random seed, or specific integer for reproducible results

# Current seed that can be modified at runtime
CURRENT_SEED = DEFAULT_SEED

# Prompt Templates
PROMPT_PREFIX = "professional portrait photograph of a"
PROMPT_SUFFIX = "person, high quality, detailed, realistic, photographic style"
NEGATIVE_PROMPT = "cartoon, anime, drawing, painting, sketch, low quality, blurry, distorted"

# Demographics Form Configuration
DEMOGRAPHICS_FIELDS = {
    "age": {
        "label": "Age",
        "options": ["?", "Child", "Teen", "Young Adult", "Middle-Aged", "Senior"],
        "prompt_mapping": {
            "Child": "child",
            "Teen": "teenager",
            "Young Adult": "young adult",
            "Middle-Aged": "middle-aged",
            "Senior": "elderly"
        }
    },
    "gender": {
        "label": "Gender",
        "options": ["?", "Male", "Female"],
        "prompt_mapping": {
            "Male": "male",
            "Female": "female"
        }
    },
    "ethnicity": {
        "label": "Ethnicity",
        "options": ["?", "White", "Asian", "American Indian", "Black or African American", 
                   "Hispanic Latino or Spanish origin", "Middle Eastern or North African", 
                   "Native Hawaiian or Other Pacific Islander", "Other"],
        "prompt_mapping": {
            "White": "caucasian",
            "Asian": "asian",
            "American Indian": "native american",
            "Black or African American": "african american",
            "Hispanic Latino or Spanish origin": "hispanic",
            "Middle Eastern or North African": "middle eastern",
            "Native Hawaiian or Other Pacific Islander": "pacific islander",
            "Other": "mixed ethnicity"
        }
    },
    "education": {
        "label": "Education",
        "options": ["?", "Some schooling", "High school", "College", "Graduate / professional degree"],
        "prompt_mapping": {
            "Some schooling": "with basic education",
            "High school": "with high school education",
            "College": "college educated",
            "Graduate / professional degree": "highly educated professional"
        }
    },
    "employment": {
        "label": "Employment",
        "options": ["?", "Unemployed", "Student", "Part-time", "Full-time", "Retired"],
        "prompt_mapping": {
            "Unemployed": "unemployed",
            "Student": "student",
            "Part-time": "part-time worker",
            "Full-time": "professional worker",
            "Retired": "retired"
        }
    },
    "income": {
        "label": "Income",
        "options": ["?", "$0–$24,999", "$25,000–$49,999", "$50,000–$99,999", 
                   "$100,000–$199,999", "$200,000+"],
        "prompt_mapping": {
            "$0–$24,999": "low income",
            "$25,000–$49,999": "modest income",
            "$50,000–$99,999": "middle class",
            "$100,000–$199,999": "upper middle class",
            "$200,000+": "wealthy"
        }
    }
}

# UI Settings
FONT_SIZE_LARGE = 18
FONT_SIZE_MEDIUM = 14
FONT_SIZE_SMALL = 12

BUTTON_HEIGHT = 35  # Much smaller for compact layout
BUTTON_WIDTH_TOUCH = 200  # Smaller width
DROPDOWN_HEIGHT = 35  # Much smaller dropdown height
SPACING = 4  # Much tighter spacing
PADDING = 8  # Less padding

# Colors (RGBA) - Improved contrast and modern styling
COLOR_PRIMARY = (0.1, 0.4, 0.7, 1.0)      # Darker blue for better contrast
COLOR_SECONDARY = (0.95, 0.95, 0.95, 1.0) # Very light gray for unselected
COLOR_BACKGROUND = (1.0, 1.0, 1.0, 1.0)   # White
COLOR_TEXT = (0.2, 0.2, 0.2, 1.0)         # Dark gray for good readability
COLOR_TEXT_LIGHT = (0.9, 0.9, 0.9, 1.0)   # Light text for dark backgrounds
COLOR_ACCENT = (0.8, 0.4, 0.2, 1.0)       # Orange
COLOR_SELECTED = (0.2, 0.7, 0.3, 1.0)     # Green for selected items
COLOR_UNSELECTED = (0.8, 0.8, 0.8, 1.0)   # Gray for unselected items

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "logs/notyou.log"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Paths
ASSETS_PATH = "assets"
UI_ELEMENTS_PATH = "assets/ui_elements"
FONTS_PATH = "assets/fonts"
PLACEHOLDER_IMAGE = "assets/ui_elements/unknown_portrait.png"

# Image Archive Settings
GENERATED_IMAGES_PATH = "generated_images"  # Local directory for generated images
MAX_ARCHIVED_IMAGES = 100  # Maximum number of images to keep in archive
