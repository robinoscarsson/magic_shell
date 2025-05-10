"""Core shell functionality for the Magic Shell."""

import os
import readline
from utils.welcome import print_welcome
from utils.prompt import get_prompt
from core.commands import CommandManager
from core.history import History
from spells.wizard import Wizard

class Shell:
    """Main shell class for the Magic Shell."""
    
    def __init__(self):
        """Initialize the shell."""
        self.state = {
            "wizard_mode": False,
            "running": True
        }
        
        self.history = History()
        self.commands = CommandManager(self.state)
        self.wizard = Wizard()
        
        # Set up tab completion
        self._setup_completion()
        
    def _setup_completion(self):
        """Configure tab completion for the shell."""
        # Define list of base commands for completion
        self.base_commands = [
            "exit", "quit", "help", "cd", "history", "wizard", "normal"
        ]
        
        # Register our completer function
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self._completer)
        
    def _completer(self, text, state):
        """
        Custom completer function for readline.
        
        Args:
            text: The text to complete
            state: The state of completion (0, 1, etc. for multiple matches)
            
        Returns:
            str: The completion suggestion or None
        """
        # Collect all possible completions
        options = []
        
        # Add built-in commands
        options.extend(self.base_commands)
        
        # Add spell names if in wizard mode
        if self.state["wizard_mode"]:
            options.extend(self.wizard.spells.keys())
            
        # Add file completion for cd command
        buffer = readline.get_line_buffer().lstrip()
        if buffer.startswith('cd '):
            path = buffer[3:]
            if not text:  # If we're just after 'cd '
                options = [f for f in os.listdir('.') if os.path.isdir(f)]
            else:
                # Try to complete partial directory names
                options = [f for f in os.listdir('.') 
                          if f.startswith(text) and os.path.isdir(f)]
            # Add trailing slash to directories
            options = [f"{o}/" for o in options]
                
        # Filter options that match the text being completed
        matches = [o for o in options if o.startswith(text)]
        
        # Return the state-th match or None if no more matches
        if state < len(matches):
            return matches[state]
        return None
        
    def run(self) -> int:
        """
        Run the shell main loop.
        
        Returns:
            int: Exit code (0 for normal exit, non-zero for errors)
        """
        print_welcome()
        
        # Main command loop
        while self.state["running"]:
            try:
                command = self._get_command()
                
                # Empty commands
                if not command:
                    continue
                    
                # Handle special commands first
                if self.commands.handle_special_command(command):
                    continue
                    
                # Execute command based on mode
                if self.state["wizard_mode"]:
                    self.wizard.cast_spell(command)
                else:
                    self.commands.execute_command(command)
                    
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print("\nExiting...")
                os.system("clear" if os.name == "posix" else "cls")
                break
        
        return 0
        
    def _get_command(self) -> str:
        """
        Get and process a command from the user.
        
        Returns:
            str: The command to execute, or empty string for internal commands
        """
        # Get and display command prompt
        prompt = get_prompt()
        
        # Get user input
        cmd = input(prompt).strip()
        
        # Skip empty commands
        if not cmd:
            return ""
            
        # Add to history
        self.history.add(cmd)
        
        # Handle history display command
        if cmd.lower() == "history":
            self.history.display()
            return ""
            
        # Handle history recall
        if cmd.startswith("!"):
            return self.history.recall(cmd[1:])
            
        return cmd