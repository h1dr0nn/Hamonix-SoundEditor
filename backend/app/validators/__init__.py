"""Audio and parameter validation for the Harmonix SE backend.

This package provides comprehensive validation utilities for audio files,
processing parameters, and format specifications. It ensures data integrity
before processing begins and provides clear error messages for invalid inputs.

Modules:
    audio_validator: Validates audio files and their properties
    parameter_validator: Validates processing parameters
    format_validator: Validates audio formats and specifications
    
Example:
    ```python
    from app.validators import validate_audio_file, validate_conversion_params
    
    # Validate input file
    is_valid, error = validate_audio_file("input.mp3")
    if not is_valid:
        print(f"Invalid audio file: {error}")
        
    # Validate parameters
    params = {"format": "mp3", "bitrate": "320k"}
    is_valid, error = validate_conversion_params(params)
    ```
"""

from .audio_validator import (
    validate_audio_file,
    check_file_format,
    verify_file_size,
    validate_path,
)
from .parameter_validator import (
    validate_conversion_params,
    validate_mastering_params,
    validate_trim_params,
    validate_modify_params,
)
from .format_validator import (
    is_valid_format,
    get_supported_formats,
    validate_sample_rate,
    validate_bitrate,
)

__all__ = [
    # Audio validation
    "validate_audio_file",
    "check_file_format",
    "verify_file_size",
    "validate_path",
    # Parameter validation
    "validate_conversion_params",
    "validate_mastering_params",
    "validate_trim_params",
    "validate_modify_params",
    # Format validation
    "is_valid_format",
    "get_supported_formats",
    "validate_sample_rate",
    "validate_bitrate",
]
