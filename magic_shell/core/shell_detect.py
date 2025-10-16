"""Shell detection utilities for Magic Shell."""

import os
import pwd
import subprocess
from pathlib import Path
from typing import Optional


def get_login_shell() -> str:
    """
    Detect the user's login shell.
    
    Returns:
        str: Path to the user's login shell
    """
    try:
        # Try to get from passwd database (most reliable)
        user_entry = pwd.getpwuid(os.getuid())
        login_shell = user_entry.pw_shell
        
        if login_shell and Path(login_shell).exists():
            return login_shell
    except (KeyError, OSError):
        pass
    
    # Fallback methods
    fallback_methods = [
        lambda: os.environ.get("SHELL"),
        lambda: subprocess.run(["getent", "passwd", os.getlogin()], 
                              capture_output=True, text=True, check=False).stdout.split(":")[-1].strip(),
        lambda: "/bin/bash",  # Common default
        lambda: "/bin/sh",    # POSIX fallback
    ]
    
    for method in fallback_methods:
        try:
            shell = method()
            if shell and Path(shell).exists():
                return shell
        except (OSError, subprocess.CalledProcessError):
            continue
    
    # Last resort - check common shell locations
    common_shells = ["/bin/bash", "/usr/bin/bash", "/bin/zsh", "/usr/bin/zsh", "/bin/sh"]
    for shell in common_shells:
        if Path(shell).exists():
            return shell
    
    raise RuntimeError("Could not detect any available shell")


def get_shell_name(shell_path: str) -> str:
    """
    Get the name of a shell from its path.
    
    Args:
        shell_path: Path to the shell executable
        
    Returns:
        str: Shell name (e.g., "bash", "zsh", "fish")
    """
    return Path(shell_path).name


def validate_shell(shell_path: str) -> bool:
    """
    Validate that a shell path exists and is executable.
    
    Args:
        shell_path: Path to validate
        
    Returns:
        bool: True if shell is valid and executable
    """
    try:
        path = Path(shell_path)
        return path.exists() and os.access(path, os.X_OK)
    except (OSError, TypeError):
        return False


def get_shell_with_fallback(requested_shell: Optional[str] = None) -> str:
    """
    Get shell path with fallback to login shell.
    
    Args:
        requested_shell: Specific shell requested by user
        
    Returns:
        str: Path to shell to use
        
    Raises:
        RuntimeError: If no valid shell can be found
    """
    if requested_shell:
        if validate_shell(requested_shell):
            return requested_shell
        else:
            raise RuntimeError(f"Requested shell '{requested_shell}' is not available or not executable")
    
    return get_login_shell()