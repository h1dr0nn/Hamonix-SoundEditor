"""Exceptions related to audio processing failures."""

from .base import HarmonixError

class ProcessingError(HarmonixError):
    """Base class for processing errors."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="PROCESSING_ERROR", details=details)


class ConversionError(ProcessingError):
    """Raised when audio conversion fails."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, details=details)
        self.code = "CONVERSION_FAILED"


class FFmpegError(ProcessingError):
    """Raised when FFmpeg subprocess fails."""
    def __init__(self, message: str, return_code: int = None, stderr: str = None):
        details = {}
        if return_code is not None:
            details["return_code"] = return_code
        if stderr:
            details["stderr"] = stderr
        super().__init__(message, details=details)
        self.code = "FFMPEG_ERROR"


class TimeoutError(ProcessingError):
    """Raised when processing times out."""
    def __init__(self, message: str = "Operation timed out", limit_seconds: int = None):
        details = {}
        if limit_seconds:
            details["limit_seconds"] = limit_seconds
        super().__init__(message, details=details)
        self.code = "TIMEOUT_ERROR"
