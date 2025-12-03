"""Audio format validation utilities.

This module validates technical audio specifications including sample rates,
bitrates, and container formats.
"""

from typing import Tuple, Optional, List

# Constants
VALID_SAMPLE_RATES = [
    8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000
]

VALID_BITRATES = [
    "32k", "64k", "96k", "128k", "160k", "192k", "256k", "320k"
]

SUPPORTED_OUTPUT_FORMATS = [
    "mp3", "wav", "aac", "m4a", "flac", "ogg", "wma", "aiff"
]


def get_supported_formats() -> List[str]:
    """Get list of supported output formats.

    Returns:
        List[str]: List of format extensions.
    """
    return sorted(SUPPORTED_OUTPUT_FORMATS)


def is_valid_format(fmt: str) -> bool:
    """Check if a format string is supported.

    Args:
        fmt: Format string (e.g., 'mp3', 'wav').

    Returns:
        bool: True if supported.
    """
    return fmt.lower().strip('.') in SUPPORTED_OUTPUT_FORMATS


def validate_sample_rate(rate: int) -> Tuple[bool, Optional[str]]:
    """Validate audio sample rate.

    Args:
        rate: Sample rate in Hz.

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if valid.
    """
    if not isinstance(rate, int):
        return False, "Sample rate must be an integer"
        
    if rate not in VALID_SAMPLE_RATES:
        return False, f"Unsupported sample rate: {rate}. Valid: {VALID_SAMPLE_RATES}"
        
    return True, None


def validate_bitrate(bitrate: str) -> Tuple[bool, Optional[str]]:
    """Validate audio bitrate string.

    Args:
        bitrate: Bitrate string (e.g., '192k').

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if valid.
    """
    if not isinstance(bitrate, str):
        return False, "Bitrate must be a string"
        
    if bitrate not in VALID_BITRATES:
        # Also check if it's a raw number convertible to int
        try:
            val = int(bitrate.replace('k', ''))
            if 32 <= val <= 320:
                return True, None
        except ValueError:
            pass
        return False, f"Invalid bitrate: {bitrate}. Standard: {VALID_BITRATES}"
        
    return True, None
