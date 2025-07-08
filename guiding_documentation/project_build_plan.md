# Project Design and Build Plan: "Not You" Art Installation

## Project Overview

"Not You" is an interactive art installation that explores the limitations of demographic forms and inherent biases in AI-generated images. Running on a Raspberry Pi 5 with a touchscreen interface, visitors interact with a simple demographics form. As they make selections, the system automatically generates a photographic-style portrait using a Stable Diffusion API, visualizing how AI interprets and represents different demographic combinations.

The name "Not You" emphasizes that no demographic form can fully capture the complexity of human identity, and the generated images inevitably reflect algorithmic biases rather than authentic representation.

## System Architecture

### Hardware Components
- Raspberry Pi 5
- 1024 x 600 pixel touchscreen in landscape orientation
- Power supply and optional network connectivity
- Appropriate enclosure for kiosk presentation

### Development Environment
- Development should be conducted on larger displays with the application window sized to exactly 1024x600 pixels
- This ensures pixel-perfect development matching the target touchscreen resolution
- UI elements must be designed and tested at this exact resolution to guarantee proper display on the installation hardware

### Software Architecture
- Python 3.11.2 application
- Kivy framework for touchscreen UI
- RESTful API client for Stable Diffusion image generation
- Local file storage for configuration and generated images
- Watchdog process for system stability in a public kiosk environment

## Component Breakdown

### 1. Core Application
- Main application loop
- Kiosk mode management
- Error handling and recovery
- Logging system

### 2. User Interface Components
- Demographics form panel (right side)
- Image display panel (left side)
- Touch-friendly form elements (dropdowns, buttons, etc.)
- Visual feedback elements

### 3. API Integration Layer
- Authentication handler (username:password for AUTOMATIC1111)
- Request formatting and queue management
- Response processing (base64 image decoding)
- Error handling and retries
- Request cancellation for rapid form changes

### 4. Configuration System
- User interface settings
- API connection parameters
- Prompt engineering configurations
- Form field mappings to prompt text

### 5. Monitoring & Maintenance
- Automated restart mechanism
- Log rotation
- Health checks

## User Interface Design

### Layout
- **Left Panel (40-45% of width)**: Displays the generated portrait image (512x512 pixels)
- **Right Panel (55-60% of width)**: Demographics form with categorical selections
- Clean, minimalistic design with high contrast for public use
- Large, easily tappable form elements
- Clear visual indication of current selections

### User Flow
1. User approaches kiosk displaying a placeholder image and form with all fields unselected (showing "?" values)
2. As soon as the user selects ANY first form field value, image generation is triggered automatically
3. Any subsequent change to any field value will trigger a new image generation (3-4 second process)
4. If user makes rapid form changes, each new change moves to the front of the queue; any previously-queued unfulfilled image generations are abandoned
5. Updated image appears with the prompt text used to generate it
6. User can continue modifying selections to see different results
7. No field is required - images will generate based on any combination of selected values

### Form Elements
- All interactions via touch selection (no keyboard input)
- Dropdown menus, radio buttons, or slider controls depending on field type
- Large touch targets suitable for public kiosk use
- Visual feedback on selection (highlighting, animation)

## Data Flow

1. **User Input**: Demographics form selections (any combination of fields, none required)
2. **Queue Management**: New selections cancel any pending incomplete image generation requests
3. **Mapping Layer**: Converts selections to appropriate prompt text based on configuration
4. **Prompt Construction**: Assembles prompt with prepended/appended text and formatting
5. **API Request**: Sends constructed prompt to AUTOMATIC1111 Stable Diffusion API with username:password authentication
6. **Image Processing**: Receives and processes generated image (base64 decoded)
7. **Display Update**: Shows new image and updates associated information

## Technical Implementation Plan

### Phase 1: Setup and Foundation
- Setup Raspberry Pi with required OS and dependencies
- Install Python 3.11.2 and Kivy framework
- Create project structure and configuration files
- Implement basic application shell with error handling

### Phase 2: UI Development
- Create main application window sized to exactly 1024x600 pixels for development consistency
- Configure kiosk mode for full-screen deployment
- Design and implement form elements optimized for 1024x600 resolution
- Implement image display panel with proper scaling for target resolution
- Create visual feedback elements sized appropriately for touchscreen interaction
- Test all UI elements at target resolution to ensure proper display on installation hardware

### Phase 3: API Integration
- Implement AUTOMATIC1111 authentication mechanism (username:password)
- Create prompt construction utilities
- Develop API client with queue management and request cancellation
- Implement base64 image decoding and processing
- Test integration with mock responses

### Phase 4: Core Logic
- Implement form-to-prompt mapping for specific demographic categories
- Create real-time image generation workflow with queue management
- Develop state management system for form selections
- Implement configuration loading/saving
- Add request cancellation logic for rapid form changes

### Phase 5: Optimization and Refinement
- Optimize for performance on Raspberry Pi
- Implement caching strategies if needed
- Fine-tune UI responsiveness
- Enhance error recovery mechanisms

### Phase 6: Testing and Hardening
- Perform comprehensive testing
- Implement automatic restart mechanisms
- Create system monitoring tools
- Conduct user testing and refinement

## File Structure

