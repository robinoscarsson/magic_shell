"""Magic Shell - A magical wrapper around your real shell.

Entry point for the magic-shell command.
"""

import argparse
import asyncio
import sys
from pathlib import Path

from .core.bridge import PTYBridge
from .core.shell_detect import get_shell_with_fallback, get_shell_name
from .core.theme import create_theme, MagicTheme


def _handle_timing_event(theme: MagicTheme, event: str) -> None:
    """
    Handle shell timing events by calling appropriate theme methods.
    
    Args:
        theme: Theme instance
        event: Event name (command_start, command_end, prompt_start, prompt_end)
    """
    if event == "command_start":
        theme.on_command_start()
    elif event == "command_end":
        theme.on_command_end()  # TODO: Get actual exit code in PR 4
    elif event == "prompt_start":
        theme.on_prompt_start()
    elif event == "prompt_end":
        theme.on_prompt_end()


def main() -> int:
    """Main entry point for Magic Shell."""
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
        "--stage",
        action="store_true", 
        help="Enable experimental features",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.3.0",
    )
    
    args = parser.parse_args()
    
    try:
        # Detect shell to use
        shell_path = get_shell_with_fallback(args.shell)
        shell_name = get_shell_name(shell_path)
        
        # Create theme (effects disabled if --plain)
        theme_name = "plain" if args.plain else (args.theme or "veil")
        theme = create_theme(theme_name)
        
        # Show startup banner if effects enabled
        if not args.plain:
            theme.show_startup_banner()
            print(f"Wrapping {shell_name} with precise command timing")
            
        # Create PTY bridge
        bridge = PTYBridge(
            shell_path=shell_path,
            stage_mode=args.stage
        )
        
        # Connect theme to bridge events for future effects (PR 4)
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