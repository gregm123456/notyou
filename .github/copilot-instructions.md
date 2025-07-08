# Project context:

## This project is Python-based and creates a kiosk-style full-screen application for an art installation running on a Raspberry Pi.

## The application explores demographics and inherent biases in AI-generated images.

## The application will utilize a touchscreen interface on a small touchscreen. User input will evoke a very standarized demographics survey form, and display AI-generated photographic-style images based on the form values selected by the user.

## The name of this installation is `Not You`, since no demographics form can fully capture the complexity of human identity.

# Python styling guidelines:

    - use PEP 8 style guide for Python code

# Configuration settings:

    - use `config.py` for non-secret configuration settings
    - use `secrets.py` for secret configuration settings (e.g., API keys, passwords)

# Error handling:

    - use `try` and `except` blocks to handle exceptions
    - log errors using the `logging` module
    - provide user-friendly error messages in the UI
    - attempt to recover from errors gracefully and keep the public kiosk application running; restart if necessary

# UI style:

    - use a clean, modern, and minimalistic design; fun, approachable, stylish and artistic
    - ensure the UI is responsive and works well on a small touchscreen
    - use large buttons and clear labels for user interaction
    - provide visual feedback for user actions (e.g., button presses)
    - ensure the UI is accessible to users with different abilities

# Public github repo:

    - we use a public GitHub repository for the project: https://github.com/gregm123456/notyou
    - ensure the repository is well-organized and includes a clear README file

# Technologies:

    - use Python 3.x for the application; preferably Python 3.11.2 unless there is a compelling reason to use a different version.
    - use Kivy for the UI framework