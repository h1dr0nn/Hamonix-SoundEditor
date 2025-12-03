"""Application settings classes.

This module defines configuration classes for different aspects of the application.
Using classes allows for type safety and easy grouping of related settings.
"""

from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class AudioSettings:
    """Settings related to audio processing."""
    
    # Default format if none specified
    DEFAULT_FORMAT: str = "mp3"
    
    # Default bitrate for compressed formats
    DEFAULT_BITRATE: str = "192k"
    
    # Default sample rate in Hz
    DEFAULT_SAMPLE_RATE: int = 44100
    
    # Maximum allowed file size in MB
    MAX_FILE_SIZE_MB: int = 2000
    
    # Supported input formats (extensions)
    SUPPORTED_INPUTS: List[str] = field(default_factory=lambda: [
        ".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".wma", ".aiff", ".alac"
    ])
    
    # Supported output formats (extensions without dot)
    SUPPORTED_OUTPUTS: List[str] = field(default_factory=lambda: [
        "mp3", "wav", "aac", "m4a", "flac", "ogg", "wma", "aiff"
    ])


@dataclass
class ProcessingSettings:
    """Settings related to the processing engine."""
    
    # Maximum concurrent files to process
    MAX_CONCURRENT_FILES: int = 4
    
    # Timeout for a single file processing in seconds
    TIMEOUT_SECONDS: int = 600
    
    # Buffer size for stream reading in bytes
    BUFFER_SIZE: int = 4096
    
    # Whether to overwrite existing files by default
    OVERWRITE_EXISTING: bool = False
    
    # Temp directory name
    TEMP_DIR_NAME: str = "harmonix_temp"


@dataclass
class AppSettings:
    """Global application settings."""
    
    APP_NAME: str = "Harmonix SE"
    VERSION: str = "1.0.3"
    DEBUG_MODE: bool = False
    
    audio: AudioSettings = field(default_factory=AudioSettings)
    processing: ProcessingSettings = field(default_factory=ProcessingSettings)
