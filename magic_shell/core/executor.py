"""Safe subprocess execution for Magic Shell."""

import os
import shlex
import subprocess
import signal
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import logging

from ..utils.colors import COLORS as colors


class SafeExecutor:
    """Safe subprocess execution with whitelisting and timeouts."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the safe executor.
        
        Args:
            config: Configuration dictionary with execution settings
        """
        self.config = config or {}
        
        # Default safe commands whitelist
        self.default_whitelist = {
            'ls', 'cat', 'grep', 'find', 'head', 'tail', 'wc', 'sort', 'uniq',
            'pwd', 'whoami', 'date', 'echo', 'which', 'man', 'help',
            'git', 'python3', 'python', 'pip', 'pip3', 'node', 'npm',
            'tree', 'du', 'df', 'ps', 'top', 'htop', 'free', 'uptime',
            'curl', 'wget', 'ssh', 'scp', 'rsync', 'tar', 'zip', 'unzip'
        }
        
        # Get whitelist from config or use defaults
        self.whitelist = set(self.config.get('allowed_commands', self.default_whitelist))
        
        # Default execution settings
        self.default_timeout = self.config.get('default_timeout', 30)  # 30 seconds
        self.max_output_size = self.config.get('max_output_size', 1024 * 1024)  # 1MB
        self.working_directory = self.config.get('working_directory', os.getcwd())
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def is_command_allowed(self, command: str) -> bool:
        """
        Check if a command is in the whitelist.
        
        Args:
            command: Command name to check
            
        Returns:
            bool: True if command is allowed, False otherwise
        """
        # Extract base command name
        base_command = command.split()[0] if command.strip() else ""
        base_command = os.path.basename(base_command)  # Remove path
        
        return base_command in self.whitelist
    
    def execute_safe(
        self, 
        command: str, 
        timeout: Optional[int] = None,
        capture_output: bool = True,
        check_whitelist: bool = True
    ) -> Tuple[int, str, str]:
        """
        Safely execute a command with proper escaping and timeout.
        
        Args:
            command: Command string to execute
            timeout: Timeout in seconds (None for default)
            capture_output: Whether to capture stdout/stderr
            check_whitelist: Whether to check command whitelist
            
        Returns:
            Tuple of (return_code, stdout, stderr)
            
        Raises:
            SecurityError: If command is not whitelisted
            subprocess.TimeoutExpired: If command times out
        """
        if not command.strip():
            return 1, "", "Empty command"
        
        # Parse command safely
        try:
            parsed_command = shlex.split(command)
        except ValueError as e:
            return 1, "", f"Invalid command syntax: {e}"
        
        if not parsed_command:
            return 1, "", "No command specified"
        
        # Check whitelist
        if check_whitelist and not self.is_command_allowed(parsed_command[0]):
            base_cmd = os.path.basename(parsed_command[0])
            return 1, "", f"Command '{base_cmd}' is not in the allowed commands list"
        
        # Set timeout
        exec_timeout = timeout or self.default_timeout
        
        try:
            # Execute with proper security settings
            result = subprocess.run(
                parsed_command,
                cwd=self.working_directory,
                timeout=exec_timeout,
                capture_output=capture_output,
                text=True,
                env=self._get_safe_environment(),
                # Security settings
                start_new_session=True,  # Create new process group
            )
            
            # Limit output size to prevent memory issues
            stdout = result.stdout or ""
            stderr = result.stderr or ""
            
            if len(stdout) > self.max_output_size:
                stdout = stdout[:self.max_output_size] + "\n... (output truncated)"
                
            if len(stderr) > self.max_output_size:
                stderr = stderr[:self.max_output_size] + "\n... (error output truncated)"
            
            return result.returncode, stdout, stderr
            
        except subprocess.TimeoutExpired:
            return 124, "", f"Command timed out after {exec_timeout} seconds"
            
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout or "", e.stderr or ""
            
        except FileNotFoundError:
            return 127, "", f"Command not found: {parsed_command[0]}"
            
        except PermissionError:
            return 126, "", f"Permission denied: {parsed_command[0]}"
            
        except Exception as e:
            self.logger.error(f"Unexpected error executing command '{command}': {e}")
            return 1, "", f"Execution error: {e}"
    
    def _get_safe_environment(self) -> Dict[str, str]:
        """
        Get a safe environment for subprocess execution.
        
        Returns:
            Dict of environment variables
        """
        # Start with minimal safe environment
        safe_env = {
            'PATH': os.environ.get('PATH', '/usr/local/bin:/usr/bin:/bin'),
            'HOME': os.environ.get('HOME', '/tmp'),
            'USER': os.environ.get('USER', 'unknown'),
            'TERM': os.environ.get('TERM', 'xterm-256color'),
            'LANG': os.environ.get('LANG', 'C.UTF-8'),
        }
        
        # Add additional safe variables from config
        additional_env = self.config.get('additional_env_vars', {})
        safe_env.update(additional_env)
        
        return safe_env
    
    def execute_with_feedback(self, command: str, show_progress: bool = True) -> int:
        """
        Execute command with user feedback and progress indication.
        
        Args:
            command: Command to execute
            show_progress: Whether to show progress feedback
            
        Returns:
            int: Exit code of the command
        """
        if show_progress:
            print(f"{colors['blue']}🔄 Executing: {command}{colors['end']}")
        
        returncode, stdout, stderr = self.execute_safe(command)
        
        # Print output with appropriate colors
        if stdout:
            print(stdout.rstrip())
            
        if stderr:
            if returncode == 0:
                # Some commands output helpful info to stderr
                print(f"{colors['yellow']}{stderr.rstrip()}{colors['end']}")
            else:
                print(f"{colors['red']}{stderr.rstrip()}{colors['end']}")
        
        # Show completion status
        if show_progress:
            if returncode == 0:
                print(f"{colors['green']}✅ Command completed successfully{colors['end']}")
            else:
                print(f"{colors['red']}❌ Command failed with exit code {returncode}{colors['end']}")
        
        return returncode
    
    def add_to_whitelist(self, commands: List[str]) -> None:
        """
        Add commands to the whitelist.
        
        Args:
            commands: List of command names to add
        """
        self.whitelist.update(commands)
        self.logger.info(f"Added commands to whitelist: {commands}")
    
    def remove_from_whitelist(self, commands: List[str]) -> None:
        """
        Remove commands from the whitelist.
        
        Args:
            commands: List of command names to remove
        """
        self.whitelist.difference_update(commands)
        self.logger.info(f"Removed commands from whitelist: {commands}")
    
    def list_allowed_commands(self) -> List[str]:
        """
        Get list of allowed commands.
        
        Returns:
            List of allowed command names
        """
        return sorted(list(self.whitelist))


# Global safe executor instance (will be configured when config is loaded)
safe_executor = SafeExecutor()