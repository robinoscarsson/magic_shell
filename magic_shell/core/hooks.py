"""Shell hooks for precise command timing in Magic Shell.

This module injects timing hooks into different shells to emit OSC markers
that allow the PTY bridge to detect exact command boundaries.
"""

import re
from typing import Dict, Optional


class ShellHooks:
    """Manages shell-specific hook injection for command timing."""
    
    # OSC (Operating System Command) escape sequences for markers
    # These are invisible to the user but detectable by the PTY bridge
    OSC_COMMAND_START = "\033]133;A\007"      # Command started
    OSC_COMMAND_END = "\033]133;B\007"        # Command finished  
    OSC_PROMPT_START = "\033]133;P\007"       # Prompt started
    OSC_PROMPT_END = "\033]133;Q\007"         # Prompt finished
    
    def __init__(self):
        """Initialize shell hooks manager."""
        self.hooks = {
            "bash": self._get_bash_hooks,
            "zsh": self._get_zsh_hooks,
            "fish": self._get_fish_hooks,
        }
    
    def _get_bash_hooks(self) -> Dict[str, str]:
        """
        Generate bash hook commands.
        
        Returns:
            Dict[str, str]: Hook commands for bash
        """
        # Bash uses PROMPT_COMMAND and DEBUG trap for timing
        return {
            "init_commands": [
                # Set up prompt command to emit prompt markers
                f'PROMPT_COMMAND="printf \'{self.OSC_PROMPT_START}\'; ${{PROMPT_COMMAND}}; printf \'{self.OSC_PROMPT_END}\'"',
                
                # Set up DEBUG trap to emit command start marker
                f'trap \'printf "{self.OSC_COMMAND_START}"\' DEBUG',
                
                # Set up command completion detection via PROMPT_COMMAND
                f'PROMPT_COMMAND="printf \'{self.OSC_COMMAND_END}\'; ${{PROMPT_COMMAND}}"',
            ]
        }
    
    def _get_zsh_hooks(self) -> Dict[str, str]:
        """
        Generate zsh hook commands.
        
        Returns:
            Dict[str, str]: Hook commands for zsh
        """
        # Zsh has preexec and precmd hooks which are perfect for this
        return {
            "init_commands": [
                # Define preexec function (called before command execution)
                f'preexec() {{ printf "{self.OSC_COMMAND_START}" }}',
                
                # Define precmd function (called before prompt display)  
                f'precmd() {{ printf "{self.OSC_COMMAND_END}"; printf "{self.OSC_PROMPT_START}"; }}',
                
                # Emit prompt end marker after prompt setup
                f'PROMPT="${{PROMPT}}"$\'\\033]133;Q\\007\'',
            ]
        }
    
    def _get_fish_hooks(self) -> Dict[str, str]:
        """
        Generate fish shell hook commands.
        
        Returns:
            Dict[str, str]: Hook commands for fish
        """
        # Fish has event-based hooks
        return {
            "init_commands": [
                # Command start hook
                f'function __magic_shell_preexec --on-event fish_preexec; printf "{self.OSC_COMMAND_START}"; end',
                
                # Command end and prompt start hook  
                f'function __magic_shell_precmd --on-event fish_prompt; printf "{self.OSC_COMMAND_END}"; printf "{self.OSC_PROMPT_START}"; end',
                
                # Prompt end marker
                f'function fish_prompt; printf "{self.OSC_PROMPT_END}"; __magic_shell_original_prompt; end',
            ]
        }
    
    def get_shell_hooks(self, shell_name: str) -> Optional[Dict[str, str]]:
        """
        Get hook commands for a specific shell.
        
        Args:
            shell_name: Name of the shell (bash, zsh, fish)
            
        Returns:
            Optional[Dict[str, str]]: Hook commands or None if not supported
        """
        hook_generator = self.hooks.get(shell_name.lower())
        if hook_generator:
            return hook_generator()
        return None
    
    def inject_hooks(self, shell_name: str) -> str:
        """
        Generate shell initialization commands to inject hooks.
        
        Args:
            shell_name: Name of the shell
            
        Returns:
            str: Shell commands to execute for hook injection
        """
        hooks = self.get_shell_hooks(shell_name)
        if not hooks:
            # For unsupported shells, return empty - no timing available
            return ""
        
        # Join all initialization commands
        commands = hooks.get("init_commands", [])
        return "; ".join(commands) + "\n"
    
    @classmethod
    def parse_osc_markers(cls, data: bytes) -> tuple[bytes, list[str]]:
        """
        Parse OSC markers from terminal data.
        
        Args:
            data: Raw terminal data bytes
            
        Returns:
            tuple: (cleaned_data_without_markers, list_of_detected_events)
        """
        # Convert to string for processing
        try:
            text = data.decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            # Return original data if not valid UTF-8
            return data, []
        
        events = []
        
        # Define marker patterns and their event names
        patterns = [
            (cls.OSC_COMMAND_START, "command_start"),
            (cls.OSC_COMMAND_END, "command_end"),
            (cls.OSC_PROMPT_START, "prompt_start"), 
            (cls.OSC_PROMPT_END, "prompt_end"),
        ]
        
        # Remove markers and collect events
        cleaned_text = text
        for marker, event_name in patterns:
            if marker in cleaned_text:
                events.append(event_name)
                cleaned_text = cleaned_text.replace(marker, "")
        
        # Convert back to bytes
        cleaned_data = cleaned_text.encode('utf-8', errors='ignore')
        
        return cleaned_data, events
    
    def is_supported_shell(self, shell_name: str) -> bool:
        """
        Check if a shell is supported for hook injection.
        
        Args:
            shell_name: Name of the shell
            
        Returns:
            bool: True if shell hooks are supported
        """
        return shell_name.lower() in self.hooks


# Global instance
shell_hooks = ShellHooks()