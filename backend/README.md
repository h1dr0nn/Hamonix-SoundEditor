# Harmonix SE Backend

This is the Python-based audio processing backend for Harmonix SE. It handles all audio conversion, mastering, trimming, and analysis tasks.

## Architecture

The backend is structured as a modular Python application:

- **`app/handler/`**: Core logic for different operations (convert, master, trim, modify).
- **`app/validators/`**: Input validation for files, parameters, and formats.
- **`app/formatters/`**: Standardization of JSON responses and file paths.
- **`app/exceptions/`**: Custom exception hierarchy for robust error handling.
- **`app/config/`**: Centralized configuration and constants.
- **`app/utils/`**: Helper functions for audio math, file ops, etc.

## Key Modules

### Validators

Ensures all inputs are valid before processing starts.

- `audio_validator`: Checks file existence, format support, and size limits.
- `parameter_validator`: Validates processing parameters (bitrate, sample rate, etc.).

### Formatters

Standardizes communication with the Tauri frontend.

- `output_formatter`: Generates consistent JSON success/error/progress responses.

### Handlers

- `SoundConverter`: Direct FFmpeg conversion.
- `MasteringEngine`: Audio mastering chain (Compression -> Normalization -> Limiting).
- `SilenceTrimmer`: Silence detection and removal.
- `Modifier`: Speed, pitch, and cut operations.

## Development

### Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

### Adding a New Feature

1. Create a new handler in `app/handler/`.
2. Add validation logic in `app/validators/`.
3. Register the operation in `main.py`.
4. Add unit tests in `tests/`.

## Dependencies

- **FFmpeg**: Required for all audio processing.
- **pydub**: Used for high-level audio manipulation (mastering, trimming).
