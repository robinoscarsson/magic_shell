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
from ..spells.wizard import Wizard


class Shell:
    """Main shell class for the Magic Shell."""
    
    def __init__(self):
        """Initialize the shell."""
        self.state = {"wizard_mode": False, "running": True}
        self.history = History()
        self.commands = CommandManager(self.state)
        self.wizard = Wizard()
        
        # Simple prompt session
        history_file = os.path.expanduser("~/.magic_shell_history")
        self.session = PromptSession(history=FileHistory(history_file))
        
    def run(self) -> int:
        """Run the shell main loop."""
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
