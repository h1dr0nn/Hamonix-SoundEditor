"""General utility helpers.

This package provides common utility functions for audio math, file operations,
and string manipulation.
"""

from .audio_utils import db_to_float, float_to_db, ms_to_samples
from .file_utils import safe_delete, get_file_info, list_audio_files
from .string_utils import random_string, slugify, format_duration

__all__ = [
    "db_to_float",
    "float_to_db",
    "ms_to_samples",
    "safe_delete",
    "get_file_info",
    "list_audio_files",
    "random_string",
    "slugify",
    "format_duration",
]
