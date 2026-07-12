"""
relnotes.render -- turn a list of Entry objects into readable output.

No file I/O, no argparse -- pure formatting functions, easy to test in
isolation from the CLI or the storage layer.
"""

from __future__ import annotations

from relnotes.core import VALID_CATEGORIES, Entry

CATEGORY_HEADINGS = {
    "added": "Added",
    "changed": "Changed",
    "fixed": "Fixed",
    "removed": "Removed",
    "security": "Security",
}


def _group_by_category(entries: list[Entry]) -> dict[str, list[Entry]]:
    grouped: dict[str, list[Entry]] = {c: [] for c in VALID_CATEGORIES}
    for entry in entries:
        grouped[entry.category].append(entry)
    return grouped


def format_markdown(entries: list[Entry], title: str = "Changelog") -> str:
    """Render entries as a Keep-a-Changelog-style Markdown document."""
    lines = [f"# {title}", ""]
    grouped = _group_by_category(entries)
    for category in VALID_CATEGORIES:
        items = grouped[category]
        if not items:
            continue
        lines.append(f"## {CATEGORY_HEADINGS[category]}")
        for entry in items:
            lines.append(f"- {entry.description} ({entry.date})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def format_plain(entries: list[Entry]) -> str:
    """Render entries as plain, unformatted lines -- one entry per line."""
    return "\n".join(f"[{entry.date}] {entry.category}: {entry.description}" for entry in entries)


# NOTE: format_html() does not exist yet -- that's a deliberate gap. A
# future mission adds an HTML output format for `relnotes render --format
# html`, reusing _group_by_category() the same way format_markdown() does.
