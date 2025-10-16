"""Prompt utilities for the Magic Shell."""

import os
import traceback
from prompt_toolkit.formatted_text import HTML
from .colors import COLORS as colors

def get_prompt() -> str:
    """
    Generate a customized shell prompt (legacy function for compatibility).
    
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

def get_prompt_text(wizard_mode: bool = False) -> HTML:
    """
    Generate a customized prompt for prompt_toolkit.
    
    Args:
        wizard_mode: Whether the shell is in wizard mode
        
    Returns:
        HTML: Formatted prompt with HTML markup for colors
    """
    try:
        # Get system information
        username = os.getlogin()
        hostname = os.uname().nodename
        
        # Get path information
        current_path = os.getcwd()
        current_folder = os.path.basename(current_path)
        
        # Choose prompt symbol and style based on mode
        if wizard_mode:
            symbol = "🧙‍♂️✨"
            mode_color = "purple"
        else:
            symbol = ">"
            mode_color = "green"
        
        # Format the prompt with HTML markup for colors
        prompt = HTML(
            f'<green>{username}@{hostname}</green> '
            f'<yellow>{current_folder}</yellow>'
            f'<{mode_color}>{symbol}</> '
        )
        
        return prompt
    except Exception:
        # Fallback prompt if something goes wrong
        return HTML('<b>></b> ')