"""Custom exception hierarchy for Harmonix SE backend.

This package defines all custom exceptions used throughout the application
to handle errors in a structured and predictable way.
"""

from .base import HarmonixError
from .validation_errors import (
    ValidationError,
    AudioValidationError,
    ParameterError,
    FormatError
)
from .processing_errors import (
    ProcessingError,
    ConversionError,
    FFmpegError,
    TimeoutError
)
from .file_errors import (
    FileError,
    FileAccessError,
    FileNotFoundError,
    FileTooLargeError
)

__all__ = [
    "HarmonixError",
    "ValidationError",
    "AudioValidationError",
    "ParameterError",
    "FormatError",
    "ProcessingError",
    "ConversionError",
    "FFmpegError",
    "TimeoutError",
    "FileError",
    "FileAccessError",
    "FileNotFoundError",
    "FileTooLargeError",
]
