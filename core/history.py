"""History management for the Magic Shell."""

class History:
    """Command history manager."""
    
    def __init__(self):
        """Initialize command history."""
        self.commands = []
    
    def add(self, command: str) -> None:
        """Add a command to history."""
        if command:
            self.commands.append(command)
    
    def display(self) -> None:
        """Display numbered command history."""
        if not self.commands:
            print("No command history available")
            return
            
        for i, cmd in enumerate(self.commands):
            print(f"{i}: {cmd}")
    
    def recall(self, index_str: str) -> str:
        """
        Recall a command from history by index.
        
        Args:
            index_str: String representation of history index
            
        Returns:
            str: The recalled command or empty string if invalid
        """
        try:
            index = int(index_str)
            cmd = self.commands[index]
            print(f"Executing: {cmd}")
            return cmd
        except ValueError:
            print(f"Error: '{index_str}' is not a valid history index")
            return ""
        except IndexError:
            print(f"Error: No command at history position {index_str}")
            return ""