"""Response and path formatting utilities.

This package provides standardized formatting for API responses (JSON output)
and file system paths. It ensures consistency in how the backend communicates
with the frontend and how files are named.

Modules:
    output_formatter: Formats JSON responses for stdout
    path_formatter: Handles file naming and path sanitization
"""

from .output_formatter import (
    format_success,
    format_error,
    format_progress,
    format_analysis_result
)
from .path_formatter import (
    sanitize_filename,
    generate_output_path,
    ensure_unique_path
)

__all__ = [
    "format_success",
    "format_error",
    "format_progress",
    "format_analysis_result",
    "sanitize_filename",
    "generate_output_path",
    "ensure_unique_path",
]
