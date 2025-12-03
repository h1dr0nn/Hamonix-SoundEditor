"""Base exception class for the application."""

class HarmonixError(Exception):
    """Base class for all Harmonix SE exceptions.
    
    Attributes:
        message: Human-readable error message.
        code: Machine-readable error code.
        details: Optional dictionary with debug details.
    """
    
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}
        
    def to_dict(self) -> dict:
        """Convert exception to dictionary for JSON response."""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details
        }
