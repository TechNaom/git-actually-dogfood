"""
relnotes.cli -- the argparse entry point.

This module's only job is: parse sys.argv, call into core.py/render.py,
and turn the result (or a RelnotesError) into terminal output. No
storage or formatting logic lives here -- that split is what keeps
core.py and render.py testable without a terminal attached.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from relnotes.core import VALID_CATEGORIES, RelnotesError, add_entry, list_entries
from relnotes.render import format_markdown, format_plain


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="relnotes",
        description="Track and render release notes / changelog entries for a project.",
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("relnotes.json"),
        help="path to the JSON entry store (default: relnotes.json in the current directory)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="record a new changelog entry")
    add_parser.add_argument("description", help="what changed, in one sentence")
    add_parser.add_argument(
        "--category", required=True, choices=VALID_CATEGORIES, help="what kind of change this is"
    )
    add_parser.add_argument(
        "--date", default=None, help="ISO date, e.g. 2026-01-05 (default: today)"
    )

    list_parser = subparsers.add_parser("list", help="list all recorded entries")
    list_parser.add_argument(
        "--category",
        choices=VALID_CATEGORIES,
        default=None,
        help="only show entries in this category",
    )

    render_parser = subparsers.add_parser("render", help="render entries as a changelog document")
    render_parser.add_argument(
        "--format",
        choices=["markdown", "plain"],
        default="markdown",
        help="output format (default: markdown)",
    )
    render_parser.add_argument(
        "--title", default="Changelog", help="document title (markdown format only)"
    )

    return parser


def _cmd_add(args: argparse.Namespace) -> None:
    entry = add_entry(args.description, args.category, path=args.file, entry_date=args.date)
    print(f"Added [{entry.category}] {entry.description} ({entry.date})")


def _cmd_list(args: argparse.Namespace) -> None:
    entries = list_entries(path=args.file, category=args.category)
    if not entries:
        if args.category:
            print(f"No entries in category {args.category!r}.")
        else:
            print('No entries yet. Add one with: relnotes add "..." --category added')
        return
    for entry in entries:
        print(f"[{entry.date}] {entry.category}: {entry.description}")


def _cmd_render(args: argparse.Namespace) -> None:
    entries = list_entries(path=args.file)
    if args.format == "markdown":
        print(format_markdown(entries, title=args.title), end="")
    elif args.format == "plain":
        print(format_plain(entries))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "add":
            _cmd_add(args)
        elif args.command == "list":
            _cmd_list(args)
        elif args.command == "render":
            _cmd_render(args)
    except RelnotesError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
