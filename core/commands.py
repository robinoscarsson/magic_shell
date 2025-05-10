"""Command handling for the Magic Shell."""

import os
from typing import Dict, Callable, Any

CommandHandler = Callable[[str], None]

def print_help():
    """Display help information."""
    from utils.colors import COLORS as colors
    
    help_text = [
        f"{colors['green']}=== Magic Shell Help ==={colors['end']}",
        f"{colors['yellow']}exit, quit{colors['end']} - Exit the shell",
        f"{colors['yellow']}cd <path>{colors['end']} - Change directory",
        f"{colors['yellow']}history{colors['end']} - View command history",
        f"{colors['yellow']}!<number>{colors['end']} - Execute command from history",
        f"{colors['yellow']}wizard{colors['end']} - Enter wizard mode (magical command execution)",
        f"{colors['yellow']}normal{colors['end']} - Exit wizard mode",
        f"{colors['yellow']}help{colors['end']} - Display this help message",
    ]
    
    for line in help_text:
        print(line)

class CommandManager:
    """Manages command execution and special commands."""
    
    def __init__(self, state: dict):
        """
        Initialize command manager.
        
        Args:
            state: Application state dictionary
        """
        self.state = state
        self.handlers = {
            "exit": lambda _: self.state.update({"running": False}),
            "quit": lambda _: self.state.update({"running": False}),
            "wizard": lambda _: self.state.update({"wizard_mode": True}),
            "normal": lambda _: self.state.update({"wizard_mode": False}),
            "help": lambda _: print_help()
        }
        
    def handle_special_command(self, command: str) -> bool:
        """
        Handle special built-in commands.
        
        Args:
            command: The command string to process
            
        Returns:
            bool: True if a special command was handled, False otherwise
        """
        cmd_lower = command.lower()
        
        # Direct command matches
        if cmd_lower in self.handlers:
            self.handlers[cmd_lower](command)
            return True
            
        # CD command needs special handling
        if cmd_lower.startswith("cd "):
            self._handle_cd_command(command)
            return True
            
        return False
        
    def _handle_cd_command(self, command: str) -> None:
        """
        Handle the cd command to change directories.
        
        Args:
            command: The cd command with path
        """
        path = command[3:].strip()
        try:
            os.chdir(path)
        except FileNotFoundError:
            print(f"cd: no such file or directory: {path}")
        except PermissionError:
            print(f"cd: permission denied: {path}")
    
    def execute_command(self, command: str) -> int:
        """
        Execute a system command safely.
        
        Args:
            command: The command to execute
            
        Returns:
            int: Command exit code
        """
        return os.system(command)