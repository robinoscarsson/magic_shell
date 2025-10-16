"""Magic Shell - A magical wrapper around your real shell.

Entry point for the magic-shell command.
"""

import argparse
import sys


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
        version="%(prog)s 0.1.0",
    )
    
    args = parser.parse_args()
    
    # For PR 1: Just print a message showing the new direction
    print("🪄 Magic Shell v0.1.0")
    print()
    print("A magical wrapper around your real shell.")
    print("Currently under active development - PTY bridge coming in PR 2!")
    print()
    print(f"Detected arguments:")
    print(f"  Shell: {args.shell or 'auto-detect'}")
    print(f"  Theme: {args.theme or 'default from config'}")
    print(f"  Plain mode: {args.plain}")
    print(f"  Staging: {args.stage}")
    print()
    print("🚧 This is PR 1: Packaging & README & CI skeleton")
    print("   Next: PR 2 will add PTY bridge and shell detection")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())