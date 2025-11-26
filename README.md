# Sound Converter App

A modern, lightweight desktop application for converting audio files, built with Python and PySide6.

## Features

- **Modern Interface**: Clean, minimalist design with drag-and-drop support.
- **Broad Format Support**: Convert between popular formats including MP3, WAV, OGG, FLAC, AAC, and WMA.
- **Batch Processing**: Add multiple files and convert them simultaneously.
- **Custom Output**: Easily select your destination folder.
- **High Performance**: Background processing ensures the interface remains smooth and responsive during conversion.

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.9** or higher.
- **FFmpeg**: This is required for audio processing.
  - You must install FFmpeg and add it to your system's `PATH`.
  - _Alternative_: You can place the `ffmpeg` executable directly in the `app/resources/bin/` directory.

## Installation

1.  **Clone the repository** (or download the source code):

    ```bash
    git clone https://github.com/your-username/SoundConverterApp.git
    cd SoundConverterApp
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the application, simply run:

```bash
python main.py
```

Once open, you can drag and drop your audio files into the window, select your desired output format, and click convert.

## Building from Source

If you wish to create a standalone executable (e.g., `.exe` for Windows), follow these steps:

1.  Install PyInstaller:

    ```bash
    pip install pyinstaller
    ```

2.  Build the application using the provided spec file:

    ```bash
    pyinstaller setup.spec
    ```

3.  The executable will be generated in the `dist/` folder.

> **Note**: For Linux/macOS builds, ensure the separator in the spec file or command matches your operating system (use `:` instead of `;` for path separators if running commands manually).
