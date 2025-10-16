"""Command registry system for Magic Shell."""

import inspect
import os
import importlib
import pkgutil
from typing import Dict, Callable, List, Optional, Any
from dataclasses import dataclass
from functools import wraps

from ..utils.colors import COLORS as colors


@dataclass
class CommandInfo:
    """Information about a registered command."""
    
    name: str
    func: Callable
    help_text: str
    aliases: List[str]
    category: str
    wizard_only: bool = False
    

class CommandRegistry:
    """Central registry for all shell commands and spells."""
    
    def __init__(self):
        """Initialize the command registry."""
        self.commands: Dict[str, CommandInfo] = {}
        self.categories: Dict[str, List[CommandInfo]] = {}
        
    def register(
        self, 
        name: str, 
        help_text: str = "",
        aliases: Optional[List[str]] = None,
        category: str = "General",
        wizard_only: bool = False
    ):
        """
        Decorator to register a command.
        
        Args:
            name: Command name
            help_text: Help description for the command
            aliases: List of command aliases
            category: Command category for help organization
            wizard_only: Whether command is only available in wizard mode
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            # Create command info
            cmd_info = CommandInfo(
                name=name,
                func=func,
                help_text=help_text or f"Execute {name}",
                aliases=aliases or [],
                category=category,
                wizard_only=wizard_only
            )
            
            # Register main command name
            self.commands[name] = cmd_info
            
            # Register aliases
            for alias in (aliases or []):
                self.commands[alias] = cmd_info
            
            # Add to category
            if category not in self.categories:
                self.categories[category] = []
            if cmd_info not in self.categories[category]:
                self.categories[category].append(cmd_info)
                
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
            
        return decorator
    
    def get_command(self, name: str) -> Optional[CommandInfo]:
        """
        Get command info by name or alias.
        
        Args:
            name: Command name or alias
            
        Returns:
            CommandInfo if found, None otherwise
        """
        return self.commands.get(name.lower())
    
    def execute_command(self, name: str, *args, **kwargs) -> Any:
        """
        Execute a command by name.
        
        Args:
            name: Command name or alias
            *args: Arguments to pass to command
            **kwargs: Keyword arguments to pass to command
            
        Returns:
            Command result or None if command not found
        """
        cmd_info = self.get_command(name)
        if not cmd_info:
            return None
            
        try:
            # Get function signature to determine how to call it
            sig = inspect.signature(cmd_info.func)
            
            # Call with appropriate arguments based on signature
            if len(sig.parameters) == 0:
                return cmd_info.func()
            else:
                return cmd_info.func(*args, **kwargs)
                
        except Exception as e:
            print(f"{colors['red']}Error executing command '{name}': {e}{colors['end']}")
            return None
    
    def list_commands(self, wizard_mode: bool = False) -> List[CommandInfo]:
        """
        List all available commands.
        
        Args:
            wizard_mode: Whether to include wizard-only commands
            
        Returns:
            List of available CommandInfo objects
        """
        available_commands = []
        seen_commands = set()
        
        for cmd_info in self.commands.values():
            # Skip duplicates (from aliases)
            if cmd_info.name in seen_commands:
                continue
            seen_commands.add(cmd_info.name)
            
            # Filter by wizard mode
            if cmd_info.wizard_only and not wizard_mode:
                continue
                
            available_commands.append(cmd_info)
            
        return available_commands
    
    def print_help(self, wizard_mode: bool = False):
        """
        Print formatted help for all commands.
        
        Args:
            wizard_mode: Whether to show wizard-mode specific help
        """
        print(f"{colors['green']}=== 🧙‍♂️ Magic Shell Help 🧙‍♂️ ==={colors['end']}")
        print()
        
        # Group commands by category
        available_commands = self.list_commands(wizard_mode)
        categories = {}
        
        for cmd in available_commands:
            if cmd.category not in categories:
                categories[cmd.category] = []
            categories[cmd.category].append(cmd)
        
        # Print commands by category
        for category_name in sorted(categories.keys()):
            print(f"{colors['cyan']}{category_name} Commands:{colors['end']}")
            
            for cmd in sorted(categories[category_name], key=lambda x: x.name):
                aliases_text = ""
                if cmd.aliases:
                    aliases_text = f" ({', '.join(cmd.aliases)})"
                
                color = 'purple' if cmd.wizard_only else 'yellow'
                print(f"  {colors[color]}{cmd.name}{aliases_text}{colors['end']} - {cmd.help_text}")
            
            print()
        
        mode_text = "wizard mode" if wizard_mode else "normal mode"
        print(f"{colors['green']}Currently in {mode_text}. Press Ctrl+C to interrupt, Ctrl+D or :quit to exit{colors['end']}")
    
    def discover_commands(self, package_name: str):
        """
        Auto-discover and register commands from a package.
        
        Args:
            package_name: Full package name to scan for commands
        """
        try:
            # Import the package
            package = importlib.import_module(package_name)
            
            # Walk through all modules in the package
            for importer, modname, ispkg in pkgutil.iter_modules(
                package.__path__, 
                package.__name__ + "."
            ):
                try:
                    # Import the module
                    module = importlib.import_module(modname)
                    
                    # Look for functions with command registration
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isfunction(obj) and 
                            hasattr(obj, '_magic_command_info')):
                            # This function was decorated with @command
                            cmd_info = obj._magic_command_info
                            self.commands[cmd_info.name] = cmd_info
                            
                            # Register aliases
                            for alias in cmd_info.aliases:
                                self.commands[alias] = cmd_info
                                
                except ImportError as e:
                    # Skip modules that can't be imported
                    continue
                    
        except ImportError:
            # Package doesn't exist, skip
            pass


# Global registry instance
registry = CommandRegistry()


def command(
    name: str,
    help_text: str = "",
    aliases: Optional[List[str]] = None,
    category: str = "General", 
    wizard_only: bool = False
):
    """
    Decorator to register a command with the global registry.
    
    Args:
        name: Command name
        help_text: Help description
        aliases: List of aliases
        category: Command category
        wizard_only: Whether command is wizard-only
        
    Returns:
        Decorator function
    """
    return registry.register(name, help_text, aliases, category, wizard_only)