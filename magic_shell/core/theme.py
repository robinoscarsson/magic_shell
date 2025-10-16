"""
Magic Shell theme system with rich-based visual effects.

Provides beautiful, subtle visual effects for PR 4.
"""

import asyncio
import subprocess
import time
from typing import Dict, Optional, Any, Callable

from rich.console import Console
from rich.text import Text
from rich.style import Style
from rich.panel import Panel
from rich.columns import Columns

from .config import MagicShellConfig, is_password_prompt, is_safe_environment


class MagicTheme:
    """Base class for Magic Shell themes with rich-based visual effects."""
    
    def __init__(self, name: str = "plain", config: Optional[MagicShellConfig] = None):
        """Initialize theme with configuration."""
        self.name = name
        self.config = config
        self.console = Console()
        self._last_command_time = 0
        self._password_mode = False
        self._effects_enabled = True
        
        if config:
            self._effects_enabled = (
                config.effects.enabled 
                and is_safe_environment()
                and not config.safety.compatible_mode
            )
    
    def _should_show_effects(self, text: str = "") -> bool:
        """Check if effects should be shown based on safety settings."""
        if not self._effects_enabled:
            return False
            
        if self.config and self.config.effects.no_echo_detection:
            if is_password_prompt(text):
                self._password_mode = True
                return False
            
        return not self._password_mode
    
    def on_startup(self, shell_info: Dict[str, Any]) -> None:
        """Called when Magic Shell starts up."""
        if not self.config or not self.config.shell.startup_banner:
            return
            
        hook_status = "✨ precise timing" if shell_info.get("hooks_supported") else "⚡ basic mode"
        shell_name = shell_info.get("shell", "unknown")
        
        banner = Panel(
            f"[bold blue]Magic Shell[/] [dim]v{shell_info.get('version', '0.4.0')}[/]\n"
            f"[dim]{hook_status} • {shell_name} • {self.name} theme[/]",
            border_style="blue",
            padding=(0, 1),
            width=60
        )
        
        self.console.print(banner)
    
    def on_command_start(self, command: str) -> None:
        """Called when a command starts executing."""
        if not self._should_show_effects(command):
            return
            
        self._last_command_time = time.time()
        
        if self.config and self.config.effects.command_shimmer:
            self._show_command_shimmer(command)
    
    def on_command_end(self, command: str, exit_code: int) -> None:
        """Called when a command finishes executing."""
        if not self._should_show_effects():
            return
            
        duration = time.time() - self._last_command_time
        
        if exit_code == 0 and self.config and self.config.effects.success_glow:
            self._show_success_glow(command, duration)
        elif exit_code != 0 and self.config and self.config.effects.error_pulse:
            self._show_error_pulse(command, exit_code, duration)
    
    def on_prompt_start(self) -> None:
        """Called when the prompt is about to be displayed."""
        # Reset password mode when we see a new prompt
        self._password_mode = False
    
    def on_prompt_end(self) -> None:
        """Called when the prompt is ready for input."""
        pass
    
    def _show_command_shimmer(self, command: str) -> None:
        """Show subtle shimmer effect when command starts."""
        pass  # Base implementation does nothing
    
    def _show_success_glow(self, command: str, duration: float) -> None:
        """Show success glow effect."""
        pass  # Base implementation does nothing
    
    def _show_error_pulse(self, command: str, exit_code: int, duration: float) -> None:
        """Show error pulse effect."""
        pass  # Base implementation does nothing
    
    def _get_git_info(self) -> Optional[Dict[str, str]]:
        """Get git repository information if available."""
        if not self.config or not self.config.effects.git_badge:
            return None
            
        try:
            # Quick git branch check
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                timeout=0.1  # Very fast timeout
            )
            
            if result.returncode == 0:
                branch = result.stdout.strip()
                if branch:
                    return {"branch": branch}
                    
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
        return None


class VeilTheme(MagicTheme):
    """Subtle, elegant theme with gentle effects."""
    
    def __init__(self, config: Optional[MagicShellConfig] = None):
        super().__init__("veil", config)
    
    def _show_command_shimmer(self, command: str) -> None:
        """Show gentle shimmer for command start."""
        if len(command) > 50:
            command = command[:47] + "..."
            
        shimmer = Text(f"✨ {command}", style="dim blue")
        self.console.print(shimmer, end="", flush=True)
        
        # Brief pause, then clear
        time.sleep(0.1)
        self.console.print("\r" + " " * len(shimmer) + "\r", end="", flush=True)
    
    def _show_success_glow(self, command: str, duration: float) -> None:
        """Show gentle success glow."""
        intensity = self.config.effects.intensity if self.config else 0.7
        
        if duration < 0.1:
            return  # Too fast to show effect
            
        # Brief success indicator
        if duration > 2.0:
            glow = Text(f"✅ {duration:.1f}s", style=f"green")
        else:
            glow = Text("✨", style="green")
            
        self.console.print(glow, end=" ")
        time.sleep(0.05)  # Brief pause for visibility
    
    def _show_error_pulse(self, command: str, exit_code: int, duration: float) -> None:
        """Show subtle error indication."""
        pulse = Text(f"⚠️  exit {exit_code}", style="red")
        self.console.print(pulse, end=" ")


class EmberTheme(MagicTheme):
    """Warm, fire-inspired theme with glowing effects."""
    
    def __init__(self, config: Optional[MagicShellConfig] = None):
        super().__init__("ember", config)
    
    def _show_command_shimmer(self, command: str) -> None:
        """Show warm shimmer for command start."""
        shimmer = Text("🔥", style="orange1")
        self.console.print(shimmer, end="", flush=True)
        time.sleep(0.08)
        self.console.print("\r \r", end="", flush=True)
    
    def _show_success_glow(self, command: str, duration: float) -> None:
        """Show warm success glow."""
        if duration > 1.0:
            glow = Text(f"🔥 {duration:.1f}s", style="yellow")
        else:
            glow = Text("✨", style="yellow")
            
        self.console.print(glow, end=" ")
        time.sleep(0.05)
    
    def _show_error_pulse(self, command: str, exit_code: int, duration: float) -> None:
        """Show fiery error indication."""
        pulse = Text(f"💥 exit {exit_code}", style="red")
        self.console.print(pulse, end=" ")


class PlainTheme(MagicTheme):
    """Minimal theme with no visual effects."""
    
    def __init__(self, config: Optional[MagicShellConfig] = None):
        super().__init__("plain", config)
        self._effects_enabled = False  # Override to disable all effects


# Theme registry
AVAILABLE_THEMES = {
    "veil": "Subtle ethereal effects with gentle glows",
    "ember": "Warm fire-inspired effects with glowing embers", 
    "plain": "No visual effects (compatible mode)",
}


def create_theme(theme_name: str = "veil", config: Optional[MagicShellConfig] = None) -> MagicTheme:
    """
    Create a theme instance.
    
    Args:
        theme_name: Name of the theme
        config: Configuration instance
        
    Returns:
        MagicTheme: Theme instance
    """
    if theme_name not in AVAILABLE_THEMES:
        theme_name = "veil"  # Default fallback
    
    if theme_name == "veil":
        return VeilTheme(config)
    elif theme_name == "ember":
        return EmberTheme(config)
    else:
        return PlainTheme(config)