```
/notyou/
├── main.py                  # Application entry point
├── config.py                # Non-sensitive configuration
├── secrets.py               # API keys and sensitive data
├── requirements.txt         # Python dependencies
├── assets/
│   ├── ui_elements/         # UI images and assets
│   │   └── unknown_portrait.png  # Default placeholder image
│   └── fonts/               # Custom fonts if needed
├── logs/                    # Application logs
├── src/
│   ├── ui/                  # UI components
│   │   ├── __init__.py
│   │   ├── main_screen.py   # Main application screen
│   │   ├── form_panel.py    # Demographics form panel
│   │   └── image_panel.py   # Image display panel
│   ├── api/                 # API integration
│   │   ├── __init__.py
│   │   ├── client.py        # AUTOMATIC1111 API client implementation
│   │   ├── queue_manager.py # Request queue and cancellation management
│   │   └── prompt_builder.py  # Prompt construction utilities
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── error_handling.py  # Error handling utilities
│   │   └── logging.py       # Logging configuration
│   └── data/                # Data management
│       ├── __init__.py
│       ├── form_mapping.py  # Form to prompt mapping
│       └── state.py         # Application state management
└── scripts/                 # Maintenance and setup scripts
    ├── install.sh           # Installation script
    └── start_kiosk.sh       # Kiosk mode startup script
```

## Demographics Form Design

The demographics form will include the following categories with specific values designed to explore traditional demographic biases:

1. **Age**: Child, Teen, Young Adult, Middle-Aged, Senior
2. **Gender**: Male, Female  
3. **Ethnicity**: White, Asian, American Indian, Black or African American, Hispanic Latino or Spanish origin, Middle Eastern or North African, Native Hawaiian or Other Pacific Islander, Other
4. **Education**: Some schooling, high school, college, graduate / professional degree
5. **Employment status**: Unemployed, student, part-time, full-time, retired
6. **Income**: $0–$24,999, $25,000–$49,999, $50,000–$99,999, $100,000–$199,999, $200,000+

**Important Notes:**
- Each field will have an empty/unselected/unset value choice (displayed as "?")
- No field is required - images will generate based on any combination of selected values
- Each category will map to appropriate descriptors for image generation prompts, potentially with varying weights or modifiers

## Real-Time Image Generation System

### Responsive Queue Management
- **Immediate Trigger**: Image generation starts as soon as any first form field is selected
- **Real-time Updates**: Every form field change triggers new image generation
- **Queue Priority**: New requests immediately cancel any pending incomplete requests
- **No Required Fields**: Images generate from any combination of selected demographic values
- **Rapid Response**: System handles quick successive form changes by abandoning queued requests

### Request Lifecycle
1. User selects/changes any form field
2. System cancels any pending incomplete image generation request
3. New request is queued and sent to AUTOMATIC1111 API immediately
4. Base64 image response is decoded and displayed
5. Process repeats for any subsequent form changes

## API Integration

### AUTOMATIC1111 Stable Diffusion API Integration
- Authentication using username:password format (stored in secrets.py)
- Request structure: `requests.post(url=f'{URL}/sdapi/v1/txt2img', json=payload, auth=('username', 'password'))`
- Base64 image response handling and decoding
- Queue management to cancel pending requests on new form changes
- Handling rate limiting and quota constraints
- Implementing retry logic for failed requests

### Prompt Engineering
- Template system for consistent prompt structure
- Mapping form selections to effective prompt language
- Configuration for prepended/appended text and negative prompts
- Support for syntax modifiers (parentheses for emphasis, brackets for de-emphasis)
- Dynamic prompt construction based on any combination of selected demographic values

## Configuration and Security

### File Organization
- **config.py**: Non-sensitive configuration settings (API URLs, image parameters, prompt templates)
- **secrets.py**: Sensitive authentication data (AUTOMATIC1111 username:password)
- **secrets.py** is included in .gitignore to prevent credentials from being committed to the public repository

### AUTOMATIC1111 Setup
- The stable diffusion service must be launched with: `--api-auth username:password`
- Authentication credentials are stored in secrets.py and loaded at runtime
- API endpoint: `/sdapi/v1/txt2img`

## Testing Strategy

1. **Unit Testing**: Core functions and utility modules
2. **Integration Testing**: API client and form mapping
3. **UI Testing**: Touchscreen interaction and visual elements
4. **System Testing**: Full application flow on target hardware
5. **Stress Testing**: Performance under continuous use
6. **User Testing**: Observation of real users interacting with the installation

## Deployment Process

1. **Hardware Setup**: Prepare Raspberry Pi with appropriate OS
2. **Software Installation**: Install dependencies and application code
3. **Configuration**: Set up API keys and system settings
4. **Kiosk Setup**: Configure auto-start in kiosk mode
5. **Physical Installation**: Mount hardware in display area
6. **Monitoring Setup**: Configure remote monitoring if applicable

## Error Handling and Recovery

- Implement comprehensive error logging
- Create automatic application restart mechanism
- Design user-friendly error messages
- Implement watchdog timer to detect and recover from hangs
- Create fallback images for API failure scenarios

## Maintenance Considerations

- Log rotation to prevent storage issues
- Regular health checks
- Remote monitoring capabilities if possible
- Documentation for installation staff

## Conclusion

The "Not You" art installation creates an engaging and thought-provoking experience for visitors while highlighting the limitations of demographic categorization and algorithmic representation. This technical implementation plan provides a roadmap for creating a stable, responsive, and visually appealing installation that invites interaction and reflection.
