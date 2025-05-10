"""Prompt utilities for the Magic Shell."""

import os
import traceback
from utils.colors import COLORS as colors

def get_prompt() -> str:
    """
    Generate a customized shell prompt.
    
    Returns:
        str: Formatted prompt string with colorized elements showing:
             - username@hostname in green
             - current directory name in yellow
             - appropriate prompt terminator
    """
    try:
        # Get system information
        username = os.getlogin()
        hostname = os.uname().nodename
        
        # Get path information
        current_path = os.getcwd()
        current_folder = os.path.basename(current_path)
        
        # Format the prompt with colors
        prompt = (
            f"{colors['green']}{username}@{hostname}{colors['end']} "
            f"{colors['yellow']}{current_folder}{colors['end']}> "
        )
        
        return prompt
    except Exception as e:
        # Fallback prompt if something goes wrong
        traceback.print_exc()
        return "> "