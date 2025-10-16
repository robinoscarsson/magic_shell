"""Theme and visual effects module for Magic Shell.

This module will contain cosmetic effects triggered by command timing events.
Currently a placeholder for PR 4 implementation.
"""

from typing import Dict, Any


class MagicTheme:
    """Base class for Magic Shell visual themes."""
    
    def __init__(self, theme_name: str = "veil"):
        """
        Initialize theme.
        
        Args:
            theme_name: Name of the theme ("veil", "ember", "plain")
        """
        self.theme_name = theme_name
        self.effects_enabled = theme_name != "plain"
    
    def on_command_start(self) -> None:
        """Called when a command starts executing."""
        # Placeholder for PR 4: Add subtle visual indication
        pass
    
    def on_command_end(self, exit_code: int = 0) -> None:
        """
        Called when a command finishes executing.
        
        Args:
            exit_code: Exit code of the command
        """
        # Placeholder for PR 4: Success burst or failure rift
        if self.effects_enabled:
            if exit_code == 0:
                self._show_success_effect()
            else:
                self._show_failure_effect()
    
    def on_prompt_start(self) -> None:
        """Called when shell prompt is about to be displayed."""
        # Placeholder for PR 4: Prompt enhancement
        pass
    
    def on_prompt_end(self) -> None:
        """Called when shell prompt display is complete.""" 
        # Placeholder for PR 4: Finalize prompt
        pass
    
    def _show_success_effect(self) -> None:
        """Show success effect (placeholder for PR 4)."""
        # Future: Subtle glow or burst animation with rich
        pass
    
    def _show_failure_effect(self) -> None:
        """Show failure effect (placeholder for PR 4)."""
        # Future: Discrete rift or warning indicator with rich
        pass
    
    def show_startup_banner(self) -> None:
        """Show startup banner if effects are enabled."""
        if self.effects_enabled:
            # Minimal, non-intrusive startup indication
            print(f"🪄 Magic Shell ({self.theme_name} theme)")


# Theme registry for PR 4
AVAILABLE_THEMES = {
    "veil": "Subtle ethereal effects",
    "ember": "Warm glowing effects", 
    "plain": "No visual effects",
}


def create_theme(theme_name: str = "veil") -> MagicTheme:
    """
    Create a theme instance.
    
    Args:
        theme_name: Name of the theme
        
    Returns:
        MagicTheme: Theme instance
    """
    if theme_name not in AVAILABLE_THEMES:
        theme_name = "veil"  # Default fallback
    
    return MagicTheme(theme_name)