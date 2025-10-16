"""Color utilities for the Magic Shell."""

# ANSI color codes
COLORS = {
    'purple': '\033[95m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'cyan': '\033[96m',
    'end': '\033[0m'
}

def colorize(text: str, color: str) -> str:
    """
    Apply color to text.
    
    Args:
        text: The text to colorize
        color: The color name from COLORS dictionary
        
    Returns:
        str: Colorized text
    """
    if color not in COLORS:
        return text
    return f"{COLORS[color]}{text}{COLORS['end']}"