#!/usr/bin/env python3
"""
Magic Shell - A magical command-line shell.

This is the main entry point for the Magic Shell application.
"""

import sys
from .core.shell import Shell

def main() -> int:
    """
    Main entry point for the Magic Shell application.
    
    Returns:
        int: Exit code (0 for normal exit, non-zero for errors)
    """
    shell = Shell()
    return shell.run()

if __name__ == "__main__":
    sys.exit(main())