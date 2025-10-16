"""Magic Shell - A magical wrapper around your real shell.

Entry point for the magic-shell command with PR 4 visual effects.
"""

import argparse
import asyncio
import sys
from pathlib import Path

from .core.bridge import PTYBridge
from .core.shell_detect import get_shell_with_fallback, get_shell_name
from .core.theme import create_theme, MagicTheme
from .core.config import load_config, get_config
from . import __version__


def _handle_timing_event(theme: MagicTheme, event: dict) -> None:
    """
    Handle shell timing events by calling appropriate theme methods.
    
    Args:
        theme: Theme instance
        event: Event dict with type, command, exit_code, etc.
    """
    event_type = event.get("type", "")
    
    if event_type == "command_start":
        command = event.get("command", "")
        theme.on_command_start(command)
    elif event_type == "command_end":
        command = event.get("command", "")
        exit_code = event.get("exit_code", 0)
        theme.on_command_end(command, exit_code)
    elif event_type == "prompt_start":
        theme.on_prompt_start()
    elif event_type == "prompt_end":
        theme.on_prompt_end()


def main() -> int:
    """Main entry point for Magic Shell with PR 4 config and effects."""
    parser = argparse.ArgumentParser(
        prog="magic-shell",
        description="A magical wrapper around your real shell - cosmetic effects with zero interference",
    )
    
    # Command line flags
    parser.add_argument(
        "--shell",
        type=str,
        help="Specify shell to wrap (default: auto-detect login shell)",
    )
    parser.add_argument(
        "--theme",
        choices=["veil", "ember", "plain"],
        help="Visual theme (overrides config file)",
    )
    parser.add_argument(
        "--plain",
        action="store_true",
        help="Disable all visual effects",
    )
    parser.add_argument(
        "--no-effects",
        action="store_true",
        help="Alias for --plain",
    )
    parser.add_argument(
        "--stage",
        action="store_true", 
        help="Enable experimental features",
    )
    parser.add_argument(
        "--config-dir",
        action="store_true",
        help="Show configuration directory path and exit",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    
    args = parser.parse_args()
    
    # Handle config directory query
    if args.config_dir:
        from .core.config import get_config_dir
        print(get_config_dir())
        return 0
    
    try:
        # Load configuration
        config = get_config()
        
        # Detect shell to use
        shell_override = args.shell or config.shell.shell_override
        shell_path = get_shell_with_fallback(shell_override)
        shell_name = get_shell_name(shell_path)
        
        # Determine theme (CLI args override config)
        if args.plain or args.no_effects:
            theme_name = "plain"
        else:
            theme_name = args.theme or config.effects.theme
            
        # Create theme with config
        theme = create_theme(theme_name, config)
        
        # Show startup information
        shell_info = {
            "version": __version__,
            "shell": shell_name,
            "hooks_supported": True,  # Will be updated by bridge
        }
        
        if config.shell.show_welcome:
            theme.on_startup(shell_info)
            
        # Create PTY bridge
        bridge = PTYBridge(
            shell_path=shell_path,
            stage_mode=args.stage
        )
        
        # Connect theme to bridge events
        bridge.add_event_callback(lambda event: _handle_timing_event(theme, event))
        
        # Run the bridge (this blocks until shell exits)
        exit_code = asyncio.run(bridge.run())
        
        return exit_code
        
    except RuntimeError as e:
        print(f"Magic Shell error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        # Shouldn't happen (Ctrl-C forwarded to shell), but just in case
        return 130


if __name__ == "__main__":
    sys.exit(main())