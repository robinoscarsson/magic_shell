"""Command handling for the Magic Shell."""

import os
from typing import Dict, Callable, Any

from .registry import command, registry
from .executor import safe_executor
from .config import config_manager
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
    config = config_manager.reload_config()
    # Update safe executor with new config
    safe_executor.config = {
        'allowed_commands': config.executor.allowed_commands,
        'default_timeout': config.executor.default_timeout,
        'max_output_size': config.executor.max_output_size,
        'additional_env_vars': config.executor.additional_env_vars,
        'working_directory': config.executor.working_directory
    }
    safe_executor.whitelist = set(config.executor.allowed_commands)


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


@command("config", "Show or edit configuration settings", category="System")
def show_config(*args):
    """Show configuration information or edit settings."""
    if not args:
        # Show current configuration
        config = config_manager.get_config()
        print(f"{colors['cyan']}=== 🔧 Magic Shell Configuration ==={colors['end']}")
        print(f"{colors['yellow']}Config file:{colors['end']} {config_manager.config_file}")
        print(f"{colors['yellow']}Version:{colors['end']} {config.version}")
        print()
        print(f"{colors['cyan']}Shell Settings:{colors['end']}")
        print(f"  Wizard mode on startup: {config.shell.wizard_mode_startup}")
        print(f"  Show welcome: {config.shell.show_welcome}")
        print(f"  History enabled: {config.shell.enable_history}")
        print(f"  History file: {config.shell.history_file}")
        print(f"  Auto-complete: {config.shell.auto_complete}")
        print()
        print(f"{colors['cyan']}Execution Settings:{colors['end']}")
        print(f"  Default timeout: {config.executor.default_timeout}s")
        print(f"  Max output size: {config.executor.max_output_size // 1024}KB")
        print(f"  Allowed commands: {len(config.executor.allowed_commands)} commands")
        print(f"  Working directory: {config.executor.working_directory}")
        
    elif args[0] == "edit":
        # Open config file in editor
        config_file = str(config_manager.config_file)
        editor = os.environ.get('EDITOR', 'nano')
        print(f"{colors['blue']}📝 Opening config in {editor}...{colors['end']}")
        safe_executor.execute_with_feedback(f"{editor} {config_file}")
        
    elif args[0] == "path":
        # Show config file path
        print(f"{colors['green']}Config file: {config_manager.config_file}{colors['end']}")


@command("allowed", "Show or manage allowed commands", category="System")
def manage_allowed_commands(*args):
    """Show or manage the allowed commands list."""
    if not args:
        # Show allowed commands
        allowed = safe_executor.list_allowed_commands()
        print(f"{colors['cyan']}=== 🛡️  Allowed Commands ({len(allowed)}) ==={colors['end']}")
        
        # Group commands for better display
        per_line = 6
        for i in range(0, len(allowed), per_line):
            line_commands = allowed[i:i + per_line]
            formatted = [f"{colors['yellow']}{cmd:12}{colors['end']}" for cmd in line_commands]
            print("  " + " ".join(formatted))
        
        print()
        print(f"{colors['green']}Use 'allowed add <command>' to add new commands{colors['end']}")
        print(f"{colors['green']}Use 'allowed remove <command>' to remove commands{colors['end']}")
        
    elif len(args) >= 2 and args[0] == "add":
        # Add commands to whitelist
        new_commands = list(args[1:])
        safe_executor.add_to_whitelist(new_commands)
        config_manager.add_allowed_commands(new_commands)
        print(f"{colors['green']}✅ Added commands to allowed list: {new_commands}{colors['end']}")
        
    elif len(args) >= 2 and args[0] == "remove":
        # Remove commands from whitelist
        remove_commands = list(args[1:])
        safe_executor.remove_from_whitelist(remove_commands)
        # Update config
        current = set(config_manager.config.executor.allowed_commands)
        current.difference_update(remove_commands)
        config_manager.config.executor.allowed_commands = list(current)
        print(f"{colors['yellow']}🗑️  Removed commands from allowed list: {remove_commands}{colors['end']}")
        
    else:
        print(f"{colors['red']}Usage: allowed [add|remove] <command1> [command2...]{colors['end']}")


@command("safe", "Execute command with safety checks", category="System")
def safe_execute(*args):
    """Execute a command using the safe executor."""
    if not args:
        print(f"{colors['red']}Usage: safe <command> [args...]{colors['end']}")
        return
        
    command_str = " ".join(args)
    return safe_executor.execute_with_feedback(command_str)

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
        Execute a system command safely using the safe executor.
        
        Args:
            command: The command to execute
            
        Returns:
            int: Command exit code
        """
        return safe_executor.execute_with_feedback(command)