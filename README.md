# Not You - Interactive Art Installation

"Not You" is an interactive art installation that explores the limitations of demographic forms and inherent biases in AI-generated images. Visitors interact with a demographics form, and the system generates photographic-style portraits using Stable Diffusion API based on their selections.

The name "Not You" emphasizes that no demographic form can fully capture the complexity of human identity, and the generated images inevitably reflect algorithmic biases rather than authentic representation.

## Features

- **Interactive Demographics Form**: Touch-friendly interface with categories like age, gender, ethnicity, education, employment, and income
- **Real-time Image Generation**: AI-generated portraits update automatically as users modify form selections
- **Queue Management**: New selections cancel pending requests for responsive interaction
- **Kiosk Mode**: Full-screen operation optimized for public installations
- **Error Recovery**: Robust error handling and automatic restart mechanisms

## Hardware Requirements

- Raspberry Pi 5 (or compatible Linux system)
- 1024 x 600 pixel touchscreen (landscape orientation)
- Network connectivity for API access
- Sufficient storage for logs and temporary files

## Software Requirements

- Python 3.11.2 or compatible
- AUTOMATIC1111 Stable Diffusion WebUI with API enabled
- Kivy framework for UI
- Internet connection for API requests

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gregm123456/notyou.git
   cd notyou
   ```

2. **Run the installation script:**
   ```bash
   ./scripts/install.sh
   ```

3. **Configure API credentials:**
   Edit `secrets.py` and update the AUTOMATIC1111 API credentials:
   ```python
   API_USERNAME = "your_username"
   API_PASSWORD = "your_password"
   API_BASE_URL = "http://your-api-server:7860"
   ```

4. **Start AUTOMATIC1111 with API authentication:**
   ```bash
   # On your Stable Diffusion server
   ./webui.sh --api --api-auth username:password
   ```

## Usage

### Development Mode
For development and testing on a regular computer:
```bash
source venv/bin/activate
python main.py
```

### Kiosk Mode
For production deployment on a kiosk or Raspberry Pi:
```bash
./scripts/start_kiosk.sh
```

## Configuration

### Display Settings
- `WINDOW_WIDTH`, `WINDOW_HEIGHT`: Application window size (1024x600 for target hardware)
- `FULLSCREEN`: Enable fullscreen mode for kiosk deployment

### API Settings
- `API_TIMEOUT`: Request timeout in seconds
- `MAX_RETRIES`: Number of retry attempts for failed requests
- `DEFAULT_STEPS`, `DEFAULT_CFG_SCALE`: Stable Diffusion generation parameters

### Demographics Form
The form includes six categories designed to explore traditional demographic biases:
- Age: Child, Teen, Young Adult, Middle-Aged, Senior
- Gender: Male, Female
- Ethnicity: Multiple options including various ethnic backgrounds
- Education: From basic schooling to graduate degrees
- Employment: Student, part-time, full-time, unemployed, retired
- Income: Five income brackets from $0-$24,999 to $200,000+

## Project Structure

```
/notyou/
├── main.py                  # Application entry point
├── config.py                # Non-sensitive configuration
├── secrets.py               # API keys and sensitive data
├── requirements.txt         # Python dependencies
├── assets/
│   ├── ui_elements/         # UI images and assets
│   └── fonts/               # Custom fonts if needed
├── logs/                    # Application logs
├── src/
│   ├── ui/                  # UI components
│   │   ├── main_screen.py   # Main application screen
│   │   ├── form_panel.py    # Demographics form panel
│   │   └── image_panel.py   # Image display panel
│   ├── api/                 # API integration
│   │   ├── client.py        # AUTOMATIC1111 API client
│   │   └── prompt_builder.py # Prompt construction utilities
│   ├── utils/               # Utility functions
│   │   ├── error_handling.py # Error handling utilities
│   │   └── logging.py       # Logging configuration
│   └── data/                # Data management
│       ├── form_mapping.py  # Form to prompt mapping
│       └── state.py         # Application state management
└── scripts/                 # Maintenance and setup scripts
    ├── install.sh           # Installation script
    └── start_kiosk.sh       # Kiosk mode startup script
```

## User Interaction Flow

1. **Initial State**: User sees placeholder image and form with all fields showing "?"
2. **First Selection**: As soon as any form field is selected, image generation begins
3. **Real-time Updates**: Each form change triggers new image generation
4. **Queue Management**: New requests cancel any pending incomplete generations
5. **Visual Feedback**: Loading indicators and prompt text show current state

## API Integration

The application integrates with AUTOMATIC1111 Stable Diffusion WebUI:
- **Authentication**: Username/password authentication
- **Request Format**: JSON payloads to `/sdapi/v1/txt2img` endpoint
- **Image Processing**: Base64 decoding of generated images
- **Error Handling**: Automatic retries and graceful failure recovery

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Verify AUTOMATIC1111 is running with `--api-auth` flag
   - Check network connectivity and firewall settings
   - Confirm credentials in `secrets.py` are correct

2. **Application Won't Start**
   - Ensure Python 3.11.2 is installed
   - Check that virtual environment was created: `./scripts/install.sh`
   - Verify all dependencies are installed: `pip list`

3. **Touch Interface Issues**
   - Confirm display resolution is set to 1024x600
   - Check touchscreen drivers and calibration
   - Test with mouse/keyboard input first

4. **Image Generation Slow**
   - Check API server performance and load
   - Adjust `DEFAULT_STEPS` and other generation parameters
   - Monitor network latency to API server

### Log Files

- Application logs: `logs/notyou.log`
- Kiosk startup logs: `logs/kiosk_startup.log`
- System logs: Check with `journalctl` on Linux systems
