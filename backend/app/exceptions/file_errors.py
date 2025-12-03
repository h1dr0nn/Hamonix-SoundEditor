"""Exceptions related to file system operations."""

from .base import HarmonixError

class FileError(HarmonixError):
    """Base class for file system errors."""
    def __init__(self, message: str, path: str = None, details: dict = None):
        details = details or {}
        if path:
            details["path"] = path
        super().__init__(message, code="FILE_ERROR", details=details)


class FileAccessError(FileError):
    """Raised when file cannot be accessed (permissions, lock)."""
    def __init__(self, message: str, path: str = None):
        super().__init__(message, path=path)
        self.code = "FILE_ACCESS_DENIED"


class FileNotFoundError(FileError):
    """Raised when file does not exist."""
    def __init__(self, message: str, path: str = None):
        super().__init__(message, path=path)
        self.code = "FILE_NOT_FOUND"


class FileTooLargeError(FileError):
    """Raised when file exceeds size limit."""
    def __init__(self, message: str, size_mb: float = None, limit_mb: float = None, path: str = None):
        details = {}
        if size_mb:
            details["size_mb"] = size_mb
        if limit_mb:
            details["limit_mb"] = limit_mb
        super().__init__(message, path=path, details=details)
        self.code = "FILE_TOO_LARGE"
