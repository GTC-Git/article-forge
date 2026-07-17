"""Command-line interface for article-forge.

Pattern: each command is a cmd_<name> function; main() dispatches to it.
"""

import argparse
import sys

from forge import __version__


def cmd_version(args: argparse.Namespace) -> int:
    """Print the forge version."""
    print(f"article-forge {__version__}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="forge",
        description="Turn a topic into a publish-ready MDX blog article.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Show the forge version")

    args = parser.parse_args()
    handler = globals().get(f"cmd_{args.command}")
    if handler is None:
        parser.error(f"Unknown command: {args.command}")
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())