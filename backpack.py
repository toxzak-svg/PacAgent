#!/usr/bin/env python3
"""
Backpack Agent Container System - Main Entry Point

This script provides the CLI interface for managing encrypted agent containers.
Run with --help to see available commands.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli import cli
from src.exceptions import BackpackError

if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)  # Standard exit code for Ctrl+C
    except BackpackError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        if e.details:
            print(f"  {e.details}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        if hasattr(e, '__cause__') and e.__cause__:
            print(f"  Caused by: {str(e.__cause__)}", file=sys.stderr)
        sys.exit(1)