"""Exceptions related to input validation."""

from .base import HarmonixError

class ValidationError(HarmonixError):
    """Base class for validation errors."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="VALIDATION_ERROR", details=details)


class AudioValidationError(ValidationError):
    """Raised when audio file validation fails."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, details=details)
        self.code = "INVALID_AUDIO_FILE"


class ParameterError(ValidationError):
    """Raised when processing parameters are invalid."""
    def __init__(self, message: str, param_name: str = None, details: dict = None):
        details = details or {}
        if param_name:
            details["parameter"] = param_name
        super().__init__(message, details=details)
        self.code = "INVALID_PARAMETER"


class FormatError(ValidationError):
    """Raised when format specifications are invalid."""
    def __init__(self, message: str, format_name: str = None, details: dict = None):
        details = details or {}
        if format_name:
            details["format"] = format_name
        super().__init__(message, details=details)
        self.code = "INVALID_FORMAT"
