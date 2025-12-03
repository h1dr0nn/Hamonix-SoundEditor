"""Global constants for the application.

This module contains static constant definitions used across the backend.
"""

# Audio Formats
AUDIO_FORMATS = {
    "mp3": {"mime": "audio/mpeg", "ext": ".mp3", "lossy": True},
    "wav": {"mime": "audio/wav", "ext": ".wav", "lossy": False},
    "aac": {"mime": "audio/aac", "ext": ".aac", "lossy": True},
    "m4a": {"mime": "audio/mp4", "ext": ".m4a", "lossy": True},
    "flac": {"mime": "audio/flac", "ext": ".flac", "lossy": False},
    "ogg": {"mime": "audio/ogg", "ext": ".ogg", "lossy": True},
    "wma": {"mime": "audio/x-ms-wma", "ext": ".wma", "lossy": True},
    "aiff": {"mime": "audio/x-aiff", "ext": ".aiff", "lossy": False},
}

# Valid Sample Rates (Hz)
SAMPLE_RATES = [
    8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000
]

# Valid Bit Depths (bits)
BIT_DEPTHS = [8, 16, 24, 32]

# Mastering Presets
PRESETS = {
    "music": {
        "target_lufs": -14.0,
        "true_peak": -1.0,
        "compression": True,
        "eq_profile": "balanced"
    },
    "podcast": {
        "target_lufs": -16.0,
        "true_peak": -1.0,
        "compression": True,
        "eq_profile": "vocal_boost"
    },
    "voiceover": {
        "target_lufs": -18.0,
        "true_peak": -1.0,
        "compression": True,
        "eq_profile": "clarity"
    }
}

# Process Exit Codes
EXIT_CODES = {
    "SUCCESS": 0,
    "GENERAL_ERROR": 1,
    "INVALID_ARGS": 2,
    "FILE_NOT_FOUND": 3,
    "PERMISSION_DENIED": 4,
    "TIMEOUT": 5,
    "DEPENDENCY_MISSING": 6
}
