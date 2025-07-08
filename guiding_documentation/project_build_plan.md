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
- Authentication handler
- Request formatting
- Response processing
- Error handling and retries

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
1. User approaches kiosk displaying a placeholder image and form with default values
2. User changes any demographic selection using touch interface
3. System automatically generates a new image based on selections (3-4 second process)
4. Updated image appears with the prompt text used to generate it
5. User can continue modifying selections to see different results

### Form Elements
- All interactions via touch selection (no keyboard input)
- Dropdown menus, radio buttons, or slider controls depending on field type
- Large touch targets suitable for public kiosk use
- Visual feedback on selection (highlighting, animation)

## Data Flow

1. **User Input**: Demographics form selections
2. **Mapping Layer**: Converts selections to appropriate prompt text based on configuration
3. **Prompt Construction**: Assembles prompt with prepended/appended text and formatting
4. **API Request**: Sends constructed prompt to Stable Diffusion API with authentication
5. **Image Processing**: Receives and processes generated image
6. **Display Update**: Shows new image and updates associated information

## Technical Implementation Plan

### Phase 1: Setup and Foundation
- Setup Raspberry Pi with required OS and dependencies
- Install Python 3.11.2 and Kivy framework
- Create project structure and configuration files
- Implement basic application shell with error handling

### Phase 2: UI Development
- Create main application window and kiosk mode
- Design and implement form elements
- Implement image display panel
- Create visual feedback elements

### Phase 3: API Integration
- Implement authentication mechanism
- Create prompt construction utilities
- Develop API client with error handling and retries
- Test integration with mock responses

### Phase 4: Core Logic
- Implement form-to-prompt mapping
- Create image generation workflow
- Develop state management system
- Implement configuration loading/saving

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
│   │   ├── client.py        # API client implementation
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

The demographics form will include the following categories (subject to refinement):

1. **Age Range**: Child, Teen, Young Adult, Middle-Aged, Senior
2. **Gender Identity**: Various options covering a spectrum
3. **Ethnicity/Race**: Multiple selections reflecting diverse backgrounds
4. **Occupation/Role**: Categories of work or social roles
5. **Style/Appearance**: Various aesthetic presentations

Each category will map to appropriate descriptors for image generation prompts, potentially with varying weights or modifiers.

## API Integration

### Stable Diffusion API Integration
- Authentication using API keys stored in secrets.py
- Request formatting following API documentation
- Handling rate limiting and quota constraints
- Implementing retry logic for failed requests

### Prompt Engineering
- Template system for consistent prompt structure
- Mapping form selections to effective prompt language
- Configuration for prepended/appended text
- Support for syntax modifiers (parentheses for emphasis, brackets for de-emphasis)

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
