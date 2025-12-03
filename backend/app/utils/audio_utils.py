"""Audio-related mathematical utilities.

Provides functions for converting between different audio units (dB, float, samples).
"""

import math
from typing import Union

def db_to_float(db: float) -> float:
    """Convert decibels to float amplitude.

    Args:
        db: Value in decibels.

    Returns:
        Float amplitude (0.0 to 1.0+).
    """
    return pow(10, db / 20)


def float_to_db(amplitude: float) -> float:
    """Convert float amplitude to decibels.

    Args:
        amplitude: Float amplitude.

    Returns:
        Value in decibels.
    """
    if amplitude <= 0:
        return -float('inf')
    return 20 * math.log10(amplitude)


def ms_to_samples(ms: int, sample_rate: int = 44100) -> int:
    """Convert milliseconds to number of samples.

    Args:
        ms: Duration in milliseconds.
        sample_rate: Sample rate in Hz.

    Returns:
        Number of samples.
    """
    return int((ms / 1000) * sample_rate)


def samples_to_ms(samples: int, sample_rate: int = 44100) -> float:
    """Convert number of samples to milliseconds.

    Args:
        samples: Number of samples.
        sample_rate: Sample rate in Hz.

    Returns:
        Duration in milliseconds.
    """
    return (samples / sample_rate) * 1000
