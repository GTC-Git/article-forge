"""Command-line interface for article-forge.

Pattern: each command is a cmd_<name> function; main() dispatches to it.
"""

import argparse
import sys

from forge import __version__
from forge.stations import intake


def cmd_version(args: argparse.Namespace) -> int:
    """Print the forge version."""
    print(f"article-forge {__version__}")
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    """Create a full article from a topic (starts a new run)."""
    report = intake.run({"topic": args.topic})

    if not report["success"]:
        print(f"error: {report['error']}", file=sys.stderr)
        return 1

    print(f"run created: {report['run_id']}")
    print(f"intake file: {report['output_file']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="forge",
        description="Turn a topic into a publish-ready MDX blog article.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Show the forge version")

    parser_new = subparsers.add_parser(
        "new",
        help="Create a full article from a topic",
        description="Create a full article from a topic (starts a new run).",
    )
    parser_new.add_argument(
        "topic",
        help='Article topic in quotes, e.g. "How to choose FPV motors"',
    )

    args = parser.parse_args()
    handler = globals().get(f"cmd_{args.command}")
    if handler is None:
        parser.error(f"Unknown command: {args.command}")
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())