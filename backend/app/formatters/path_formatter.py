"""File path formatting and generation utilities.

This module handles file naming conventions, path sanitization, and
output path generation logic.
"""

import os
import re
from pathlib import Path
from typing import Optional


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters.

    Args:
        filename: Original filename.

    Returns:
        Sanitized filename safe for file systems.
    """
    # Remove null bytes
    filename = filename.replace('\0', '')
    
    # Replace invalid characters with underscore
    # Windows invalid: < > : " / \ | ? *
    # Unix: /
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing periods and spaces
    filename = filename.strip('. ')
    
    # Ensure it's not empty
    if not filename:
        filename = "unnamed_file"
        
    return filename


def ensure_unique_path(base_path: Path) -> Path:
    """Ensure a path is unique by appending a counter if it exists.

    Example: file.mp3 -> file_1.mp3 -> file_2.mp3

    Args:
        base_path: Desired path.

    Returns:
        Unique Path object.
    """
    if not base_path.exists():
        return base_path

    stem = base_path.stem
    suffix = base_path.suffix
    parent = base_path.parent
    counter = 1

    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def generate_output_path(
    input_path: str,
    output_dir: str,
    output_format: Optional[str] = None,
    suffix: str = ""
) -> str:
    """Generate a full output path based on input and settings.

    Args:
        input_path: Path to the source file.
        output_dir: Directory to save the output.
        output_format: Desired output extension (e.g., 'mp3'). If None, keeps original.
        suffix: Optional suffix to append to filename (e.g., '_mastered').

    Returns:
        String representation of the absolute output path.
    """
    input_p = Path(input_path)
    output_d = Path(output_dir)
    
    # Determine extension
    ext = f".{output_format.lstrip('.')}" if output_format else input_p.suffix
    
    # Construct filename
    new_filename = f"{input_p.stem}{suffix}{ext}"
    sanitized_name = sanitize_filename(new_filename)
    
    # Combine
    full_path = output_d / sanitized_name
    
    # Ensure uniqueness
    unique_path = ensure_unique_path(full_path)
    
    return str(unique_path.absolute())
