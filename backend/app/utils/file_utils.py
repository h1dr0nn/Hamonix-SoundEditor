"""File system utility functions.

Provides safe file operations and file info retrieval.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Union, Optional
from datetime import datetime

def safe_delete(path: Union[str, Path]) -> bool:
    """Safely delete a file or directory.

    Args:
        path: Path to delete.

    Returns:
        True if deleted or didn't exist, False if error.
    """
    p = Path(path)
    if not p.exists():
        return True
        
    try:
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        return True
    except OSError:
        return False


def get_file_info(path: Union[str, Path]) -> Optional[Dict[str, Union[str, int, float]]]:
    """Get detailed information about a file.

    Args:
        path: Path to file.

    Returns:
        Dictionary with size, created/modified times, extension.
    """
    p = Path(path)
    if not p.exists() or not p.is_file():
        return None
        
    stat = p.stat()
    return {
        "name": p.name,
        "extension": p.suffix,
        "size_bytes": stat.st_size,
        "size_mb": round(stat.st_size / (1024 * 1024), 2),
        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "absolute_path": str(p.absolute())
    }


def list_audio_files(directory: Union[str, Path], recursive: bool = False) -> List[Path]:
    """List all audio files in a directory.

    Args:
        directory: Directory to search.
        recursive: Whether to search subdirectories.

    Returns:
        List of Path objects.
    """
    p = Path(directory)
    if not p.exists() or not p.is_dir():
        return []
        
    extensions = {'.mp3', '.wav', '.aac', '.m4a', '.flac', '.ogg', '.wma', '.aiff'}
    pattern = "**/*" if recursive else "*"
    
    return [
        f for f in p.glob(pattern)
        if f.is_file() and f.suffix.lower() in extensions
    ]
