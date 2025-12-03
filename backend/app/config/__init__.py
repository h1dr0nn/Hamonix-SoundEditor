"""Application configuration and constants.

This package centralizes all configuration settings and constants used
throughout the backend application.
"""

from .settings import AudioSettings, ProcessingSettings, AppSettings
from .constants import (
    AUDIO_FORMATS,
    SAMPLE_RATES,
    BIT_DEPTHS,
    PRESETS,
    EXIT_CODES
)

__all__ = [
    "AudioSettings",
    "ProcessingSettings",
    "AppSettings",
    "AUDIO_FORMATS",
    "SAMPLE_RATES",
    "BIT_DEPTHS",
    "PRESETS",
    "EXIT_CODES",
]
