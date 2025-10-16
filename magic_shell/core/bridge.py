"""PTY bridge for Magic Shell - forwards terminal I/O with zero interference."""

import asyncio
import os
import pty
import signal
import struct
import sys
import termios
import tty
from typing import Optional, Tuple, List, Callable

from .shell_detect import get_shell_with_fallback, get_shell_name
from .hooks import shell_hooks


class PTYBridge:
    """
    PTY bridge that spawns a shell and forwards all I/O transparently.
    
    This class implements a pseudo-terminal bridge that:
    1. Spawns the user's shell in a PTY
    2. Forwards all input/output as raw bytes  
    3. Handles signals (Ctrl-C, SIGWINCH)
    4. Preserves exit codes
    5. Maintains perfect compatibility with all terminal programs
    """
    
    def __init__(self, shell_path: Optional[str] = None, stage_mode: bool = False):
        """
        Initialize PTY bridge.
        
        Args:
            shell_path: Path to shell executable (auto-detected if None)
            stage_mode: Enable experimental features
        """
        self.shell_path = get_shell_with_fallback(shell_path)
        self.shell_name = get_shell_name(self.shell_path)
        self.stage_mode = stage_mode
        self.master_fd: Optional[int] = None
        self.child_pid: Optional[int] = None
        self.original_termios: Optional[list] = None
        self.exit_code: int = 0
        
        # Event callbacks for command timing
        self.event_callbacks: List[Callable[[str], None]] = []
        
        # Hook injection support
        self.hooks_injected = False
        
    def _setup_terminal(self) -> None:
        """Setup terminal for raw mode."""
        try:
            # Save original terminal settings
            self.original_termios = termios.tcgetattr(sys.stdin.fileno())
            
            # Set terminal to raw mode for transparent forwarding
            tty.setraw(sys.stdin.fileno())
            
        except (OSError, termios.error) as e:
            raise RuntimeError(f"Failed to setup terminal: {e}")
    
    def _restore_terminal(self) -> None:
        """Restore original terminal settings."""
        if self.original_termios is not None:
            try:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.original_termios)
            except (OSError, termios.error):
                pass  # Best effort restoration
    
    def _handle_window_resize(self, signum: int, frame) -> None:
        """Handle SIGWINCH (window resize) signals."""
        if self.master_fd is not None:
            try:
                # Get current terminal size
                rows, cols = os.get_terminal_size()
                
                # Set PTY size to match
                winsize = struct.pack("HHHH", rows, cols, 0, 0)
                import fcntl
                fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, winsize)
                
            except (OSError, struct.error):
                pass  # Best effort resize
    
    def _spawn_shell(self) -> Tuple[int, int]:
        """
        Spawn shell in PTY.
        
        Returns:
            Tuple[int, int]: (master_fd, child_pid)
        """
        try:
            # Create PTY pair
            master_fd, slave_fd = pty.openpty()
            
            # Fork process
            pid = os.fork()
            
            if pid == 0:
                # Child process - become the shell
                os.close(master_fd)
                
                # Make slave PTY the controlling terminal
                os.setsid()
                os.dup2(slave_fd, 0)  # stdin
                os.dup2(slave_fd, 1)  # stdout  
                os.dup2(slave_fd, 2)  # stderr
                os.close(slave_fd)
                
                # Set terminal size
                try:
                    rows, cols = os.get_terminal_size()
                    winsize = struct.pack("HHHH", rows, cols, 0, 0)
                    import fcntl
                    fcntl.ioctl(0, termios.TIOCSWINSZ, winsize)
                except (OSError, struct.error):
                    pass
                
                # Execute shell with hook injection
                shell_args = [self.shell_path]
                
                # Add hook injection for supported shells
                if shell_hooks.is_supported_shell(self.shell_name):
                    # Create initialization script for hooks
                    hook_commands = shell_hooks.inject_hooks(self.shell_name)
                    if hook_commands:
                        # For bash/zsh, use -c to execute init commands then interactive mode
                        if self.shell_name in ["bash", "zsh"]:
                            init_script = f"{hook_commands}; exec {self.shell_path}"
                            shell_args = [self.shell_path, "-c", init_script]
                
                os.execv(self.shell_path, shell_args)
                
            else:
                # Parent process - manage PTY
                os.close(slave_fd)
                return master_fd, pid
                
        except OSError as e:
            raise RuntimeError(f"Failed to spawn shell: {e}")
    
    async def _forward_input(self) -> None:
        """Forward input from stdin to shell (async)."""
        loop = asyncio.get_event_loop()
        
        while True:
            try:
                # Read from stdin in non-blocking way
                data = await loop.run_in_executor(None, os.read, sys.stdin.fileno(), 1024)
                
                if not data:
                    break
                    
                # Forward to shell
                if self.master_fd is not None:
                    os.write(self.master_fd, data)
                    
            except OSError:
                break
    
    async def _forward_output(self) -> None:
        """Forward output from shell to stdout, parsing OSC markers (async)."""
        loop = asyncio.get_event_loop()
        
        while True:
            try:
                # Read from shell
                if self.master_fd is not None:
                    data = await loop.run_in_executor(None, os.read, self.master_fd, 1024)
                    
                    if not data:
                        break
                    
                    # Parse OSC markers and extract events
                    cleaned_data, events = shell_hooks.parse_osc_markers(data)
                    
                    # Trigger event callbacks for detected timing events
                    for event in events:
                        self._trigger_event(event)
                    
                    # Forward cleaned data (without markers) to stdout
                    if cleaned_data:
                        os.write(sys.stdout.fileno(), cleaned_data)
                    
            except OSError:
                break
    
    def _wait_for_child(self) -> int:
        """
        Wait for child process to exit and get exit code.
        
        Returns:
            int: Exit code of child process
        """
        if self.child_pid is None:
            return 1
            
        try:
            _, status = os.waitpid(self.child_pid, 0)
            
            if os.WIFEXITED(status):
                return os.WEXITSTATUS(status)
            elif os.WIFSIGNALED(status):
                # Child was killed by signal
                return 128 + os.WTERMSIG(status)
            else:
                return 1
                
        except OSError:
            return 1
    
    async def run(self) -> int:
        """
        Run the PTY bridge.
        
        Returns:
            int: Exit code of the shell process
        """
        try:
            # Setup signal handlers
            signal.signal(signal.SIGWINCH, self._handle_window_resize)
            
            # Setup terminal
            self._setup_terminal()
            
            # Spawn shell
            self.master_fd, self.child_pid = self._spawn_shell()
            
            # Create forwarding tasks
            input_task = asyncio.create_task(self._forward_input())
            output_task = asyncio.create_task(self._forward_output())
            
            # Wait for either task to complete (shell exit or connection lost)
            try:
                await asyncio.wait([input_task, output_task], return_when=asyncio.FIRST_COMPLETED)
            except KeyboardInterrupt:
                # Ctrl-C should be forwarded to shell, not handled here
                pass
            
            # Cancel remaining tasks
            input_task.cancel()
            output_task.cancel()
            
            # Wait for child to exit and get exit code
            self.exit_code = self._wait_for_child()
            
            return self.exit_code
            
        finally:
            # Cleanup
            self._restore_terminal()
            
            if self.master_fd is not None:
                try:
                    os.close(self.master_fd)
                except OSError:
                    pass
    
    def add_event_callback(self, callback: Callable[[str], None]) -> None:
        """
        Add a callback for shell timing events.
        
        Args:
            callback: Function to call with event name
        """
        self.event_callbacks.append(callback)
    
    def _trigger_event(self, event_name: str) -> None:
        """
        Trigger all registered event callbacks.
        
        Args:
            event_name: Name of the event (command_start, command_end, etc.)
        """
        for callback in self.event_callbacks:
            try:
                callback(event_name)
            except Exception:
                # Don't let callback errors break the PTY bridge
                pass
    
    def get_shell_info(self) -> dict:
        """
        Get information about the shell being wrapped.
        
        Returns:
            dict: Shell information
        """
        return {
            "path": self.shell_path,
            "name": self.shell_name,
            "stage_mode": self.stage_mode,
            "hooks_supported": shell_hooks.is_supported_shell(self.shell_name),
        }