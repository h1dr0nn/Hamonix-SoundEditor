"""Audio file validation utilities.

This module provides functions to validate audio files before processing.
It checks for file existence, supported formats, file size limits, and
path validity.
"""

import os
from pathlib import Path
from typing import Optional, Tuple, Union

# Constants
MAX_FILE_SIZE_MB_DEFAULT = 500
SUPPORTED_EXTENSIONS = {
    '.mp3', '.wav', '.aac', '.m4a', '.flac', '.ogg', '.wma', '.aiff', '.alac'
}


def validate_path(path_str: str) -> Tuple[bool, Optional[str]]:
    """Validate that a path string is well-formed and exists.

    Args:
        path_str: The file system path to validate.

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if valid, (False, error_message) if invalid.
    """
    if not path_str:
        return False, "Path cannot be empty"

    try:
        path = Path(path_str)
        if not path.exists():
            return False, f"Path does not exist: {path_str}"
        return True, None
    except Exception as e:
        return False, f"Invalid path format: {str(e)}"


def check_file_format(file_path: Union[str, Path]) -> Tuple[bool, Optional[str]]:
    """Check if the file has a supported audio extension.

    Args:
        file_path: Path to the audio file.

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if supported, (False, error_message) if not.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()
    
    if suffix not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported file format: {suffix}. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
    
    return True, None


def verify_file_size(file_path: Union[str, Path], max_size_mb: int = MAX_FILE_SIZE_MB_DEFAULT) -> Tuple[bool, Optional[str]]:
    """Verify that the file size is within the allowed limit.

    Args:
        file_path: Path to the file.
        max_size_mb: Maximum allowed size in Megabytes.

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if within limit, (False, error_message) if exceeded.
    """
    path = Path(file_path)
    try:
        size_bytes = path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        
        if size_mb > max_size_mb:
            return False, f"File size ({size_mb:.2f} MB) exceeds limit of {max_size_mb} MB"
        
        return True, None
    except OSError as e:
        return False, f"Could not read file size: {str(e)}"


def validate_audio_file(file_path: Union[str, Path]) -> Tuple[bool, Optional[str]]:
    """Comprehensive validation of an audio file.

    Performs all checks: existence, format, and size.

    Args:
        file_path: Path to the audio file.

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if all checks pass, (False, error_message) if any fail.
    """
    # 1. Validate path existence
    exists, error = validate_path(str(file_path))
    if not exists:
        return False, error

    # 2. Check format
    valid_format, error = check_file_format(file_path)
    if not valid_format:
        return False, error

    # 3. Check size
    valid_size, error = verify_file_size(file_path)
    if not valid_size:
        return False, error

    return True, None
