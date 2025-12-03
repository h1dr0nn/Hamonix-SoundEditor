"""String manipulation utility functions."""

import random
import string
import re
import unicodedata

def random_string(length: int = 8) -> str:
    """Generate a random alphanumeric string.

    Args:
        length: Length of string.

    Returns:
        Random string.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def slugify(text: str) -> str:
    """Convert text to a safe filename slug.

    Args:
        text: Input text.

    Returns:
        Slugified text (lowercase, no special chars).
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    
    # Remove invalid characters
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    
    # Replace spaces/underscores with hyphens
    text = re.sub(r'[-\s_]+', '-', text)
    
    return text


def format_duration(seconds: float) -> str:
    """Format seconds into HH:MM:SS string.

    Args:
        seconds: Duration in seconds.

    Returns:
        Formatted string.
    """
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"
