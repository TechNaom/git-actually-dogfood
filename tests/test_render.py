"""test_render.py -- pytest suite for relnotes.render."""

from relnotes.core import Entry
from relnotes.render import format_markdown, format_plain


def _entries():
    return [
        Entry(description="Added dark mode", category="added", date="2026-01-05"),
        Entry(description="Fixed crash on startup", category="fixed", date="2026-01-06"),
        Entry(description="Removed legacy API", category="removed", date="2026-01-07"),
    ]


def test_format_markdown_groups_by_category_with_headings():
    output = format_markdown(_entries(), title="v1.1.0")

    assert "# v1.1.0" in output
    assert "## Added" in output
    assert "## Fixed" in output
    assert "## Removed" in output
    assert "- Added dark mode (2026-01-05)" in output


def test_format_markdown_omits_empty_categories():
    entries = [Entry(description="Added dark mode", category="added", date="2026-01-05")]

    output = format_markdown(entries)

    assert "## Added" in output
    assert "## Fixed" not in output
    assert "## Security" not in output


def test_format_markdown_empty_entries_still_has_title():
    output = format_markdown([], title="Nothing Yet")

    assert output.strip() == "# Nothing Yet"


def test_format_plain_one_line_per_entry():
    output = format_plain(_entries())

    lines = output.splitlines()
    assert len(lines) == 3
    assert lines[0] == "[2026-01-05] added: Added dark mode"
