"""Magic Shell - A magical wrapper around your real shell.

Entry point for the magic-shell command.
"""

import argparse
import asyncio
import sys
from pathlib import Path

from .core.bridge import PTYBridge
from .core.shell_detect import get_shell_with_fallback, get_shell_name


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
        version="%(prog)s 0.2.0",
    )
    
    args = parser.parse_args()
    
    try:
        # Detect shell to use
        shell_path = get_shell_with_fallback(args.shell)
        shell_name = get_shell_name(shell_path)
        
        # Show startup info (brief, non-intrusive)
        if not args.plain:
            print(f"🪄 Magic Shell v0.2.0 - Wrapping {shell_name}")
            
        # Create and run PTY bridge
        bridge = PTYBridge(
            shell_path=shell_path,
            stage_mode=args.stage
        )
        
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