"""Core shell functionality for the Magic Shell."""

import os
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory

from ..utils.welcome import print_welcome
from ..utils.prompt import get_prompt_text
from .commands import CommandManager
from .registry import registry
from .history import History
from .config import config_manager
from .executor import safe_executor
from ..spells.wizard import Wizard


class Shell:
    """Main shell class for the Magic Shell."""
    
    def __init__(self):
        """Initialize the shell."""
        # Load configuration first
        self.config = config_manager.load_config()
        
        # Initialize state (may be overridden by config)
        self.state = {
            "wizard_mode": self.config.shell.wizard_mode_startup,
            "running": True
        }
        
        # Configure safe executor with loaded config
        safe_executor.config = {
            'allowed_commands': self.config.executor.allowed_commands,
            'default_timeout': self.config.executor.default_timeout,
            'max_output_size': self.config.executor.max_output_size,
            'additional_env_vars': self.config.executor.additional_env_vars,
            'working_directory': self.config.executor.working_directory
        }
        safe_executor.whitelist = set(self.config.executor.allowed_commands)
        
        # Initialize components
        self.history = History()
        self.commands = CommandManager(self.state)
        self.wizard = Wizard()
        
        # Setup prompt session with configuration
        history_file = os.path.expanduser(self.config.shell.history_file)
        self.session = PromptSession(
            history=FileHistory(history_file) if self.config.shell.enable_history else None
        )
        
    def run(self) -> int:
        """Run the shell main loop."""
        if self.config.shell.show_welcome:
            print_welcome()
        
        while self.state["running"]:
            try:
                prompt_text = get_prompt_text(self.state["wizard_mode"])
                cmd = self.session.prompt(prompt_text).strip()
                
                if not cmd:
                    continue
                    
                if self.commands.handle_special_command(cmd):
                    continue
                    
                if self.state["wizard_mode"]:
                    self.wizard.cast_spell(cmd)
                else:
                    self.commands.execute_command(cmd)
                    
            except KeyboardInterrupt:
                print("\n✨ Magic interrupted! Use 'quit' or ':quit' to exit.")
                continue
            except EOFError:
                print("\n👋 Goodbye!")
                break
        
        return 0
