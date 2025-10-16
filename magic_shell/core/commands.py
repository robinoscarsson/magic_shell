"""Command handling for the Magic Shell."""

import os
from typing import Dict, Callable, Any

from .registry import command, registry
from ..utils.colors import COLORS as colors

CommandHandler = Callable[[str], None]


@command("help", "Display this help message", category="Basic")
def print_help(wizard_mode: bool = False):
    """Display help information using the command registry."""
    registry.print_help(wizard_mode)


@command("exit", "Exit the shell", aliases=["quit", ":quit"], category="Basic")  
def exit_shell(state: dict):
    """Exit the magic shell."""
    state.update({"running": False})
    print(f"{colors['green']}👋 Farewell, brave adventurer! May your terminals always be magical!{colors['end']}")


@command("wizard", "Enter wizard mode for magical command execution", category="Magic")
def enter_wizard_mode(state: dict):
    """Enter wizard mode with fanfare."""
    state.update({"wizard_mode": True})
    print(f"{colors['purple']}🧙‍♂️ Entering Wizard Mode... ✨{colors['end']}")
    print(f"{colors['cyan']}You can now cast magical spells! Use 'help' to see available magic.{colors['end']}")


@command("normal", "Exit wizard mode and return to normal shell", category="Magic") 
def exit_wizard_mode(state: dict):
    """Exit wizard mode."""
    state.update({"wizard_mode": False})
    print(f"{colors['green']}✨ Returning to normal mode... 🧙‍♂️{colors['end']}")


@command(":reload", "Reload shell configuration", category="System")
def reload_config():
    """Reload shell configuration."""
    print(f"{colors['blue']}🔄 Reloading configuration... (feature coming soon!){colors['end']}")


@command("cd", "Change directory", category="System")
def change_directory(path: str = "~"):
    """Change the current working directory."""
    try:
        expanded_path = os.path.expanduser(path)
        os.chdir(expanded_path)
        print(f"{colors['green']}📁 Changed directory to: {os.getcwd()}{colors['end']}")
    except FileNotFoundError:
        print(f"{colors['red']}cd: no such file or directory: {path}{colors['end']}")
    except PermissionError:
        print(f"{colors['red']}cd: permission denied: {path}{colors['end']}")
    except Exception as e:
        print(f"{colors['red']}cd: error: {e}{colors['end']}")

class CommandManager:
    """Manages command execution using the command registry."""
    
    def __init__(self, state: dict):
        """
        Initialize command manager.
        
        Args:
            state: Application state dictionary
        """
        self.state = state
        
        # Discover commands from spells package
        registry.discover_commands("magic_shell.spells")
        
    def handle_special_command(self, command: str) -> bool:
        """
        Handle commands using the registry system.
        
        Args:
            command: The command string to process
            
        Returns:
            bool: True if a command was handled, False otherwise
        """
        # Parse command and arguments
        parts = command.split()
        if not parts:
            return False
            
        cmd_name = parts[0].lower()
        args = parts[1:]
        
        # Check if command exists in registry
        cmd_info = registry.get_command(cmd_name)
        if not cmd_info:
            return False
        
        # Check wizard mode restrictions
        if cmd_info.wizard_only and not self.state["wizard_mode"]:
            print(f"{colors['red']}🧙‍♂️ The spell '{cmd_name}' can only be cast in wizard mode!{colors['end']}")
            return True
            
        # Execute the command with appropriate arguments
        try:
            # Get function signature to determine arguments
            import inspect
            sig = inspect.signature(cmd_info.func)
            params = list(sig.parameters.keys())
            
            if not params:
                # No parameters
                registry.execute_command(cmd_name)
            elif 'state' in params and 'wizard_mode' in params:
                # Help command that needs both
                registry.execute_command(cmd_name, wizard_mode=self.state["wizard_mode"])
            elif 'state' in params:
                # Commands that need state
                registry.execute_command(cmd_name, self.state)
            elif len(params) == 1 and args:
                # Commands with single argument (like cd)
                registry.execute_command(cmd_name, ' '.join(args))
            elif params and args:
                # Commands with multiple arguments
                registry.execute_command(cmd_name, *args)
            else:
                # No arguments or command doesn't need them
                registry.execute_command(cmd_name)
                
        except Exception as e:
            print(f"{colors['red']}Error executing command '{cmd_name}': {e}{colors['end']}")
            
        return True

    def execute_command(self, command: str) -> int:
        """
        Execute a system command safely.
        
        Args:
            command: The command to execute
            
        Returns:
            int: Command exit code
        """
        return os.system(command)