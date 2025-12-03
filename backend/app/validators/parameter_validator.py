"""Processing parameter validation utilities.

This module validates the configuration dictionaries passed to various
processing handlers (converter, mastering, trimmer, modifier).
"""

from typing import Dict, Any, Tuple, Optional
from .format_validator import is_valid_format, validate_bitrate, validate_sample_rate


def validate_conversion_params(params: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate parameters for audio conversion.

    Args:
        params: Dictionary containing conversion settings.
                Expected keys: format, bitrate (optional), sample_rate (optional).

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if valid.
    """
    if not params:
        return False, "Parameters cannot be empty"

    # Validate Format
    fmt = params.get("format")
    if not fmt:
        return False, "Missing required parameter: format"
    
    if not is_valid_format(fmt):
        return False, f"Unsupported output format: {fmt}"

    # Validate Bitrate (if present)
    if "bitrate" in params:
        valid, error = validate_bitrate(params["bitrate"])
        if not valid:
            return False, error

    # Validate Sample Rate (if present)
    if "sample_rate" in params:
        valid, error = validate_sample_rate(params["sample_rate"])
        if not valid:
            return False, error

    return True, None


def validate_mastering_params(params: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate parameters for audio mastering.

    Args:
        params: Dictionary containing mastering settings.
                Expected keys: preset, target_lufs (optional).

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if valid.
    """
    if not params:
        return False, "Parameters cannot be empty"

    preset = params.get("preset")
    valid_presets = ["music", "podcast", "voiceover", "custom"]
    
    if preset and preset not in valid_presets:
        return False, f"Invalid preset: {preset}. Valid: {valid_presets}"

    # Validate Target LUFS
    if "target_lufs" in params:
        try:
            lufs = float(params["target_lufs"])
            if not (-50 <= lufs <= 0):
                return False, "Target LUFS must be between -50 and 0"
        except (ValueError, TypeError):
            return False, "Target LUFS must be a number"

    return True, None


def validate_trim_params(params: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate parameters for silence trimming.

    Args:
        params: Dictionary containing trim settings.
                Expected keys: threshold, min_silence_len, padding.

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if valid.
    """
    if not params:
        return False, "Parameters cannot be empty"

    # Threshold (dB)
    if "threshold" in params:
        try:
            thresh = float(params["threshold"])
            if thresh > 0:
                return False, "Silence threshold must be negative (dB)"
        except (ValueError, TypeError):
            return False, "Threshold must be a number"

    # Min Silence Length (ms)
    if "min_silence_len" in params:
        try:
            length = int(params["min_silence_len"])
            if length < 0:
                return False, "Minimum silence length must be positive"
        except (ValueError, TypeError):
            return False, "Minimum silence length must be an integer"

    return True, None


def validate_modify_params(params: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate parameters for audio modification.

    Args:
        params: Dictionary containing modification settings.
                Expected keys: speed, pitch, volume.

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if valid.
    """
    if not params:
        return False, "Parameters cannot be empty"

    # Speed (0.5x to 4.0x)
    if "speed" in params:
        try:
            speed = float(params["speed"])
            if not (0.1 <= speed <= 10.0):
                return False, "Speed must be between 0.1 and 10.0"
        except (ValueError, TypeError):
            return False, "Speed must be a number"

    # Pitch (semitones)
    if "pitch" in params:
        try:
            float(params["pitch"])
        except (ValueError, TypeError):
            return False, "Pitch must be a number"

    return True, None
